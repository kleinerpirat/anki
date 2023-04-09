// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./toolbar-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";

import Toolbar from "./Toolbar.svelte";
import type { ToolbarArgs } from "../toolbar/types";
import type { SyncStatus } from "./types";

const i18n = setupI18n({
    modules: [ModuleName.ACTIONS, ModuleName.QT_MISC],
});

let page: Toolbar;

export function setSyncActive(active: boolean): boolean {
    if (!page) {
        return false;
    }
    page.$set({
        syncActive: active,
    });
    return true;
}

export function setSyncStatus(status: SyncStatus): boolean {
    if (!page) {
        return false;
    }
    page.$set({
        syncStatus: status,
    });
    return true;
}

export async function setupTopToolbar(args: ToolbarArgs): Promise<Toolbar> {
    checkNightMode();
    await i18n;

    page = new Toolbar({
        target: document.body,
        props: {
            centerTrayContent: args.centerTrayContent,
            leftTrayContent: args.leftTrayContent,
            rightTrayContent: args.rightTrayContent,
            theme: args.theme
        },
    });

    return page;
}

globalThis.setupTopToolbar = setupTopToolbar;
globalThis.setSyncActive = setSyncActive;
globalThis.setSyncStatus = setSyncStatus;
