<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";
    import type { MainPageArgs } from "main/types";

    export let dueTree: MainPageArgs["dueTree"];
    export let editing = false;
    export let hasDescription = false;
    export let name: string;

    function deckHierarchy(
        deck: MainPageArgs["dueTree"],
        parts: string[],
        levels: MainPageArgs["dueTree"][],
    ): MainPageArgs["dueTree"][] {
        deck = deck.children.find((child) => child.name == parts[0])!;
        if (parts.length == 1) {
            return [...levels, deck];
        }
        return deckHierarchy(deck, parts.slice(1), [...levels, deck]);
    }

    $: levels = deckHierarchy(dueTree, name.split("::"), []);
</script>

<div class="deck-header" class:editing class:has-description={hasDescription}>
    <div class="title">
        <!-- Placeholder -->
        <span style="visibility: hidden;">&nbsp;</span>
        {#each levels as deck, i}
            {#if i === levels.length - 1}
                <h1 class="deck-title">
                    {deck.name}
                </h1>
            {:else}
                <span
                    class="deck-level"
                    on:click={() => bridgeCommand(`select:${deck.deckId}`)}
                >
                    {deck.name}
                </span>
            {/if}
        {/each}
    </div>
</div>

<style lang="scss">
    @use "sass/feedback";

    .deck-header {
        width: 100%;
        display: grid;
        grid-template-columns: 1fr min-content;
    }
    .title {
        text-align: center;
    }
    .deck-level {
        @include feedback.clickable;
        &:not(:first-child)::before {
            content: " ‣ ";
        }
    }
</style>
