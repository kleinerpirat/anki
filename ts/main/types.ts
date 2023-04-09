// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL | version 3 or later; http://www.gnu.org/licenses/agpl.html

import type { Decks } from "@tslib/proto";

export enum MainViewMode {
    OVERVIEW,
    DECK_OPTIONS,
    REVIEW,
    STATS,
    CUSTOM_STUDY,
}

export type OverviewArgs = {
    deck: {
        name: string;
        finished: boolean;
        isDyn: boolean;
        description: string;
        url: string;
    };
    markdown: boolean;
    days: number;
};

export type DeckBrowserArgs = {
    dueTree: Decks.DeckTreeNode;
    currentDeckId: number;
    schedulerVersion: number;
    studiedToday: string;
    searchTerm: string;
};

export interface FilteredDeckTree extends Decks.DeckTreeNode {
    matched: boolean;
    containsMatch: boolean;
    children: FilteredDeckTree[];
}

export type DeckEditorArgs = {
    description: string;
    markdown: boolean;
};

export type ReviewerArgs = {
    softwareDriver: boolean;
    extraContent: string;
};
