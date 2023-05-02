<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { Writable } from "svelte/store";
    import { writable } from "svelte/store";
    import { fly } from "svelte/transition";
    import CongratsPage from "../congrats/CongratsPage.svelte";
    import { empty, scheduler } from "@tslib/proto";

    import type { MainPageArgs, StatsData } from "../types";
    import Preview from "./Preview.svelte";
    import WithGraphData from "graphs/WithGraphData.svelte";

    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    import { marked } from "marked";

    import { bridgeCommand } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";

    import Header from "./Header.svelte";
    import Tile from "components/Tile.svelte";
    import { customStudyIcon, optionsIcon, emptyIcon, rebuildIcon } from "./icons";
    import ScrollArea from "components/ScrollArea.svelte";
    import Calendar from "./Calendar.svelte";

    export let deck: MainPageArgs["deck"];
    export let dueTree: MainPageArgs["dueTree"];

    // Search current deck node in dueTree
    function getCurrentNode(id: number, node: MainPageArgs["dueTree"]) {
        if (node.deckId == id) {
            return node;
        }
        if (node.children) {
            for (const child of node.children) {
                const match = getCurrentNode(id, child);
                if (match) {
                    return match;
                }
            }
        }
        return null;
    }
    $: currentNode = getCurrentNode(deck.id, dueTree);

    export let graphsData: StatsData | null;
    export let search: Writable<string>;

    $: descriptionText = deck.description;

    let editing = false;

    function stripHTML(str: string) {
        const el = document.createElement("div");
        el.innerHTML = str;
        return el.innerText;
    }

    $: if (!editing && descriptionText !== deck.description) {
        bridgeCommand(
            `description:${deck.markdownDescription}:${
                deck.markdownDescription ? stripHTML(descriptionText) : descriptionText
            }`,
        );
    }

    let descriptionOverflowing = false;
    let cutDescription = true;

    function checkForOverflow(e: Event) {
        const el = e.target as HTMLElement;
        descriptionOverflowing = el.scrollHeight > el.offsetHeight;
    }
</script>

<div class="overview" class:rtl transition:fly={{ x: 500 }}>
    <div class="deck">
        <Header
            name={deck.name}
            hasDescription={descriptionText !== ""}
            {dueTree}
            bind:editing
        />
        {#if deck.url}
            <a href={deck.url}>{tr.decksReviewsAndUpdates()}</a>
        {/if}

        <div
            class="description"
            class:dyn={deck.isDyn}
            class:editing
            class:cut-description={cutDescription}
        >
            {#if deck.isDyn}
                <p>
                    {tr.studyingThisIsASpecialDeckFor()}
                    {tr.studyingCardsWillBeAutomaticallyReturnedTo()}
                    {tr.studyingDeletingThisDeckFromTheDeck()}
                </p>
            {:else}
                <div
                    class="description-content"
                    class:has-overflow={descriptionOverflowing}
                    on:resize={checkForOverflow}
                >
                    <ScrollArea>
                        <div class="description-text">
                            {@html deck.markdownDescription
                                ? marked(descriptionText)
                                : descriptionText}
                        </div>
                    </ScrollArea>
                </div>
                {#if editing}
                    <textarea
                        bind:value={descriptionText}
                        placeholder={deck.markdownDescription
                            ? tr.deckConfigEnterDescriptionInMarkdown()
                            : tr.deckConfigEnterDescriptionInHtml()}
                    />
                {/if}
                {#if editing}
                    <div class="description-ui">
                        <div>
                            <label
                                for="md-checkbox"
                                title={tr.deckConfigDescriptionNewHandlingHint()}
                            >
                                {tr.deckConfigDescriptionNewHandling()}
                            </label>
                            <input
                                id="md-checkbox"
                                type="checkbox"
                                bind:checked={deck.markdownDescription}
                            />
                        </div>
                    </div>
                {/if}
            {/if}

            {#if !editing}
                <div class="preview">
                    {#if deck.finished}
                        {#await scheduler.congratsInfo(empty) then info}
                            <CongratsPage {info} />
                        {/await}
                    {:else}
                        <Preview deck={currentNode} {graphsData} {search} />
                    {/if}
                </div>
            {/if}
        </div>
    </div>
    <div class="calendar">
        <WithGraphData
            search={writable("*")}
            days={writable(0)}
            let:sourceData
            let:preferences
            let:revlogRange
        >
            <Calendar graphsData={{ sourceData, preferences, revlogRange }} {search} />
        </WithGraphData>
    </div>

    <div class="actions">
        <div class="center">
            <Tile
                size={64}
                icon={optionsIcon}
                tooltip={tr.actionsOptions()}
                on:click={() => bridgeCommand("opts")}
                on:action={() => bridgeCommand("opts")}
            />
            {#if deck.isDyn}
                <Tile
                    size={64}
                    icon={rebuildIcon}
                    tooltip={tr.actionsRebuild()}
                    shortcut="R"
                    on:click={() => bridgeCommand("refresh")}
                    on:action={() => bridgeCommand("refresh")}
                />
                <Tile
                    size={64}
                    icon={emptyIcon}
                    tooltip={tr.studyingEmpty()}
                    shortcut="E"
                    on:click={() => bridgeCommand("empty")}
                    on:action={() => bridgeCommand("empty")}
                />
            {:else}
                <Tile
                    size={64}
                    icon={customStudyIcon}
                    tooltip={tr.actionsCustomStudy()}
                    on:click={() => bridgeCommand("customStudy")}
                    on:action={() => bridgeCommand("customStudy")}
                />
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;
    @use "sass/breakpoints" as *;

    .overview {
        height: 100%;
        position: relative;
        display: grid;
        overflow: hidden;
        padding-top: 2rem;
        align-content: center;
        justify-content: center;
        grid-template:
            "deck actions" 75%
            "calendar actions" 25% / 1fr min-content;

        .deck {
            grid-area: deck;
        }
        .calendar {
            max-width: 720px;
            grid-area: calendar;
        }
    }

    .description {
        width: 800px;
        @media only screen and (max-width: 800px) {
            width: 100%;
        }
        padding-inline: props.$border-radius-large;
        display: grid;
        grid-template:
            "text" 1fr
            "preview" min-content / 1fr;

        backdrop-filter: blur(props.$blur);
        border-radius: props.$border-radius-large;
        @include elevation(3);

        &.editing {
            color: colors.$fg-subtle;
            display: grid;
            grid-gap: 2em;
            grid-template:
                "input text" 9fr
                "ui ui" 1fr / 1fr 1fr;

            .description-content {
                backdrop-filter: blur(props.$blur);
                border: 1px solid colors.$border-subtle;
                border-radius: props.$border-radius;
            }
        }

        .description-content {
            grid-area: text;
            padding: 0.5em 0.75em;
            line-height: 1.2;
            overflow: hidden;
            position: relative;
            display: flex;
        }

        &.cut-description {
            max-height: 60vh;
        }
        textarea {
            grid-area: input;
            padding: 0.5em 0.75em;
            color: colors.$fg;
            background: colors.$glass;
            backdrop-filter: blur(props.$blur);
            border-radius: props.$border-radius;
        }

        .description-ui {
            grid-area: ui;
            display: flex;
            width: 100%;
            justify-content: space-between;
            color: colors.$fg;
        }
    }

    .preview {
        grid-area: preview;
    }

    .actions {
        grid-area: actions;
        display: flex;
        flex-direction: column;
        justify-content:center;

        .center {
            background-color: colors.$glass;
            backdrop-filter: blur(props.$blur);
            @include elevation(4);
            border-top-left-radius: props.$border-radius-medium;
            border-bottom-left-radius: props.$border-radius-medium;
        }
    }
</style>
