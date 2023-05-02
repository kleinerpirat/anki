// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./main-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";

import { bridgeCommand } from "@tslib/bridgecommand";
import type Reviewer from "reviewer-iframe/Reviewer.svelte";
import { tick } from "svelte";
import type { ReviewerArgs } from "../reviewer-iframe/types";
import type DeckBrowser from "./deck-browser/DeckBrowser.svelte";
import MainPage from "./MainPage.svelte";
import type StatusBar from "./status-bar/StatusBar.svelte";
import type Toolbar from "./toolbar/Toolbar.svelte";
import { MainPageArgs, MainPageContext } from "./types";
import { mwContext } from "./lib";

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
let toolbar: Toolbar;
let deckBrowser: DeckBrowser;
let statusBar: StatusBar;

let initialized = false;

async function setupMainPage(props: any) {
    checkNightMode();
    await i18n;

    page = new MainPage({
        target: document.body,
        props,
    });

    await tick();

    ({ toolbar, deckBrowser, statusBar } = page.getComponents());
    console.log(toolbar);

    initialized = true;

    return page;
}

export async function updateMainPage(args: MainPageArgs): Promise<void> {
    if (!initialized) {
        setupMainPage({ args });
    } else {
        page.$set({ args });
    }
}

export function setHomeState() : void {
    mwContext.set(MainPageContext.HOME)
}

export function focusSearch(): void {
    deckBrowser.focusSearch();
}
export function showDecks(): void {
    if (!page) {
        return;
    }
    page.$set({ decksCollapsed: false });
}

export async function setupDeckOptions(): Promise<void> {
    mwContext.set(MainPageContext.DECK_OPTIONS)
}

export function setupReviewer(args: ReviewerArgs): void {
    page.$set({ mode: MainPageContext.REVIEW, reviewerArgs: args });
}

export async function setupStats(): Promise<void> {
    mwContext.set(MainPageContext.STATS)
}

export async function setupCustomStudy(): Promise<void> {
    mwContext.set(MainPageContext.CUSTOM_STUDY)
}

export function selectedAnswerButton(): number {
    return 2;
}

export function getTypedAnswer(): string | null {
    return null; // typeans?.value ?? null;
}

export function _drawFlag(flag: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7): void {
    const elem = document.getElementById("_flag")!;
    elem.toggleAttribute("hidden", flag === 0);
    elem.style.color = `var(--flag-${flag})`;
}

export function _drawMark(mark: boolean): void {
    document.getElementById("_mark")!.toggleAttribute("hidden", !mark);
}

export function _typeAnsPress(): void {
    const code = (window.event as KeyboardEvent).code;
    if (["Enter", "NumpadEnter"].includes(code)) {
        bridgeCommand("ans");
    }
}

export function _emulateMobile(enabled: boolean): void {
    document.documentElement.classList.toggle("mobile", enabled);
}

export function setRefreshNeeded(needed: boolean): void {
    page.$set({ refreshNeeded: true });
}
