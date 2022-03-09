// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./main-view-base.css";

import { ModuleName, setupI18n } from "../lib/i18n";
import { checkNightMode } from "../lib/nightmode";

import MainViewPage from "./MainViewPage.svelte";
let page;

export async function setupMainView(args): Promise<MainViewPage> {
    await setupI18n({
        modules: [
            ModuleName.BROWSING,
            ModuleName.SCHEDULING,
            ModuleName.ACTIONS,
            ModuleName.QT_MISC,
        ],
    });

    checkNightMode();

    page = new MainViewPage({
        target: document.body,
        props: { args },
    });

    return page;
}

export function refreshMainView(args) {
    page.refresh(args);
}
