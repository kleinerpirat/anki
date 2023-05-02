<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import PreviewGraph from "./PreviewGraph.svelte";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import type { MainPageArgs, StatsData } from "../types";
    import type { Writable } from "svelte/store";
    import Switch from "components/Switch.svelte";

    export let graphsData: StatsData | null;
    export let search: Writable<string>;
    export let deck: MainPageArgs["dueTree"];

    let showTotal = false;
</script>

<div class="stats">
    {#if graphsData && graphsData.sourceData && graphsData.preferences}
        <PreviewGraph
            {deck}
            {showTotal}
            sourceData={graphsData.sourceData}
            hideTitle
            on:search={(e) =>
                bridgeCommand(`browserSearch: ${$search} ${e.detail.query}`)}
        />
    {/if}

    <div class="switch">
        <Switch id="totalSwitch" label="Total" bind:value={showTotal} />
    </div>
</div>

<style lang="scss">
    .switch {
        position: absolute;
        inset: auto 0 0 auto;
    }
</style>