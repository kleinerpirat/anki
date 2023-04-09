<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { MainViewMode } from "./types";
    import type { DeckBrowserArgs, OverviewArgs, ReviewerArgs } from "./types";
    import type { ToolbarArgs } from "./toolbar/types";
    import Overview from "./overview/Overview.svelte";
    import UpgradeMessage from "./UpgradeMessage.svelte";
    import DeckBrowser from "./deck-browser/DeckBrowser.svelte";
    import Reviewer from "../reviewer/Reviewer.svelte";
    import ScrollArea from "../components/ScrollArea.svelte";
    import Toolbar from "./toolbar/Toolbar.svelte";
    import CustomStudyMenu from "./custom-study/CustomStudyMenu.svelte";

    export let mode: MainViewMode = MainViewMode.OVERVIEW;
    export let deckBrowserArgs: DeckBrowserArgs;
    export let overviewArgs: OverviewArgs;
    export let toolbarArgs: ToolbarArgs;
    export let reviewerArgs: ReviewerArgs;

    export let decksCollapsed: boolean;
    export let serverURL: string;

    let toolbar: Toolbar;
    let overview: Overview;

    // Execute addon scripts inserted via HTML
    function loadAddonScripts(el: HTMLDivElement) {
        Array.from(document.body.querySelectorAll("script")).forEach((script) => {
            const newScript = document.createElement("script");
            Array.from(script.attributes).forEach((attr) => {
                newScript.setAttribute(attr.name, attr.value);
            });
            newScript.text = script.text;
            script.parentNode?.removeChild(script);
            el.appendChild(newScript);
        });
    }

    $: decksCollapsed = [
        MainViewMode.DECK_OPTIONS,
        MainViewMode.STATS,
        MainViewMode.REVIEW,
        MainViewMode.CUSTOM_STUDY,
    ].includes(mode);

    let deckContainer: HTMLDivElement;
    function collapseDecksOnClickOutside(e: MouseEvent) {
        decksCollapsed = !deckContainer.contains(e.target as HTMLElement);
    }

    function handleDeckTab(e: CustomEvent) {
        e.detail.shiftKey ? toolbar.focus() : overview.focus();
    }
</script>

<div hidden use:loadAddonScripts />

<Toolbar {toolbarArgs} {decksCollapsed} bind:this={toolbar} collapsed={false} />

<div
    class="main-page"
    class:decks-expanded={!decksCollapsed}
    class:deck-options={mode === MainViewMode.DECK_OPTIONS}
    class:stats={mode === MainViewMode.STATS}
    class:review={mode === MainViewMode.REVIEW}
    on:click={collapseDecksOnClickOutside}
>
    <ScrollArea>
        {#if deckBrowserArgs.schedulerVersion == 1}
            <UpgradeMessage />
        {/if}

        <div bind:this={deckContainer}>
            <DeckBrowser
                {deckBrowserArgs}
                {decksCollapsed}
                on:tab={handleDeckTab}
            />
        </div>

        {#if mode === MainViewMode.REVIEW}
            <Reviewer {reviewerArgs} {serverURL} />
        {:else if mode === MainViewMode.OVERVIEW}
            <Overview {overviewArgs} bind:this={overview} />

            <div id="studiedToday"><span>{deckBrowserArgs.studiedToday}</span></div>
        {:else if mode === MainViewMode.CUSTOM_STUDY}
            <CustomStudyMenu />
        {/if}
    </ScrollArea>
</div>

{#if mode === MainViewMode.DECK_OPTIONS}
    <div id="deckOptions" />
{/if}
{#if mode === MainViewMode.STATS}
    <div id="stats" />
{/if}

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;

    .main-page {
        height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
        position: relative;
        transition: padding props.$transition-medium;
        &.decks-expanded,
        &.deck-options,
        &.stats {
            padding-left: 540px;
        }
        &.deck-options,
        &.stats {
            padding-left: -100vw;
            padding-right: 100vw;
        }
    }

    @keyframes slide-from-right {
        from {
            left: 100vw;
        }
        to {
            left: 0;
        }
    }

    #deckOptions,
    #stats {
        width: 100vw;
        position: fixed;
        z-index: 1;
        top: 0;
        bottom: 0;
    }
    #deckOptions,
    #stats {
        animation: slide-from-right props.$transition-medium;
    }

    #studiedToday {
        position: absolute;
        right: 1em;
        bottom: 0;
    }
</style>
