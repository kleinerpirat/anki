<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { debounce } from "lodash-es";

    import type { DeckBrowserArgs, FilteredDeckTree } from "../types";
    import * as tr2 from "@tslib/ftl";
    import Deck from "./Deck.svelte";
    import MatchedDeck from "./MatchedDeck.svelte";
    import { Decks } from "@tslib/proto";
    import ScrollArea from "components/ScrollArea.svelte";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import ButtonToolbar from "components/ButtonToolbar.svelte";
    import IconButton from "components/IconButton.svelte";
    import { createIcon, getSharedIcon, importFileIcon } from "main/icons";
    import IconConstrain from "components/IconConstrain.svelte";

    let args: DeckBrowserArgs;
    export { args as deckBrowserArgs };

    export let decksCollapsed: boolean;

    $: dueTree = Decks.DeckTreeNode.toObject(args.dueTree);
    let filteredDecks: FilteredDeckTree[];

    $: filtered = searchTerm !== "";
    $: if (filtered) {
        filteredDecks = filterDecksByName(dueTree.children, searchTerm);
    }

    $: searchTerm = args.searchTerm;

    const debounceSearch = debounce((value) => {
        searchTerm = value;
    }, 150);

    function handleSearchInput(event: Event) {
        const value = (event.target as HTMLInputElement).value.trim();
        debounceSearch(value);
    }

    function filterDecksByName(decks: any[], name: string): FilteredDeckTree[] {
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
    let headerHeight: number;
</script>

<div class="deck-browser" class:collapsed={decksCollapsed}>
    <ScrollArea --inset-top="{headerHeight}px">
        <table>
            <thead bind:clientHeight={headerHeight}>
                <tr>
                    <th class="input" colspan="3">
                        <input
                            type="text"
                            placeholder="Search deck"
                            on:input={handleSearchInput}
                            bind:this={input}
                        />
                        <span
                            class="search-icon"
                            title={tr2.decksSearchAnkiweb()}
                            on:click={() =>
                                bridgeCommand(
                                    `shared:${encodeURIComponent(searchTerm)}`,
                                )}
                        >
                            <IconConstrain iconSize={100}>
                                {@html getSharedIcon}
                            </IconConstrain>
                        </span>
                    </th>
                    <th class="buttons" colspan="2">
                        <ButtonToolbar --icon-align="middle">
                            <IconButton
                                iconSize={100}
                                tooltip={tr2.decksCreateDeck()}
                                on:click={() => bridgeCommand("create")}
                            >
                                {@html createIcon}
                            </IconButton>
                            <IconButton
                                iconSize={100}
                                tooltip={tr2.decksImportFile()}
                                on:click={() => bridgeCommand("import")}
                            >
                                {@html importFileIcon}
                            </IconButton>
                        </ButtonToolbar>
                    </th>
                    <th>{tr2.actionsNew()}</th>
                    <th>{tr2.cardStatsReviewLogTypeLearn()}</th>
                    <th>{tr2.statisticsDueCount()}</th>
                </tr>
            </thead>
            <tbody>
                {#if filtered}
                    {#each filteredDecks as node}
                        <MatchedDeck {node} />
                    {/each}
                {:else}
                    {#each dueTree.children as node}
                        <Deck
                            {node}
                            current={node.deckId == args.currentDeckId}
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
        &.collapsed {
            left: -540px;
        }
        width: 540px;
        position: fixed;
        display: flex;
        flex-direction: column;
        z-index: 60;
        top: 0;
        bottom: 0;
        left: 0;
        overflow: hidden;
        transition: props.$transition ease-in-out;

        border-inline-end: 1px solid colors.$glass;

        background: colors.$glass;
        backdrop-filter: blur(props.$blur);

        @include elevation(4, $opacity-boost: -0.08);
        &:hover {
            @include elevation(4);
        }
    }

    table {
        table-layout: fixed;
        width: 100%;
        position: relative;
        padding: 0;

        thead {
            position: sticky;
            top: 0;
            border-bottom: 1px solid colors.$border-subtle;
            background: colors.$canvas;
            z-index: 2;
        }

        th {
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
            &.buttons {
                text-align: start;
            }
        }
    }
</style>
