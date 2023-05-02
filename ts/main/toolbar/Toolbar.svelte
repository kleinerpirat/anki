<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { refreshInsertedHTML } from "@tslib/helpers";
    import type { ToolbarContent } from "./types";
    import { MainPageContext } from "../types";
    import { moveLegacyAddonsToTray } from "./legacy";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import { SyncStatus } from "./types";
    import SyncLink from "./SyncLink.svelte";
    import ToolbarLink from "./ToolbarLink.svelte";
    import ThemeToggle from "./ThemeToggle.svelte";
    import { onMount } from "svelte";
    import { mwContext } from "../lib";
    import Tray from "./Tray.svelte";

    export let addonContent: ToolbarContent;

    export let syncActive = false;
    export let syncStatus: SyncStatus = SyncStatus.NO_CHANGES;
    export let decksCollapsed: boolean;
    export let collapsed: boolean;

    onMount(moveLegacyAddonsToTray);

    function runUserContent(el: HTMLElement) {
        refreshInsertedHTML(el);
    }
</script>

<div class="toolbar" class:collapsed use:runUserContent>
    <Tray position="start" items={addonContent.leftTrayContent}>
        {#if decksCollapsed}
            <ToolbarLink
                id="decks"
                label={tr.actionsDecks()}
                title={tr.actionsShortcutKey({ val: "D" })}
                on:click={() => bridgeCommand("decks")}
            />
        {/if}
    </Tray>

    <Tray position="center" items={addonContent.centerTrayContent}>
        {#if $mwContext !== MainPageContext.HOME}
            <ToolbarLink
                label={tr.qtMiscHome()}
                title={tr.actionsShortcutKey({ val: "Escape" })}
                on:click={() => bridgeCommand("home")}
            />
        {/if}
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
        <SyncLink slot="after" active={syncActive} status={syncStatus} />
    </Tray>
    <Tray position="end" items={addonContent.rightTrayContent}>
        <ThemeToggle />
    </Tray>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    .toolbar {
        grid-area: toolbar;
        white-space: nowrap;
        transition: all props.$transition ease-in-out;
        display: grid;
        grid-template-columns: repeat(3, 1fr);

        background: var(--MainPage-toolbar-bg, colors.$glass);
        backdrop-filter: blur(props.$blur);

        border-bottom: 1px solid colors.$border-subtle;
        &.collapsed {
            transform: translateY(-100vh);
            :global(:not(.fancy)) & {
                opacity: 0;
            }
        }
        transition: all props.$transition ease-in-out;
    }
</style>
