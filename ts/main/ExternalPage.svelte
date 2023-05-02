<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { MainPageContext } from "./types";
    import { mwContext } from "./lib";
    import Badge from "components/Badge.svelte";
    import { backIcon } from "./icons";
    import { setupGraphsPage } from "graphs";
    import { setupDeckOptions } from "deck-options";

    const pages = {
        [MainPageContext.DECK_OPTIONS]: {
            name: tr.deckConfigTitle(),
            setup: setupGraphsPage,
        },
        [MainPageContext.STATS]: {
            name: tr.statisticsStats(),
            setup: setupDeckOptions,
        },
    };

    function loadPage(anchor: HTMLDivElement) {
        pages[$mwContext].setup(anchor);
    }
</script>

{#if Object.keys(pages).includes($mwContext.toString())}
    <Badge iconSize={150} on:click={() => ($mwContext = MainPageContext.HOME)}>
        {@html backIcon}
    </Badge>
    <!-- Page is mounted into this div -->
    <div class="external-page" use:loadPage />
{/if}

<style lang="scss">
    @use "sass/colors";

    .external-page {
        background-color: colors.$canvas;
    }
</style>
