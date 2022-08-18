<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Container from "./Container.svelte";
    import type { Breakpoint } from "./types";

    export let id: string | undefined = undefined;
    let className: string = "";
    export { className as class };

    export let breakpoint: Breakpoint | "fluid" = "fluid";

    export let vertical = true;
    export let horizontal = false;

    let element: HTMLElement;

    let clientWidth = 0;
    let clientHeight = 0;
    let scrollWidth = 0;
    let scrollHeight = 0;
    let scrollTop = 0;
    let scrollLeft = 0;

    $: overflowX = scrollWidth > clientWidth;
    $: overflowY = scrollHeight > clientHeight;

    $: scrolledToTop = !overflowY ? true : scrollTop == 0;
    $: scrolledToRight = !overflowX ? true : scrollLeft == scrollWidth - clientWidth;
    $: scrolledToBottom = !overflowY ? true : scrollTop == scrollHeight - clientHeight;
    $: scrolledToLeft = !overflowX ? true : scrollLeft == 0;
    $: console.log(scrollLeft);

    $: shadows = {
        top: scrolledToBottom ? "0 0" : "0px -5px",
        right: scrolledToLeft ? "0 0" : "5px 0px",
        bottom: scrolledToTop ? "0 0" : "0px 5px",
        left: scrolledToRight ? "0 0" : "-5px 0px",
    };
    const rest = "5px -5px var(--border)";

    $: shadow = Array.from(Object.values(shadows), (v) => `inset ${v} ${rest}`).join(
        ", ",
    );
</script>

<div
    {id}
    class="scroll-area {className}"
    style={`--box-shadow: ${shadow}; --client-height: ${clientHeight}px`}
    bind:this={element}
    bind:clientHeight
    bind:clientWidth
    class:vertical
    class:horizontal
    on:scroll={() => {
        scrollHeight = element.scrollHeight;
        scrollWidth = element.scrollWidth;
        scrollTop = element.scrollTop;
        scrollLeft = element.scrollLeft;
    }}
>
    <Container {breakpoint}>
        <slot />
    </Container>
</div>

<style lang="scss">
    .scroll-area {
        background: var(--scroll-bg, var(--window-bg));
        margin: var(--margin, var(--margin-y, 0)) var(--margin, var(--margin-x, 0));
        overflow: hidden;

        flex-grow: 1;
        &.vertical {
            overflow-y: scroll;
        }
        &.horizontal {
            overflow-x: scroll;
        }
        /* force box-shadow to be rendered above children */
        &::before {
            content: "";
            position: fixed;
            pointer-events: none;
            left: 0;
            right: 0;
            z-index: 3;
            height: var(--client-height);
            box-shadow: var(--box-shadow);
            transition: box-shadow 0.1s ease-in-out;
        }
    }
</style>
