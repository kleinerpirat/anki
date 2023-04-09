class Color(dict):
    def __init__(self, red: int, green: int, blue: int, alpha: float):
        self["red"] = red
        self["green"] = green
        self["blue"] = blue
        self["alpha"] = int(alpha * 255)


DEFAULT_LIGHT_PALETTE = {
    "canvas": Color(245, 245, 245, 1),
    "canvas-secondary": Color(255, 255, 255, 1),
    "canvas-code": Color(255, 255, 255, 1),

    "fg": Color(2, 2, 2, 1),
    "fg-subtle": Color(30, 30, 30, 1),
    "fg-disabled": Color(50, 50, 50, 1),

    "link": Color(29, 78, 216, 1),

    "border": Color(196, 196, 196, 1),
    "border-subtle": Color(210, 210, 210, 1),

    "focus": Color(59, 1, 246, 1),
    "shadow": Color(54, 54, 54, 0.6),

    "glass": Color(255, 255, 255, 0.4),
    "glass-thick": Color(255, 255, 255, 0.6),

    "button": Color(252, 252, 252, 1),
    "button-gradient-start": Color(255, 255, 255, 1),
    "button-gradient-end": Color(245, 245, 245, 1),
    "button-disabled": Color(252, 252, 252, 0.4),

    "button-primary": Color(48, 107, 236, 1),
    "button-primary-gradient-start": Color(54, 113, 242, 1),
    "button-primary-gradient-end": Color(42, 101, 230, 1),
    "button-primary-disabled": Color(48, 107, 236, 0.4),

    "scrollbar": Color(214, 214, 214, 1),
    "scrollbar-hover": Color(207, 207, 207, 1),
    "scrollbar-pressed": Color(200, 200, 200, 1),

    "input-bg": Color(255, 255, 255, 1),
    "card": Color(96, 165, 250, 1),
    "note": Color(34, 197, 94, 1),
    "warning": Color(239, 68, 68, 1),
    "flag-1": Color(239, 68, 68, 1),
    "flag-2": Color(251, 146, 60, 1),
    "flag-3": Color(74, 222, 128, 1),
    "flag-4": Color(59, 1, 246, 1),
    "flag-5": Color(232, 121, 249, 1),
    "flag-6": Color(45, 212, 191, 1),
    "flag-7": Color(168, 85, 247, 1),
    "card-new": Color(59, 1, 246, 1),
    "card-learn": Color(220, 38, 38, 1),
    "card-review": Color(22, 163, 74, 1),
    "card-buried": Color(245, 158, 11, 1),
    "card-suspended": Color(250, 204, 21, 1),
    "card-marked": Color(99, 102, 241, 1),
    "text-highlighted-bg": Color(37, 99, 235, 0.5),
    "text-highlighted-fg": Color(0, 0, 0, 1),
    "item-selected-bg": Color(214, 214, 214, 0.5),
    "item-selected-fg": Color(0, 0, 0, 1),
    "search-match-bg": Color(214, 214, 214, 0.5),
    "search-match-fg": Color(0, 0, 0, 1),
}

DEFAULT_DARK_PALETTE = {
    "canvas": Color(44, 44, 44, 1),
    "canvas-secondary": Color(54, 54, 54, 1),
    "canvas-code": Color(37, 37, 37, 1),

    "fg": Color(252, 252, 252, 1),
    "fg-subtle": Color(200, 200, 200, 1),
    "fg-disabled": Color(170, 170, 170, 1),

    "link": Color(191, 219, 254, 1),

    "border": Color(32, 32, 32, 1),
    "border-subtle": Color(36, 36, 36, 1),

    "focus": Color(59, 130, 246, 1),
    "shadow": Color(20, 20, 20, 1),
    "glass": Color(54, 54, 54, 0.4),
    "glass-thick": Color(54, 54, 54, 0.6),

    "button": Color(64, 64, 64, 1),
    "button-gradient-start": Color(70, 70, 70, 1),
    "button-gradient-end": Color(60, 60, 60, 1),
    "button-disabled": Color(64, 64, 64, 0.4),

    "button-primary": Color(38, 82, 207, 1),
    "button-primary-gradient-start": Color(42, 86, 211, 1),
    "button-primary-gradient-end": Color(34, 78, 203, 1),
    "button-primary-disabled": Color(38, 82, 207, 0.4),

    "scrollbar": Color(69, 69, 69, 1),
    "scrollbar-hover": Color(75, 75, 75, 1),
    "scrollbar-pressed": Color(78, 78, 78, 1),

    "input-bg": Color(44, 44, 44, 1),
    "card": Color(147, 197, 253, 1),
    "note": Color(74, 222, 128, 1),
    "warning": Color(248, 113, 113, 1),
    "flag-1": Color(248, 113, 113, 1),
    "flag-2": Color(253, 186, 116, 1),
    "flag-3": Color(134, 239, 172, 1),
    "flag-4": Color(96, 165, 250, 1),
    "flag-5": Color(240, 171, 252, 1),
    "flag-6": Color(94, 234, 212, 1),
    "flag-7": Color(192, 132, 252, 1),
    "card-new": Color(147, 197, 253, 1),
    "card-learn": Color(248, 113, 113, 1),
    "card-review": Color(34, 197, 94, 1),
    "card-buried": Color(146, 64, 14, 1),
    "card-suspended": Color(254, 249, 195, 1),
    "card-marked": Color(168, 85, 247, 1),
    "text-highlighted-bg": Color(147, 197, 253, 0.5),
    "text-highlighted-fg": Color(255, 255, 255, 1),
    "item-selected-bg": Color(147, 197, 253, 0.5),
    "item-selected-fg": Color(255, 255, 255, 1),
    "search-match-bg": Color(147, 197, 253, 0.5),
    "search-match-fg": Color(255, 255, 255, 1),
}
