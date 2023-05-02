# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from enum import Enum


class Props(Enum):
    FONT_SIZE = "font-size"

    BORDER_RADIUS = "border-radius"
    BORDER_RADIUS_MEDIUM = "border-radius-medium"
    BORDER_RADIUS_LARGE = "border-radius-large"

    BLUR = "blur"

    OPACITY_DISABLED = "opacity-disabled"
    OPACITY_IDLE = "opacity-idle"
    OPACITY_HOVER = "opacity-hover"

    TRANSITION = "transition"
    TRANSITION_MEDIUM = "transition-medium"
    TRANSITION_SLOW = "transition-slow"
