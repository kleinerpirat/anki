// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./deck-browser-base.css";

import { ModuleName, setupI18n } from "../lib/i18n";
import { checkNightMode } from "../lib/nightmode";

import DeckBrowserPage from "./DeckBrowserPage.svelte";
let page;

export async function setupDeckBrowser(args): Promise<DeckBrowserPage> {
    await setupI18n({
        modules: [ModuleName.BROWSING, ModuleName.SCHEDULING, ModuleName.ACTIONS],
    });

    checkNightMode();

    page = new DeckBrowserPage({
        target: document.body,
        props: { args },
    });

    return page;
}

export function refreshDeckBrowser(args) {
    page.refresh(args);
}
