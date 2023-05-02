# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re
import sys
from pathlib import Path

sys.path.append("out/qt")
from colors_default import DEFAULT_DARK_PALETTE, DEFAULT_LIGHT_PALETTE


def lowercase_var(name: str) -> str:
    return name.lower().replace("_", "-")


def backend_color_to_hex(color: dict) -> str:
    return f"""{color["red"]:x}{color["green"]:x}{color["blue"]:x}"""


input_path = Path(sys.argv[1])
input_name = input_path.stem
color_names = sys.argv[2].split(":")

# two files created for each additional color
offset = len(color_names) * 2
svg_paths = sys.argv[3 : 3 + offset]

with open(input_path, "r") as f:
    svg_data = f.read()

    for color_name in color_names:
        light_svg = dark_svg = ""

        if color_name == "FG":
            prefix = input_name
        else:
            prefix = f"{input_name}-{color_name}"

        for path in svg_paths:
            if f"{prefix}-light.svg" in path:
                light_svg = path
            elif f"{prefix}-dark.svg" in path:
                dark_svg = path

        def substitute(data: str, filename: str, palette: dict) -> None:
            if "fill" in data:
                data = re.sub(
                    r"fill=\"#.+?\"",
                    f'fill="{backend_color_to_hex(palette[lowercase_var(color_name)])}"',
                    data,
                )
            else:
                data = re.sub(
                    r"<svg",
                    f'<svg fill="{backend_color_to_hex(palette[lowercase_var(color_name)])}"',
                    data,
                    1,
                )
            with open(filename, "w") as f:
                f.write(data)

        substitute(svg_data, light_svg, DEFAULT_LIGHT_PALETTE)
        substitute(svg_data, dark_svg, DEFAULT_DARK_PALETTE)
