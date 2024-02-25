import argparse
import logging
import os
import sys
from typing import List

import pcbnew

from .board_builder import BoardBuilder
from .defaults import DEFAULT_DIODE_POSITION, ZERO_POSITION
from .edge_generator import build_board_outline
from .element_position import ElementInfo, ElementPosition, Point, PositionOption, Side
from .key_placer import KeyPlacer
from .template_copier import copy_from_template_to_board

logger = logging.getLogger(__name__)


class ElementInfoAction(argparse.Action):
    def __call__(self, parser, namespace, values: str, option_string=None) -> None:
        try:
            value: ElementInfo = self.parse(values, option_string)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))
        setattr(namespace, self.dest, value)

    def parse(self, values: str, option_string) -> ElementInfo:
        tokens: list[str] = values.split()
        err = ""
        if len(tokens) not in [2, 3, 6]:
            err = f"{option_string} invalid format."
            raise ValueError(err)
        else:
            annotation = tokens[0]
            if annotation.count("{}") != 1:
                err = (
                    f"'{annotation}' invalid annotation specifier, "
                    "it must contain exactly one '{}' placeholder."
                )
                raise ValueError(err)

            option = PositionOption.get(tokens[1])
            position = None
            template_path = ""

            if len(tokens) == 2:
                if option not in [
                    PositionOption.RELATIVE,
                    PositionOption.DEFAULT,
                    PositionOption.UNCHANGED,
                ]:
                    err = (
                        f"{option_string} position option needs to be equal "
                        "RELATIVE or DEFAULT if position details not provided"
                    )
                    raise ValueError(err)
            elif len(tokens) == 3:
                if option not in [PositionOption.PRESET, PositionOption.RELATIVE]:
                    err = (
                        f"{option_string} position option needs to be equal"
                        "RELATIVE or PRESET when providing template path"
                    )
                    raise ValueError(err)
            elif option != PositionOption.CUSTOM:
                err = (
                    f"{option_string} position option needs to be equal CUSTOM "
                    "when providing position details"
                )
                raise ValueError(err)

            if option == PositionOption.CUSTOM:
                floats = tuple(map(float, tokens[2:5]))
                side = Side.get(tokens[5])
                position = ElementPosition(Point(floats[0], floats[1]), floats[2], side)
            elif option == PositionOption.RELATIVE:
                # template path if optional for RELATIVE option:
                if len(tokens) == 3:
                    template_path = tokens[2]
            elif option == PositionOption.PRESET:
                template_path = tokens[2]

            value: ElementInfo = ElementInfo(
                annotation,
                option,
                position,
                template_path,
            )
            return value


class ElementInfoListAction(ElementInfoAction):
    def __call__(self, parser, namespace, values: str, option_string=None) -> None:
        try:
            if "DEFAULT" in values:
                msg = f"{option_string} does not support DEFAULT position"
                raise ValueError(msg)
            value: List[ElementInfo] = []
            tokens: list[str] = values.split(";")
            for token in tokens:
                element_info: ElementInfo = super().parse(token.strip(), option_string)
                value.append(element_info)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))
        setattr(namespace, self.dest, value)


class XYAction(argparse.Action):
    def __call__(self, parser, namespace, values: str, option_string=None) -> None:
        try:
            value = tuple(map(float, values.split()))
            if len(value) != 2:
                msg = (
                    f"{option_string} must be exactly two numeric values "
                    "separated by a space."
                )
                raise ValueError(msg)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))
        setattr(namespace, self.dest, value)


def app():
    parser = argparse.ArgumentParser(
        description="Keyboard's key autoplacer",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-b",
        "--board",
        required=True,
        help=".kicad_pcb file to be processed or created",
    )
    parser.add_argument(
        "-l", "--layout", required=False, help="json layout definition file"
    )
    parser.add_argument(
        "--route-switches-with-diodes",
        action="store_true",
        help="Enable switch-diode routing",
    )
    parser.add_argument(
        "--route-rows-and-columns",
        action="store_true",
        help="Enable rows/columns routing",
    )
    parser.add_argument(
        "-d",
        "--diode",
        default=ElementInfo("D{}", PositionOption.DEFAULT, DEFAULT_DIODE_POSITION, ""),
        action=ElementInfoAction,
        help=(
            "Diode information, space separated value of ANNOTATION OPTION [POSITION]\n"
            "Available OPTION choices: DEFAULT, UNCHANGED, RELATIVE, PRESET and CUSTOM\n"
            "When DEFAULT or UNCHAGED, then POSITION needs to be omitted,\n"
            "when RELATIVE, then POSITION is optional path for saving kicad_pcb template file\n"
            "when PRESET, then POSITION is mandatory path to kicad_pcb template file\n"
            "when CUSTOM, then POSITION is space separated value of X Y ORIENTATION FRONT|BACK\n"
            "for example:\n"
            "\tD{} RELATIVE\n"
            "\tD{} PRESET /home/user/project/diode_preset.kicad_pcb\n"
            "\tD{} CUSTOM 5 -4.5 90 BACK\n"
            "equal 'D{} DEFAULT' by default"
        ),
    )
    parser.add_argument(
        "--additional-elements",
        default=[
            ElementInfo(
                "ST{}",
                PositionOption.CUSTOM,
                ZERO_POSITION,
                "",
            )
        ],
        action=ElementInfoListAction,
        help=(
            "List of ';' separated additional elements ELEMENT_INFO values\n"
            "ELEMENT_INFO is space separated value of ANNOTATION OPTION POSITION\n"
            "Available OPTION choices: RELATIVE, PRESET and CUSTOM\n"
            "when RELATIVE, then POSITION is optional path for saving kicad_pcb template file\n"
            "when PRESET, then POSITION is mandatory path to kicad_pcb template file\n"
            "when CUSTOM, then POSITION is space separated value of X Y ORIENTATION FRONT|BACK\n"
            "for example:\n"
            "\tST{} CUSTOM 0 0 180 BACK;LED{} RELATIVE\n"
            "equal 'ST{} CUSTOM 0 0 0 FRONT' by default"
        ),
    )
    parser.add_argument(
        "--key-distance",
        default=(19.05, 19.05),
        action=XYAction,
        help=(
            "X and Y key 1U distance in mm, as two space separated numeric values, "
            "19.05 19.05 by default"
        ),
    )
    parser.add_argument("-t", "--template", help="Controller circuit template")
    parser.add_argument(
        "--build-board-outline",
        required=False,
        action="store_true",
        help="Enables board outline generation around switch footprints.",
    )
    parser.add_argument(
        "--outline-delta",
        required=False,
        default=0.0,
        type=float,
        help="The amount (in millimetres) to inflate/deflate board outline.",
    )
    parser.add_argument(
        "--create-from-annotated-layout",
        required=False,
        action="store_true",
        help=(
            "Enables experimental creation mode, where via-annotated kle layout is used\n"
            "for adding footprints and netlists to the newly created board file.\n"
        ),
    )
    parser.add_argument(
        "--switch-footprint",
        required=False,
        type=str,
        help=(
            "Full path to switch footprint, required when `--crate-from-via` option used."
        ),
    )
    parser.add_argument(
        "--diode-footprint",
        required=False,
        type=str,
        help=(
            "Full path to diode footprint, required when `--crate-from-via` option used."
        ),
    )

    args = parser.parse_args()

    layout_path = args.layout
    board_path = args.board

    # set up logger
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s: %(message)s", datefmt="%H:%M:%S"
    )

    if args.create_from_annotated_layout:
        if os.path.isfile(board_path):
            logger.error(f"File {board_path} already exist, aborting")
            sys.exit(1)

        builder = BoardBuilder(
            switch_footprint=args.switch_footprint,
            diode_footprint=args.diode_footprint,
        )
        board = builder.create_board(layout_path)
        board.Save(board_path)

    board = pcbnew.LoadBoard(board_path)

    placer = KeyPlacer(board, args.key_distance)
    placer.run(
        layout_path,
        ElementInfo("SW{}", PositionOption.DEFAULT, ZERO_POSITION, ""),
        args.diode,
        args.route_switches_with_diodes,
        args.route_rows_and_columns,
        additional_elements=args.additional_elements,
    )

    if args.build_board_outline:
        build_board_outline(board, args.outline_delta, "SW{}")

    if args.template:
        copy_from_template_to_board(board, args.template, args.route_rows_and_columns)

    pcbnew.Refresh()
    pcbnew.SaveBoard(board_path, board)

    logging.shutdown()


if __name__ == "__main__":
    app()
