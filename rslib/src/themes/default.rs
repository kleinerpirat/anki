// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

pub use palette::LinSrgba;

pub use crate::pb::themes::Vars;
pub use crate::pb::themes::Factors;
pub use crate::pb::themes::Palette;
pub use crate::pb::themes::Color;

macro_rules! rgba {
    ($r:expr, $g:expr, $b:expr, $a:expr $(,)?) => {
        LinSrgba::new(
            f32::from($r) / 255.0,
            f32::from($g) / 255.0,
            f32::from($b) / 255.0,
            f32::from($a),
        )
    };
}

const DEFAULT_FACTORS: Factors = Factors {
    font_size: 1.0,
    transparency: 0.35,
    roundness: 1.0,
    spacing: 1.0,
    animation_speed: 1.0,

    other: Vec::new(),
};

const DEFAULT_PALETTE: Palette = Palette {
    canvas: Color {
        light: rgba!(245, 245, 245, 1),
        dark: rgba!(44, 44, 44, 1),
    },
    canvas_secondary: Color {
        light: rgba!(255, 255, 255, 1),
        dark: rgba!(54, 54, 54, 1),
    },
    input_bg: Color {
        light: rgba!(255, 255, 255, 1),
        dark: rgba!(44, 44, 44, 1),
    },
    code_bg: Color {
        light: rgba!(255, 255, 255, 1),
        dark: rgba!(37, 37, 37, 1),
    },
    fg: Color {
        light: rgba!(2, 2, 2, 1),
        dark: rgba!(252, 252, 252, 1),
    },
    border: Color {
        light: rgba!(196, 196, 196, 1),
        dark: rgba!(32, 32, 32, 1),
    },
    focus: Color {
        light: rgba!(59, 1, 246, 1),
        dark: rgba!(59, 130, 246, 1),
    },
    shadow: Color {
        light: rgba!(54, 54, 54, 0.6),
        dark: rgba!(20, 20, 20, 1),
    },
    glass: Color {
        light: rgba!(255, 255, 255, 0.4),
        dark: rgba!(54, 54, 54, 0.4),
    },
    button: Color {
        light: rgba!(252, 252, 252, 1),
        dark: rgba!(64, 64, 64, 1),
    },
    button_primary: Color {
        light: rgba!(48, 107, 236, 1),
        dark: rgba!(38, 82, 207, 1),
    },
    scrollbar: Color {
        light: rgba!(214, 214, 214, 1),
        dark: rgba!(69, 69, 69, 1),
    },
    link: Color {
        light: rgba!(29, 78, 216, 1),
        dark: rgba!(191, 219, 254, 1),
    },
    warning: Color {
        light: rgba!(239, 68, 68, 1),
        dark: rgba!(248, 113, 113, 1),
    },
    card: Color {
        light: rgba!(96, 165, 250, 1),
        dark: rgba!(147, 197, 253, 1),
    },
    note: Color {
        light: rgba!(34, 197, 94, 1),
        dark: rgba!(74, 222, 128, 1),
    },
    flag_1: Color {
        light: rgba!(239, 68, 68, 1),
        dark: rgba!(248, 113, 113, 1),
    },
    flag_2: Color {
        light: rgba!(251, 146, 60, 1),
        dark: rgba!(253, 186, 116, 1),
    },
    flag_3: Color {
        light: rgba!(74, 222, 128, 1),
        dark: rgba!(134, 239, 172, 1),
    },
    flag_4: Color {
        light: rgba!(59, 1, 246, 1),
        dark: rgba!(96, 165, 250, 1),
    },
    flag_5: Color {
        light: rgba!(232, 121, 249, 1),
        dark: rgba!(240, 171, 252, 1),
    },
    flag_6: Color {
        light: rgba!(45, 212, 191, 1),
        dark: rgba!(94, 234, 212, 1),
    },
    flag_7: Color {
        light: rgba!(168, 85, 247, 1),
        dark: rgba!(192, 132, 252, 1),
    },
    card_new: Color {
        light: rgba!(59, 1, 246, 1),
        dark: rgba!(147, 197, 253, 1),
    },
    card_learn: Color {
        light: rgba!(220, 38, 38, 1),
        dark: rgba!(248, 113, 113, 1),
    },
    card_review: Color {
        light: rgba!(22, 163, 74, 1),
        dark: rgba!(34, 197, 94, 1),
    },
    card_buried: Color {
        light: rgba!(245, 158, 11, 1),
        dark: rgba!(146, 64, 14, 1),
    },
    card_suspended: Color {
        light: rgba!(250, 204, 21, 1),
        dark: rgba!(254, 249, 195, 1),
    },
    card_marked: Color {
        light: rgba!(99, 102, 241, 1),
        dark: rgba!(168, 85, 247, 1),
    },
    highlighted_bg: Color {
        light: rgba!(37, 99, 235, 0.5),
        dark: rgba!(147, 197, 253, 0.5),
    },
    highlighted_fg: Color {
        light: rgba!(0, 0, 0, 1),
        dark: rgba!(255, 255, 255, 1),
    },
    selected_bg: Color {
        light: rgba!(214, 214, 214, 0.5),
        dark: rgba!(147, 197, 253, 0.5),
    },
    selected_fg: Color {
        light: rgba!(0, 0, 0, 1),
        dark: rgba!(255, 255, 255, 1),
    },
    other: Vec::new(),
};

pub const DEFAULT_VARS: Vars = Vars {
    factors: DEFAULT_FACTORS,
    palette: DEFAULT_PALETTE,
};
