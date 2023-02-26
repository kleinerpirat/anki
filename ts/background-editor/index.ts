// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./background-editor-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";

import BackgroundEditor from "./BackgroundEditor.svelte";

const i18n = setupI18n({ modules: [ModuleName.PREFERENCES] });

export async function setupBackgroundEditor(backgroundCSS: string): Promise<BackgroundEditor> {
    checkNightMode();
    await i18n;

    const page = new BackgroundEditor({
        target: document.body,
        props: { backgroundCSS },
    });

    return page;
}
