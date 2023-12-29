<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { Breakpoint } from "./types";
    import IconConstrain from "./IconConstrain.svelte";
    import Shortcut from "./Shortcut.svelte";

    export let icon: string = "";
    export let text: string = "";
    export let shortcut: string | undefined = undefined;
    export let tooltip: string | undefined = undefined;
    export let withBackground = false;
    export let size = 160;
    export let breakpoint: Breakpoint | "fluid" = "fluid";
</script>

{#if shortcut}
    <Shortcut keyCombination={shortcut} on:action />
{/if}
<div
    class="tile"
    class:with-background={withBackground}
    class:tile-xxs={breakpoint === "xxs"}
    class:tile-xs={breakpoint === "xs"}
    class:tile-sm={breakpoint === "sm"}
    class:tile-md={breakpoint === "md"}
    class:tile-lg={breakpoint === "lg"}
    class:tile-xl={breakpoint === "xl"}
    class:tile-xxl={breakpoint === "xxl"}
    title={tooltip}
    style:--tile-size="{size}px"
    on:click
    on:mouseenter
    on:mouseleave
>
    <div class="icon">
        <IconConstrain iconSize={100}>
            {@html icon}
            <slot name="icon" />
        </IconConstrain>
    </div>
    {#if text}
        <span class="text">
            {text}
        </span>
    {/if}
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/feedback";

    .tile {
        width: var(--tile-size);
        height: var(--tile-size);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        // determines icon size
        --buttons-size: calc(var(--tile-size) / 2);
        @include feedback.clickable($primary: true);
        border-radius: props.$border-radius;

        &.with-background {
            background: var(--tile-bg, colors.$glass);
        }

        transition: transform props.$transition ease-out;
        transform: scale(0.95);

        &:hover {
            background: var(--tile-bg, colors.$glass);
            z-index: 1;

            transform: scale(1);
        }

        .text {
            font-size: 1rem;
            text-align: center;
        }
    }
</style>
