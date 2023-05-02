// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./previewer-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";

import PreviewerPage from "./PreviewerPage.svelte";

const i18n = setupI18n({
    modules: [ModuleName.ACTIONS],
});

export async function setupPreviewer(
    target: HTMLElement,
    props = {},
): Promise<PreviewerPage> {
    checkNightMode();
    await i18n;

    return new PreviewerPage({ target, props });
}
