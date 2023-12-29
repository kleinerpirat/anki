<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import CalendarGraph from "../../graphs/CalendarGraph.svelte";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import type { StatsData } from "../types";
    import type { Writable } from "svelte/store";
    import { pageTheme } from "sveltelib/theme";

    export let graphsData: StatsData | null;
    export let search: Writable<string>;
</script>

<div class="calendar">
    {#if graphsData && graphsData.sourceData && graphsData.preferences}
        <CalendarGraph
            sourceData={graphsData.sourceData}
            preferences={graphsData.preferences}
            revlogRange={graphsData.revlogRange}
            nightMode={$pageTheme.isDark}
            hideTitle
            on:search={(e) =>
                bridgeCommand(`browserSearch: ${$search} ${e.detail.query}`)}
        />
    {/if}
</div>

<style lang="scss">
    @use "sass/props";
    @use "sass/elevation" as *;

    .calendar {
        padding: 0.5em 1em;
        backdrop-filter: blur(props.$blur);
        border-top-left-radius: props.$border-radius-large;
        border-top-right-radius: props.$border-radius-large;
        @include elevation(3);
    }
</style>
