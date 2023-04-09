<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { fly } from "svelte/transition";
    import CongratsPage from "../congrats/CongratsPage.svelte";
    import { empty, scheduler } from "@tslib/proto";

    import { bridgeCommand } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";
    import type { OverviewArgs } from "../types";
    import Container from "../../components/Container.svelte";
    import Shortcut from "../../components/Shortcut.svelte";
    import DeckDescription from "./DeckDescription.svelte";
    import DeckStats from "./DeckStats.svelte";

    let args: OverviewArgs;
    export { args as overviewArgs };

    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    $: isDyn = args.deck.isDyn;
</script>

<div class="deck-overview" class:rtl transition:fly={{ x: 500 }}>
    <Container breakpoint="md">
        {#if args.deck.url}
            <a href={args.deck.url}>Reviews and Updates</a>
        {/if}

        <DeckDescription
            descriptionText={args.deck.description}
            markdown={args.markdown}
            {isDyn}
        />
        {#if isDyn}
            <Shortcut keyCombination="R" on:action={() => bridgeCommand("refresh")} />
            <button on:click={() => bridgeCommand("refresh")}>
                {tr.actionsRebuild()}
            </button>

            <Shortcut keyCombination="E" on:action={() => bridgeCommand("empty")} />
            <button on:click={() => bridgeCommand("empty")}>
                {tr.studyingEmpty()}
            </button>
        {:else}
            <button on:click={() => bridgeCommand("customStudy")}>
                {tr.actionsCustomStudy()}
            </button>
        {/if}
    </Container>

    {#if args.deck.finished}
        {#await scheduler.congratsInfo(empty) then info}
            <CongratsPage {info} />
        {/await}
    {:else}
        <button class="btn-primary" on:click={() => bridgeCommand("study")}>
            Study
        </button>

        <DeckStats deckName={args.deck.name} interval={args.days} />
    {/if}
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/button-mixins" as button;

    .deck-overview {
        margin-top: 2em;
        width: 100%;
        text-align: center;
        align-items: center;
        justify-content: center;

        > :global(*) {
            text-align: start;
            max-width: 65em;
            margin: 0 auto 1em auto;
        }
    }
</style>
