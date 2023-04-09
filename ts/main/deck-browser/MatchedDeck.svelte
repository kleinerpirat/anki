<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { dotIcon } from "../icons";

    import { bridgeCommand } from "@tslib/bridgecommand";
    import IconConstrain from "../../components/IconConstrain.svelte";
    import type { FilteredDeckTree } from "../types";

    export let node: FilteredDeckTree;
</script>

{#if node.matched || node.containsMatch}
    <tr
        class="deck"
        class:current={node.matched}
        on:contextmenu|preventDefault={() => bridgeCommand(`opts:${node.deckId}`)}
    >
        <td
            class="decktd"
            colspan="5"
            style:padding-left="{(node.level - 1) * 0.8}rem"
            on:click={() => bridgeCommand(`open:${node.deckId}`)}
            on:dblclick={() => bridgeCommand("study")}
        >
            {#if node.matched}
                <span style:opacity={0.4}>
                    <IconConstrain iconSize={80}>{@html dotIcon}</IconConstrain>
                </span>
            {:else}
                <span>
                    <IconConstrain iconSize={80} />
                </span>
            {/if}
            <div class="deck-name" class:filtered={node.filtered}>
                {node.name}
            </div>
        </td>
        <td align="right">
            <span class="new-count" class:zero-count={!node.newCount}>
                {node.newCount ? node.newCount : 0}
            </span>
        </td>
        <td align="right">
            <span class="learn-count" class:zero-count={!node.learnCount}>
                {node.learnCount ? node.learnCount : 0}
            </span>
        </td>
        <td align="right">
            <span class="review-count" class:zero-count={!node.reviewCount}>
                {node.reviewCount ? node.reviewCount : 0}
            </span>
        </td>
    </tr>

    {#if node.children}
        {#each node.children as child}
            <svelte:self node={child} />
        {/each}
    {/if}
{/if}

<style lang="scss">
    @use "sass/colors";

    .deck-name {
        color: colors.$fg;
        text-decoration: none;
        width: 100%;
        display: inline-block;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
