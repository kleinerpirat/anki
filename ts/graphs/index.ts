// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import "./graphs-base.scss";

import { ModuleName, setupI18n } from "@tslib/i18n";
import { checkNightMode } from "@tslib/nightmode";
import type { SvelteComponentDev } from "svelte/internal";

import GraphsPage from "./GraphsPage.svelte";

const i18n = setupI18n({ modules: [ModuleName.STATISTICS, ModuleName.SCHEDULING] });

export async function setupGraphs(
    graphs: typeof SvelteComponentDev[],
    {
        search = "deck:current",
        days = 365,
        controller = null as typeof SvelteComponentDev | null,
    } = {},
    target: HTMLElement,
): Promise<GraphsPage> {
    checkNightMode();
    await i18n;

    return new GraphsPage({
        target,
        props: {
            initialSearch: search,
            initialDays: days,
            graphs,
            controller,
        },
    });
}

import AddedGraph from "./AddedGraph.svelte";
import ButtonsGraph from "./ButtonsGraph.svelte";
import CalendarGraph from "./CalendarGraph.svelte";
import CardCounts from "./CardCounts.svelte";
import EaseGraph from "./EaseGraph.svelte";
import FutureDue from "./FutureDue.svelte";
import { RevlogRange } from "./graph-helpers";
import HourGraph from "./HourGraph.svelte";
import IntervalsGraph from "./IntervalsGraph.svelte";
import RangeBox from "./RangeBox.svelte";
import ReviewsGraph from "./ReviewsGraph.svelte";
import TodayStats from "./TodayStats.svelte";

export function setupGraphsPage(target: HTMLElement = document.body): void {
    setupGraphs(
        [
            TodayStats,
            FutureDue,
            CalendarGraph,
            ReviewsGraph,
            CardCounts,
            IntervalsGraph,
            EaseGraph,
            HourGraph,
            ButtonsGraph,
            AddedGraph,
        ],
        {
            controller: RangeBox,
        },
        target,
    );
}

export const graphComponents = {
    TodayStats,
    FutureDue,
    CalendarGraph,
    ReviewsGraph,
    CardCounts,
    IntervalsGraph,
    EaseGraph,
    HourGraph,
    ButtonsGraph,
    AddedGraph,
    RangeBox,
    RevlogRange,
};
