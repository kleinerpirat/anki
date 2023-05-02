// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./theme-editor-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";

import ThemeEditor from "./ThemeEditor.svelte";
import type { Theme } from "./types";

const i18n = setupI18n({ modules: [ModuleName.PREFERENCES] });

let page: ThemeEditor;

export async function setupThemeEditor({
    light,
    dark,
}: {
    light: Theme;
    dark: Theme;
}): Promise<ThemeEditor> {
    checkNightMode();
    await i18n;

    page = new ThemeEditor({
        target: document.body,
        props: { light, dark },
    });

    return page;
}

export function setBackgroundImage(name: string): void {
    if (!page) {
        return;
    }
    page.setBackgroundImage(name);
}
