<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import type { ToolbarArgs } from "./types";
    import { moveLegacyAddonsToTray } from "./legacy";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import { SyncStatus } from "./types";
    import SyncLink from "./SyncLink.svelte";
    import ToolbarLink from "./ToolbarLink.svelte";
    import ThemeToggle from "./ThemeToggle.svelte";
    import { onMount } from "svelte";

    let args: ToolbarArgs;
    export { args as toolbarArgs };

    export let syncActive = false;
    export let syncStatus: SyncStatus = SyncStatus.NO_CHANGES;
    export let decksCollapsed: boolean;
    export let collapsed: boolean;

    onMount(moveLegacyAddonsToTray);

    let leftTray: HTMLDivElement;
    export function focus(): void {
        leftTray?.focus();
    }
</script>

<div class="toolbar" class:collapsed class:decks-expanded={!decksCollapsed}>
    <div class="left-tray" bind:this={leftTray}>
        {#if decksCollapsed}
            <ToolbarLink
                id="decks"
                label={tr.actionsDecks()}
                title={tr.actionsShortcutKey({ val: "D" })}
                on:click={() => bridgeCommand("decks")}
            />
        {/if}
        {#each args.leftTrayContent as item}
            <div class="tray-item">
                {@html item}
            </div>
        {/each}
    </div>
    <div class="center-tray">
        <ToolbarLink
            label={tr.actionsAdd()}
            title={tr.actionsShortcutKey({ val: "A" })}
            on:click={() => bridgeCommand("add")}
        />
        <ToolbarLink
            label={tr.qtMiscBrowse()}
            title={tr.actionsShortcutKey({ val: "B" })}
            on:click={() => bridgeCommand("browse")}
        />
        <ToolbarLink
            label={tr.qtMiscStats()}
            title={tr.actionsShortcutKey({ val: "T" })}
            on:click={() => bridgeCommand("stats")}
        />
        {#each args.centerTrayContent as item}
            <div class="tray-item">
                {@html item}
            </div>
        {/each}
        <SyncLink active={syncActive} status={syncStatus} />
    </div>
    <div class="right-tray">
        {#each args.rightTrayContent as item}
            <div class="tray-item">
                {@html item}
            </div>
        {/each}
        <ThemeToggle />
    </div>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;
    @use "sass/button-mixins" as button;

    .toolbar {
        white-space: nowrap;
        transition: all props.$transition ease-in-out;
        display: grid;
        grid-template-columns: repeat(3, 1fr);

        background: colors.$glass;
        backdrop-filter: blur(props.$blur);

        &.collapsed {
            transform: translateY(-100vh);
            :global(:not(.fancy)) & {
                opacity: 0;
            }
        }
        transition: all props.$transition ease-in-out;

        &.decks-expanded {
            margin-left: 540px;
        }
    }


    .left-tray,
    .center-tray,
    .right-tray {
        display: flex;
        flex-direction: row;

       > div {
            display: inline-block;
        }
    }

    .left-tray {
        justify-content: start;
    }
    .center-tray {
        justify-content: center;
    }
    .right-tray {
        justify-content: end;
    }
</style>
