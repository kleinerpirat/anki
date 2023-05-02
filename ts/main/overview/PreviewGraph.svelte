<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import type { Stats } from "@tslib/proto";
    import { createEventDispatcher } from "svelte";

    import type { GraphData, TableDatum, TableData } from "./preview";
    import { gatherData, renderPreview } from "./preview";
    import Graph from "../../graphs/Graph.svelte";
    import type { SearchEventMap } from "../../graphs/graph-helpers";
    import { defaultGraphBounds } from "../../graphs/graph-helpers";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import Tile from "components/Tile.svelte";
    import StudyIcon from "./StudyIcon.svelte";
    import type { MainPageArgs } from "../types";

    export let deck: MainPageArgs["dueTree"];
    export let sourceData: Stats.GraphsResponse;
    export let hideTitle = false;
    export let showTotal = false;

    const dispatch = createEventDispatcher<SearchEventMap>();

    let svg = null as HTMLElement | SVGElement | null;

    const bounds = defaultGraphBounds();
    bounds.width = 225;
    bounds.marginBottom = 0;

    let graphData = null as unknown as GraphData;
    let tableData = null as unknown as TableData;

    $: {
        graphData = gatherData(sourceData);
        tableData = renderPreview(svg as any, bounds, graphData);
    }

    $: hideSum =
        (showTotal
            ? Object.values(tableData).filter((d) => d.count > 0).length
            : [deck.newCount, deck.learnCount, deck.reviewCount].filter(
                  (c) => c !== undefined,
              ).length) <= 1;

    const total = tr.statisticsCountsTotalCards();

    $: if (showTotal) {
        renderPreview(svg as any, bounds, graphData);
    }

    const suffix = 'AND -("is:buried" OR "is:suspended")';
</script>

<Graph title="" {hideTitle}>
    <div class="counts-outer">
        {#if tableData}
            <div class="counts-table">
                <table>
                    <tr hidden={showTotal ? tableData.new.count === 0 : !deck.newCount}>
                        <td>
                            <span style="color: {tableData.new.color};">■&nbsp;</span>
                            <span
                                class="search-link"
                                on:click={() =>
                                    dispatch("search", { query: `"is:new" ${suffix}` })}
                            >
                                {showTotal
                                    ? tableData.new.label
                                    : tr.statisticsCountsNewCards()}
                            </span>
                        </td>
                        <td class="right">
                            {showTotal ? tableData.new.count : deck.newCount}
                        </td>
                    </tr>
                    <tr
                        hidden={showTotal
                            ? tableData.learn.count === 0
                            : !deck.learnCount}
                    >
                        <td>
                            <span style="color: {tableData.learn.color};">■&nbsp;</span>
                            <span
                                class="search-link"
                                on:click={() =>
                                    dispatch("search", {
                                        query: `(${
                                            showTotal ? `-"is:review" AND ` : ""
                                        }is:learn) ${suffix}`,
                                    })}
                            >
                                {showTotal
                                    ? tableData.learn.label
                                    : tr.statisticsCountsLearningCards()}
                            </span>
                        </td>
                        <td class="right">
                            {showTotal ? tableData.learn.count : deck.learnCount}
                        </td>
                    </tr>
                    <tr hidden={!showTotal || tableData.relearn.count === 0}>
                        <td>
                            <span style="color: {tableData.relearn.color};"
                                >■&nbsp;</span
                            >
                            <span
                                class="search-link"
                                on:click={() =>
                                    dispatch("search", {
                                        query: `("is:review" AND "is:learn") ${suffix}`,
                                    })}
                            >
                                {tableData.relearn.label}
                            </span>
                        </td>
                        <td class="right">{tableData.relearn.count}</td>
                    </tr>
                    <tr hidden={!showTotal || tableData.young.count === 0}>
                        <td>
                            <span style="color: {tableData.young.color};">■&nbsp;</span>
                            <span
                                class="search-link"
                                on:click={() =>
                                    dispatch("search", {
                                        query: `("is:review" AND -"is:learn") AND "prop:ivl<21" ${suffix}`,
                                    })}
                            >
                                {tableData.young.label}
                            </span>
                        </td>
                        <td class="right">{tableData.young.count}</td>
                    </tr>
                    <tr
                        hidden={showTotal
                            ? tableData.mature.count === 0
                            : !deck.reviewCount}
                    >
                        <td>
                            <span style="color: {tableData.mature.color};">■&nbsp;</span
                            >
                            <span
                                class="search-link"
                                on:click={() =>
                                    dispatch("search", {
                                        query: `("is:review" -"is:learn")${
                                            showTotal ? ` AND "prop:ivl>=21"` : ""
                                        } ${suffix}`,
                                    })}
                            >
                                {showTotal
                                    ? tableData.mature.label
                                    : tr.statisticsCountsReviewCards()}
                            </span>
                        </td>
                        <td class="right">
                            {showTotal ? tableData.mature.count : deck.reviewCount}
                        </td>
                    </tr>
                    <tr class="total" hidden={hideSum}>
                        <td class="right">{total}</td>
                        <td class="right">
                            {showTotal
                                ? graphData.totalCards
                                : (deck.newCount ?? 0) +
                                  (deck.learnCount ?? 0) +
                                  (deck.reviewCount ?? 0)}
                        </td>
                    </tr>
                </table>
            </div>
        {/if}

        <div class="tile">
            {#if showTotal}
                <div class="pie-chart">
                    <svg
                        bind:this={svg}
                        viewBox={`0 0 ${bounds.width} ${bounds.height}`}
                        style="opacity: {graphData.totalCards ? 1 : 0}"
                    >
                        <g class="counts" class:stroke={!hideSum} />
                    </svg>
                </div>
            {:else}
                <div class="study-button">
                    <Tile
                        text={tr.decksStudy()}
                        on:click={() => bridgeCommand("study")}
                    >
                        <StudyIcon {deck} slot="icon" />
                    </Tile>
                </div>
            {/if}
        </div>
    </div>
</Graph>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    svg {
        transition: opacity props.$transition-slow;

        g.counts.stroke {
            stroke: colors.$shadow;
            stroke-width: 1px;
        }
    }

    .counts-outer {
        display: flex;
        justify-content: center;
        margin: 0 4vw;
        flex-wrap: wrap;
        flex: 1;

        .tile {
            display: grid;
            align-items: center;
            justify-items: center;

            .pie-chart {
                width: 200px;
                margin: 0;
                padding: 0;
                transition: transform props.$transition;
            }
        }

        .counts-table {
            display: flex;
            flex-direction: column;
            justify-content: center;

            table {
                border-spacing: 1em 0;
                padding-left: 4vw;

                td {
                    white-space: nowrap;
                    padding: 5px min(4vw, 40px);

                    &.right {
                        text-align: right;
                    }
                }
                tr.total {
                    > td {
                        margin-top: 10px;
                        border-top: 1px solid colors.$border-subtle;
                    }
                }
            }
        }
    }

    .search-link:hover {
        cursor: pointer;
        color: colors.$link;
        text-decoration: underline;
    }
</style>
