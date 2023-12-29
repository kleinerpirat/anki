<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { debounce } from "lodash-es";

    import { MainPageContext } from "../types";
    import type { MainPageArgs } from "../types";
    import type { Deck } from "../types";
    import * as tr2 from "@tslib/ftl";
    import DeckRow from "./DeckRow.svelte";
    import ScrollArea from "components/ScrollArea.svelte";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import {
        createIcon,
        getSharedIcon,
        importFileIcon,
        learnIcon,
        newIcon,
        reviewIcon,
    } from "main/icons";
    import Badge from "components/Badge.svelte";

    import { mwContext } from "../lib";

    export let deck: MainPageArgs["deck"];
    export let dueTree: MainPageArgs["dueTree"];

    let filteredDecks: Deck[];

    $: filtered = searchTerm !== "";
    $: if (filtered) {
        filteredDecks = filterDecksByName(dueTree.children, searchTerm) as Deck[];
    }

    let searchTerm = "";

    const debounceSearch = debounce((value) => {
        searchTerm = value;
    }, 150);

    function handleSearchInput(event: Event) {
        const value = (event.target as HTMLInputElement).value.trim();
        debounceSearch(value);
    }

    function filterDecksByName(decks: any[], name: string): Deck[] {
        return decks.map((deck) => {
            const children = filterDecksByName(deck.children || [], name);

            return {
                ...deck,
                matched: deck.name.toLowerCase().includes(name.toLowerCase()),
                containsMatch: children.some(
                    (child) => child.matched || child.containsMatch,
                ),
                children,
            };
        });
    }

    let input: HTMLInputElement;
    let inputFocused = false;

    export function focusSearch(): void {
        input.focus();
    }
    let headerHeight: number;

    $: minimized = [
        MainPageContext.STATS,
        MainPageContext.DECK_OPTIONS,
        MainPageContext.CUSTOM_STUDY,
    ].includes($mwContext);
</script>

<div class="deck-browser" class:minimized>
    <ScrollArea --inset-top="{headerHeight}px">
        <table>
            <thead bind:clientHeight={headerHeight}>
                <tr>
                    <th colspan={inputFocused || minimized ? 5 : 3}>
                        <div class="search">
                            <input
                                type="text"
                                placeholder="Search deck"
                                on:focusin={() => (inputFocused = true)}
                                on:focusout={() => (inputFocused = false)}
                                on:input={handleSearchInput}
                                bind:this={input}
                            />

                            <Badge
                                iconSize={100}
                                tooltip={tr2.decksSearchAnkiweb()}
                                on:click={() =>
                                    bridgeCommand(
                                        `shared:${encodeURIComponent(searchTerm)}`,
                                    )}
                            >
                                {@html getSharedIcon}
                            </Badge>
                        </div>
                    </th>
                    {#if !minimized}
                        {#if !inputFocused}
                            <th>
                                <Badge
                                    iconSize={100}
                                    tooltip={tr2.decksImportFile()}
                                    on:click={() => bridgeCommand("import")}
                                >
                                    {@html importFileIcon}
                                </Badge>
                            </th>
                            <th>
                                <Badge
                                    iconSize={100}
                                    tooltip={tr2.decksCreateDeck()}
                                    on:click={() => bridgeCommand("create")}
                                >
                                    {@html createIcon}
                                </Badge>
                            </th>
                        {/if}
                        <th class="new">
                            <Badge
                                tooltip={tr2.schedulingNewCards()}
                                on:click={(e) => bridgeCommand("browserSearch:is:new")}
                            >
                                {@html newIcon}
                            </Badge>
                        </th>
                        <th class="learn">
                            <Badge
                                tooltip={tr2.schedulingLearning()}
                                on:click={(e) =>
                                    bridgeCommand("browserSearch:is:learn")}
                            >
                                {@html learnIcon}
                            </Badge>
                        </th>
                        <th class="review">
                            <Badge
                                tooltip={tr2.schedulingReview()}
                                on:click={(e) =>
                                    bridgeCommand("browserSearch:is:review")}
                            >
                                {@html reviewIcon}
                            </Badge>
                        </th>
                    {/if}
                </tr>
            </thead>
            <tbody>
                {#if filtered}
                    {#each filteredDecks as node}
                        <DeckRow filtered {minimized} {node} />
                    {/each}
                {:else}
                    {#each dueTree.children as node}
                        <DeckRow
                            {node}
                            {minimized}
                            current={node.deckId == deck.id}
                            on:tab
                        />
                    {/each}
                {/if}
            </tbody>
        </table>
    </ScrollArea>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;

    .deck-browser {
        height: 100%;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background: colors.$glass;
        backdrop-filter: blur(props.$blur);

        @include elevation(4, $opacity-boost: -0.08);
        &:hover {
            @include elevation(4);
        }

        &.minimized {
            .search {
                border: none;
            }
        }
    }

    table {
        table-layout: fixed;
        width: 100%;
        position: relative;
        border-collapse: collapse;
        padding: 0;

        thead {
            position: sticky;
            top: 0;
            border-bottom: 1px solid colors.$border-subtle;
            background: colors.$canvas;
            z-index: 2;
        }

        th {
            padding-block: 0;
            text-align: center;

            &:first-child {
                text-align: start;
                white-space: nowrap;
                // border separating deck names from counts
                position: relative;
            }
            &:last-child {
                padding-right: 0.5em;
            }

            &.new {
                color: colors.$card-new;
            }
            &.learn {
                color: colors.$card-learn;
            }
            &.review {
                color: colors.$card-review;
            }
        }
    }

    .search {
        display: flex;
    }
    .search {
        padding-block: 5px;
        background-color: colors.$input-bg;
        padding-inline-end: 0.5rem;
        border-inline-end: 1px solid colors.$border;
        justify-content: space-between;
        input {
            padding-block: 0;
            min-width: 0;
            border: none;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
    }
</style>
