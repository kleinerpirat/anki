<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { MainPageArgs } from "main/types";
    import Tray from "../toolbar/Tray.svelte";
    import { refreshInsertedHTML } from "@tslib/helpers";

    export let addonContent: MainPageArgs["addonContent"]["statusBar"];

    $: leftTrayContent = addonContent?.leftTrayContent;
    $: rightTrayContent = addonContent?.rightTrayContent;

    function runUserContent(el: HTMLElement) {
        refreshInsertedHTML(el);
    }
</script>

<div class="status-bar" use:runUserContent>
    <Tray position="start" items={leftTrayContent}>
        <slot name="left-tray" />
    </Tray>
    <slot name="center-tray" />
    <Tray position="end" items={rightTrayContent}>
        <slot name="right-tray" />
    </Tray>
</div>

<style lang="scss">
    @use "sass/background";
    @use "sass/elevation" as *;

    .status-bar {
        grid-area: status;
        z-index: 100;
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-between;
        padding-inline: 5px;
        font-size: small;
        align-items: center;

        @include background.glass;
        @include elevation(3);
    }
</style>
