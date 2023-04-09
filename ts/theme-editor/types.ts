// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

export type Theme = {
    bg: Background;
};

export type Background = {
    background: string;
    saturation: number;
    opacity: number;
    blur: number;
};

export type Palette = {
    name: string;
    comment: string;
    value: string;
}[];

export enum EditorMode {
    THEME,
    BACKGROUND,
    PALETTE,
}
