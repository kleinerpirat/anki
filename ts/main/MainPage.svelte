<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { writable } from "svelte/store";

    import { MainPageContext } from "./types";
    import type { MainPageArgs, MainPageComponents } from "./types";
    import type { ReviewerArgs } from "../reviewer-iframe/types";
    import OverviewPage from "./overview/OverviewPage.svelte";
    import UpgradeMessage from "./UpgradeMessage.svelte";
    import DeckBrowser from "./deck-browser/DeckBrowser.svelte";
    import ReviewerFrame from "../reviewer-iframe/ReviewerFrame.svelte";
    import Toolbar from "./toolbar/Toolbar.svelte";
    import CustomStudyPage from "./custom-study/CustomStudyPage.svelte";
    import StatusBar from "./status-bar/StatusBar.svelte";
    import WithGraphData from "graphs/WithGraphData.svelte";
    import ExternalPage from "./ExternalPage.svelte";
    import { backIcon } from "./icons";
    import Badge from "components/Badge.svelte";
    import { mwContext } from "./lib";
    import ProfileSelector from "./status-bar/ProfileSelector.svelte";
    import StudiedToday from "./StudiedToday.svelte";
    import { Decks } from "@tslib/proto";
    import { id } from "@tslib/functional";

    export let mode: MainPageContext = MainPageContext.HOME;
    export let args: MainPageArgs;
    export let reviewerArgs: ReviewerArgs;

    export let decksCollapsed: boolean;
    export let refreshNeeded = false;

    $: $mwContext = mode;

    // Collapse deck browser by default in certain modes
    $: decksCollapsed = [MainPageContext.REVIEW, MainPageContext.CUSTOM_STUDY].includes(
        $mwContext,
    );

    let reviewer: ReviewerFrame;
    export function getReviewer(): ReviewerFrame | null {
        return reviewer;
    }

    let toolbar: Toolbar;
    let deckBrowser: DeckBrowser;
    let statusBar: StatusBar;

    export function getComponents(): MainPageComponents {
        return { toolbar, deckBrowser, statusBar };
    }

    // Data required for graphs
    const search = writable("");
    const days = writable(1);
    $: $search = `deck:"${args.deck.name}"`;
</script>

<WithGraphData {search} {days} let:sourceData let:preferences let:revlogRange>
    {#if args.schedulerVersion == 1}
        <UpgradeMessage />
    {/if}
    <div
        class="main-page"
        class:decks-collapsed={decksCollapsed}
        class:refresh-needed={refreshNeeded}
        class:deck-options={$mwContext === MainPageContext.DECK_OPTIONS}
        class:stats={$mwContext === MainPageContext.STATS}
        class:review={$mwContext === MainPageContext.REVIEW}
    >
        <div class="toolbar">
            <Toolbar
                addonContent={args.addonContent.toolbar}
                {decksCollapsed}
                collapsed={false}
                bind:this={toolbar}
            />
        </div>
        <div class="decks">
            <DeckBrowser
                deck={args.deck}
                dueTree={args.dueTree}
                bind:this={deckBrowser}
            />
        </div>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div class="main-area">
            {#if $mwContext === MainPageContext.REVIEW}
                <ReviewerFrame bind:this={reviewer} {reviewerArgs} />
            {:else if $mwContext === MainPageContext.HOME}
                <OverviewPage
                    {search}
                    addonContent={args.addonContent.overview}
                    deck={args.deck}
                    dueTree={args.dueTree}
                    graphsData={{ sourceData, preferences, revlogRange }}
                />
            {:else if $mwContext === MainPageContext.CUSTOM_STUDY}
                <CustomStudyPage />
            {/if}
            <ExternalPage />
        </div>
        <StatusBar addonContent={args.addonContent.statusBar} bind:this={statusBar}>
            <ProfileSelector profiles={args.profiles} slot="left-tray" />
            <StudiedToday {sourceData} slot="center-tray" />
        </StatusBar>
    </div>
</WithGraphData>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    .main-page {
        height: 100vh;
        width: 100vw;
        display: grid;
        grid-template:
            "decks toolbar" min-content
            "decks main" 1fr
            "status status" min-content / minmax(320px, 400px) 1fr;

        transition: all props.$transition ease-out;

        &.decks-collapsed {
            grid-template-columns: 0 1fr;
        }
        &.deck-options,
        &.stats {
            // hide toolbar
            grid-template-rows: 0 1fr min-content;
            // reduce deck browser width
            grid-template-columns: 320px 1fr;
        }

        @media (max-width: 680px) {
            grid-template-areas:
                "toolbar toolbar"
                "decks main"
                "status status";
            // show either deck browser or overview
            grid-template-columns: 1fr 0;
            &.decks-collapsed {
                grid-template-columns: 0 1fr;
            }
            --MainPage-toolbar-bg: #{colors.$canvas};
        }
        position: relative;

        .toolbar {
            grid-area: toolbar;
            z-index: 100;
        }
        .decks {
            grid-area: decks;
            z-index: 100;
        }
        .main-area {
            grid-area: main;
        }
    }
</style>
