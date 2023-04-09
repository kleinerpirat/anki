<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { writable } from "svelte/store";
    import CardCounts from "../../graphs/CardCounts.svelte";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import WithGraphData from "graphs/WithGraphData.svelte";

    export let deckName: string;
    export let interval: number;

    const search = writable("");
    const days = writable(0);

    $: $search = `deck:"${deckName}"`;
    $: $days = interval;
</script>

<div class="stats">
    <WithGraphData {search} {days} let:sourceData let:preferences let:revlogRange>
        {#if sourceData && preferences && revlogRange}
            <CardCounts
                {sourceData}
                {preferences}
                on:search={(e) =>
                    bridgeCommand(`browserSearch: ${$search} ${e.detail.query}`)}
            />
        {/if}
    </WithGraphData>
</div>
