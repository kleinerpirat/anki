<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { timeHour, timeYear, timeDay } from "d3";
    import * as tr from "@tslib/ftl";
    import type { Stats } from "@tslib/proto";
    import { createEventDispatcher } from "svelte";
    import CalHeatmap from "cal-heatmap";
    import { hideTooltip, showTooltip } from "./tooltip";
    import { pointer } from "d3";
    import { localizedDate } from "@tslib/i18n";

    import type { PreferenceStore } from "../sveltelib/preferences";
    import type { GraphData } from "./calendar";
    import { gatherData, renderCalendar } from "./calendar";
    import Graph from "./Graph.svelte";
    import type { SearchEventMap } from "./graph-helpers";
    import { defaultGraphBounds, RevlogRange } from "./graph-helpers";
    import InputBox from "./InputBox.svelte";

    export let sourceData: Stats.GraphsResponse;
    export let preferences: PreferenceStore<Stats.GraphPreferences>;
    export let revlogRange: RevlogRange;
    export let nightMode: boolean;
    export let hideTitle = false;

    const { calendarFirstDayOfWeek } = preferences;
    const dispatch = createEventDispatcher<SearchEventMap>();

    let graphData: GraphData | null = null;

    const bounds = defaultGraphBounds();
    bounds.height = 120;
    bounds.marginLeft = 20;
    bounds.marginRight = 20;

    let svg = null as HTMLElement | SVGElement | null;
    const maxYear = new Date().getFullYear();
    let minYear = 0;
    let targetYear = maxYear;

    $: if (sourceData) {
        graphData = gatherData(sourceData, $calendarFirstDayOfWeek);
    }

    $: {
        if (revlogRange < RevlogRange.Year) {
            minYear = maxYear;
        } else if ((revlogRange as RevlogRange) === RevlogRange.Year) {
            minYear = maxYear - 1;
        } else {
            minYear = 2000;
        }
        if (targetYear < minYear) {
            targetYear = minYear;
        }
    }

    let cal: CalHeatmap;

    function createCalHeatmap(): void {
        cal = new CalHeatmap();
        cal.on(
            "mouseover",
            // @ts-ignore
            (event: PointerEvent, timestamp: number, count: number) => {
                const [x, y] = pointer(event, document.body);
                const time = new Date(timestamp);
                const offsetTimestamp = timeHour.offset(
                    time,
                    time.getTimezoneOffset() / 60,
                );
                showTooltip(tooltipText(offsetTimestamp.getTime()), x, y);
            },
        );
        cal.on(
            "click",
            // @ts-ignore
            (_event: PointerEvent, timestamp: number, count: number) => {
                if (count > 0) {
                    const d = timestampMap[timestamp];
                    dispatch("search", { query: `"prop:rated=${d.day}"` });
                }
            },
        );
        cal.on("minDateReached", () => (prevDisabled = true));
        cal.on("maxDateReached", () => (nextDisabled = true));
        cal.on("minDateNotReached", () => (prevDisabled = false));
        cal.on("maxDateNotReached", () => (nextDisabled = false));
    }

    interface DayDatum {
        day: number;
        count: number;
        // 0-51
        weekNumber: number;
        // 0-6
        weekDay: number;
        date: Date;
    }

    function tooltipText(timestamp: number): string {
        const timestampDate = new Date(timestamp);
        const d = timestampMap.get(timestamp);
        const date = localizedDate(timestampDate, {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
        });
        const cards = tr.statisticsReviews({ reviews: d ? d.count : 0 });
        return `${date}<br>${cards}`;
    }

    let prevDisabled = false;
    let nextDisabled = false;

    let timestampMap: Map<number, DayDatum>;

    $: if (graphData) {
        const { map, maxCount } = renderCalendar(graphData, targetYear, revlogRange);
        timestampMap = map;

        const calHeatmapData: { timestamp: number; count: number }[] = [];
        for (const [timestamp, datum] of timestampMap.entries()) {
            calHeatmapData.push({ timestamp: timestamp, count: datum.count });
        }

        if (!cal) {
            createCalHeatmap();
        }
        cal.paint({
            data: {
                // @ts-ignore
                source: calHeatmapData,
                x: "timestamp",
                y: "count",
                defaultValue: 0,
            },
            range: 12,
            date: {
                min: new Date(minYear, 0),
                max: new Date(maxYear, 11),
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            },
            scale: {
                opacity: {
                    baseColor: "blue",
                    domain: [0, maxCount + 1],
                },
            },
            domain: {
                type: "month",
            },
            subDomain: { type: "day", radius: 2 },
            // @ts-ignore
            itemSelector: svg,
            theme: nightMode ? "dark" : "light",
        });
    }

    const title = tr.statisticsCalendarTitle();

    function previous(): void {
        targetYear--;
        cal.previous();
    }
    function next(): void {
        targetYear++;
        cal.next();
    }
</script>

<Graph {title} {hideTitle}>
    <InputBox>
        <span>
            <button on:click={() => previous()}> ◄ </button>
        </span>
        <span>{targetYear}</span>
        <span>
            <button on:click={() => next()}> ► </button>
        </span>
    </InputBox>

    <svg
        class="heatmap"
        bind:this={svg}
        viewBox={`0 0 ${bounds.width} ${bounds.height}`}
        on:mouseleave={hideTooltip}
    />
</Graph>

<style lang="scss">
    @use "sass/colors";
    @import "cal-heatmap/cal-heatmap.css";

    :global(svg.heatmap .ch-subdomain-bg) {
        stroke: colors.$shadow;
        stroke-width: 1px;
    }
</style>
