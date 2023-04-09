// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./main-base.scss";

import type { Decks } from "@tslib/proto";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";
import { setupDeckOptions as setupDeckConfig } from "../deck-options/index";
import { setupGraphsPage } from "../graphs/index";

import MainPage from "./MainPage.svelte";
import { MainViewMode } from "./types";
import type { OverviewArgs, ReviewerArgs } from "./types";
import type { ToolbarArgs } from "./toolbar/types";
import { tick } from "svelte";

const i18n = setupI18n({
    modules: [
        ModuleName.CUSTOM_STUDY,
        ModuleName.DECKS,
        ModuleName.ACTIONS,
        ModuleName.CARD_STATS,
        ModuleName.STATISTICS,
        ModuleName.STUDYING,
        ModuleName.SCHEDULING,
        ModuleName.DECK_CONFIG,
        ModuleName.HELP,
        ModuleName.KEYBOARD,
        ModuleName.QT_MISC,
        ModuleName.PREFERENCES,
    ],
});

let page: MainPage;

async function setupMainPage(props: any) {
    checkNightMode();
    await i18n;

    page = new MainPage({
        target: document.body,
        props,
    });

    return page;
}

export async function setupDeckBrowser(
    dueTree: Decks.DeckTreeNode,
    deckBrowserArgs: {
        currentDeckId: number;
        schedulerVersion: number;
        studiedToday: string;
    },
    overviewArgs: OverviewArgs,
    toolbarArgs: ToolbarArgs,
    reviewerArgs: ReviewerArgs,
    serverURL: string,
): Promise<void> {
    const props = {
        deckBrowserArgs: Object.assign(deckBrowserArgs, { dueTree, searchTerm: "" }),
        overviewArgs,
        toolbarArgs,
        reviewerArgs,
        serverURL,
        decksCollapsed: false,
        mode: MainViewMode.OVERVIEW,
    };
    if (!page) {
        setupMainPage(props);
    } else {
        page.$set(props);
    }
}

export async function setupDeckOptions(did: number): Promise<void> {
    if (!page) {
        return;
    }
    page.$set({ mode: MainViewMode.DECK_OPTIONS });
    await tick();
    setupDeckConfig(did, document.getElementById("deckOptions")!);
}

export function setupReviewer(): void {
    if (!page) {
        return;
    }
    page.$set({ mode: MainViewMode.REVIEW });
}

export async function setupStats(): Promise<void> {
    if (!page) {
        return;
    }
    page.$set({ mode: MainViewMode.STATS });
    await tick();
    setupGraphsPage(document.getElementById("stats")!);
}

export async function setupCustomStudy(): Promise<void> {
    if (!page) {
        return;
    }
    page.$set({ mode: MainViewMode.CUSTOM_STUDY });
}
