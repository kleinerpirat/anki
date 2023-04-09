<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { throttle } from "lodash-es";
    import type { Decks } from "@tslib/proto";

    import { bridgeCommand } from "@tslib/bridgecommand";
    import CollapseBadge from "../../components/CollapseBadge.svelte";
    import IconConstrain from "../../components/IconConstrain.svelte";
    import { scrollIntoViewIfNeeded } from "./utils";
    import { createEventDispatcher } from "svelte";

    export let node: Decks.DeckTreeNode;
    export let current = false;

    const dispatch = createEventDispatcher();

    function focusIfCurrent(el: HTMLTableRowElement) {
        if (current) {
            el.focus();
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        const el = e.target as HTMLTableRowElement;
        switch (e.key) {
            case "Enter":
            case "Space":
                bridgeCommand("study");
                break;
            case "ArrowUp":
                const prev = el.previousElementSibling as HTMLTableRowElement;
                prev?.focus();
                break;
            case "ArrowDown":
                const next = el.nextElementSibling as HTMLTableRowElement;
                next?.focus();
                break;
            case "ArrowLeft":
                bridgeCommand(`collapse:${node.deckId}`);

                break;
            case "ArrowRight":
                bridgeCommand(`expand:${node.deckId}`);
                break;
            case "Tab":
                e.preventDefault();
                dispatch("tab", { shiftKey: e.shiftKey });
        }
    }

    function handleFocus(e: FocusEvent) {
        scrollIntoViewIfNeeded(e.target as HTMLTableRowElement);
        bridgeCommand(`open:${node.deckId}`);
    }

    const throttleFocusHandling = throttle((e: FocusEvent) => {
        handleFocus(e);
    }, 50);
</script>

<tr
    class:current
    tabindex={0}
    on:contextmenu|preventDefault={() => bridgeCommand(`opts:${node.deckId}`)}
    on:click={() => bridgeCommand(`open:${node.deckId}`)}
    on:dblclick={() => bridgeCommand("study")}
    on:focus={throttleFocusHandling}
    on:keydown={handleKeydown}
    use:focusIfCurrent
>
    <td class="deck" colspan="5" style:padding-left="{(node.level - 1) * 0.8}rem">
        {#if node.children}
            <span
                class="collapse-button"
                on:click|preventDefault={() =>
                    bridgeCommand(
                        `${node.collapsed ? "expand" : "collapse"}:${node.deckId}`,
                    )}
            >
                <CollapseBadge collapsed={node.collapsed} />
            </span>
        {:else}
            <span>
                <IconConstrain iconSize={80} />
            </span>
        {/if}
        <span class="deck-name" class:filtered={node.filtered}>
            {node.name}
        </span>
    </td>
    <td align="right">
        <span
            class="new-count"
            class:zero-count={!node.newCount}
            on:click|preventDefault={(e) =>
                bridgeCommand(
                    `browserSearch:"deck:${node.name}" is:due OR -prop:due=0 is:new`,
                )}
        >
            {node.newCount ? node.newCount : 0}
        </span>
    </td>
    <td align="right">
        <span
            class="learn-count"
            class:zero-count={!node.learnCount}
            on:click|preventDefault={(e) =>
                bridgeCommand(
                    `browserSearch:"deck:${node.name}" is:due OR -prop:due=0 is:learn`,
                )}
        >
            {node.learnCount ? node.learnCount : 0}
        </span>
    </td>
    <td align="right">
        <span
            class="review-count"
            class:zero-count={!node.reviewCount}
            on:click|preventDefault={(e) =>
                bridgeCommand(
                    `browserSearch:"deck:${node.name}" is:due OR -prop:due=0 is:review`,
                )}
        >
            {node.reviewCount ? node.reviewCount : 0}
        </span>
    </td>
</tr>

{#if !node.collapsed && node.children}
    {#each node.children as child}
        <svelte:self node={child} />
    {/each}
{/if}

<style lang="scss">
    @use "sass/colors";

    tr {
        td {
            text-align: end;
            &:first-child {
                text-align: start;
            }
            padding: 1px 12px;
            .fancy & {
                padding: 4px 12px;
            }
            &.deck {
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
            }
        }
        &.current,
        &:hover {
            td {
                background: colors.$glass;
            }
        }
    }

    .deck-name.filtered {
        color: colors.$link;
    }
    .collapse-button,
    span[class*="count"] {
        cursor: pointer;
    }
</style>
