// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL | version 3 or later; http://www.gnu.org/licenses/agpl.html

import type { Decks } from "@tslib/proto";
import type { Stats } from "@tslib/proto";
import type { RevlogRange } from "graphs/graph-helpers";
import type { PreferenceStore } from "sveltelib/preferences";
import type Toolbar from "./toolbar/Toolbar.svelte";
import type { ToolbarContent } from "./toolbar/types";
import type DeckBrowser from "./deck-browser/DeckBrowser.svelte";
import type StatusBar from "./status-bar/StatusBar.svelte";
import type { StatusBarContent } from "./status-bar/types";

export enum MainPageContext {
    HOME,
    REVIEW,
    CUSTOM_STUDY,
    DECK_OPTIONS,
    STATS,
}

export type MainPageComponents = {
    toolbar: Toolbar;
    deckBrowser: DeckBrowser;
    statusBar: StatusBar;
};

export type MainPageArgs = {
    profiles: {
        current: string;
        other: string[];
    };
    schedulerVersion: number;
    dueTree: Decks.DeckTreeNode;
    deck: {
        id: number;
        name: string;
        description: string;
        markdownDescription: boolean;
        finished: boolean;
        isDyn: boolean;
        url: string;
    };
    defaultStatsDays: number;
    addonContent: {
        deckBrowser: {
            toolbar: string[];
        };
        overview: {
            body: string[];
        };
        toolbar: ToolbarContent;
        statusBar: StatusBarContent;
    };
};

export interface Deck extends Decks.DeckTreeNode {
    matched?: boolean;
    containsMatch?: boolean;
    children: Deck[];
}

export type DeckEditorArgs = {
    description: string;
    markdown: boolean;
};

export type StatsData = {
    sourceData: Stats.GraphsResponse | null;
    preferences: PreferenceStore<Stats.GraphPreferences> | null;
    revlogRange: RevlogRange;
};
