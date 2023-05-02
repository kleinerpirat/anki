# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from enum import Enum


class Colors(Enum):
    CANVAS = "canvas"
    CANVAS_SECONDARY = "canvas-secondary"
    CANVAS_CODE = "canvas-code"

    FG = "fg"
    FG_SUBTLE = "fg-subtle"
    FG_DISABLED = "fg-disabled"

    LINK = "link"

    ACCENT_PRIMARY = "accent-primary"
    ACCENT_SECONDARY = "accent-secondary"

    BORDER = "border"
    BORDER_SUBTLE = "border-subtle"

    FOCUS = "focus"
    SHADOW = "shadow"

    GLASS = "glass"
    GLASS_THICK = "glass-thick"

    BUTTON = "button"
    BUTTON_GRADIENT_START = "button-gradient-start"
    BUTTON_GRADIENT_END = "button-gradient-end"
    BUTTON_DISABLED = "button-disabled"

    BUTTON_PRIMARY = "button-primary"
    BUTTON_PRIMARY_GRADIENT_START = "button-primary-gradient-start"
    BUTTON_PRIMARY_GRADIENT_END = "button-primary-gradient-end"
    BUTTON_PRIMARY_DISABLED = "button-primary-disabled"

    SCROLLBAR = "scrollbar"
    SCROLLBAR_HOVER = "scrollbar-hover"
    SCROLLBAR_PRESSED = "scrollbar-pressed"

    INPUT_BG = "input-bg"
    WARNING = "warning"
    FLAG_1 = "flag-1"
    FLAG_2 = "flag-2"
    FLAG_3 = "flag-3"
    FLAG_4 = "flag-4"
    FLAG_5 = "flag-5"
    FLAG_6 = "flag-6"
    FLAG_7 = "flag-7"
    CARD_NEW = "card-new"
    CARD_LEARN = "card-learn"
    CARD_REVIEW = "card-review"
    CARD_BURIED = "card-buried"
    CARD_SUSPENDED = "card-suspended"
    CARD_MARKED = "card-marked"
    TEXT_HIGHLIGHTED_BG = "text-highlighted-bg"
    TEXT_HIGHLIGHTED_FG = "text-highlighted-fg"
    ITEM_SELECTED_BG = "item-selected-bg"
    ITEM_SELECTED_FG = "item-selected-fg"
