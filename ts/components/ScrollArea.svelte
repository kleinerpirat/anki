<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { throttle, update } from "lodash-es";
    import { tweened } from "svelte/motion";
    import { cubicOut } from "svelte/easing";
    import { onMount } from "svelte";

    let className: string = "";
    export { className as class };
    export let scrollX = false;
    export let scrollY = false;

    let scrollArea: HTMLDivElement;

    const scrollStates = {
        top: false,
        right: false,
        bottom: false,
        left: false,
    };

    const callback = (entries: IntersectionObserverEntry[]) => {
        entries.forEach((entry) => {
            scrollStates[entry.target.getAttribute("data-edge")!] =
                !entry.isIntersecting;
        });
    };

    let observer: IntersectionObserver;
    function initObserver(el: HTMLDivElement) {
        observer = new IntersectionObserver(callback, { root: el });
        for (const edge of el.getElementsByClassName("scroll-edge")) {
            observer.observe(edge);
        }
    }

    let scrollbarColor: string;
    let alpha: string;

    const alphaTween = tweened(0, { easing: cubicOut });

    onMount(() => {
        alphaTween.subscribe((value) => {
            const newValue = value.toFixed(1);

            if (alpha !== newValue) {
                const computedStyle = getComputedStyle(scrollArea);
                const hex = computedStyle.getPropertyValue("--scrollbar");
                const rgb = hexToRgb(hex);
                alpha = newValue;
                scrollbarColor = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`;
            }
        });
    });

    const hexToRgb = (hex: string) => {
        const [r, g, b] = hex.match(/\w\w/g)!.map((x) => parseInt(x, 16));
        return { r, g, b };
    };

    let timeoutId: number;

    function handleScroll() {
        alphaTween.set(1, { duration: 150 });
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            alphaTween.set(0, { duration: 800 });
        }, 360);
    }
    const throttledWheel = throttle(handleScroll, 100, { leading: true });
</script>

<div class="scroll-area-relative">
    <div
        class="scroll-area {className}"
        class:scroll-x={scrollX}
        class:scroll-y={scrollY}
        style:--scrollbar-bg={scrollbarColor}
        use:initObserver
        bind:this={scrollArea}
        on:scroll={throttledWheel}
    >
        <div class="scroll-content">
            <slot />

            <div class="scroll-edge" data-edge="top" />
            <div class="scroll-edge" data-edge="right" />
            <div class="scroll-edge" data-edge="bottom" />
            <div class="scroll-edge" data-edge="left" />
        </div>
    </div>
    {#if scrollStates.top} <div class="scroll-shadow top" /> {/if}
    {#if scrollStates.right} <div class="scroll-shadow right" /> {/if}
    {#if scrollStates.bottom} <div class="scroll-shadow bottom" /> {/if}
    {#if scrollStates.left} <div class="scroll-shadow left" /> {/if}
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    $shadow-top: inset 0 5px 5px -5px colors.$shadow;
    $shadow-bottom: inset 0 -5px 5px -5px colors.$shadow;
    $shadow-left: inset 5px 0 5px -5px colors.$shadow;
    $shadow-right: inset -5px 0 5px -5px colors.$shadow;

    .scroll-area-relative {
        position: relative;
        pointer-events: none;
        display: contents;
    }

    .scroll-area {
        position: relative;
        pointer-events: all;
        overscroll-behavior: none;
        overflow: overlay;
        &.scroll-x {
            overflow-x: auto;
            overflow-y: hidden;
            overscroll-behavior-y: auto;
        }
        &.scroll-y {
            overflow-y: auto;
            overflow-x: hidden;
            overscroll-behavior-x: none;
        }

        // transient scrollbar with tweened variable
        &::-webkit-scrollbar-thumb {
            background-color: var(--scrollbar-bg);
        }
    }

    .scroll-content {
        position: relative;
        .scroll-edge {
            position: absolute;
            &[data-edge="top"],
            &[data-edge="bottom"] {
                height: 1px;
                left: 0;
                right: 0;
            }
            &[data-edge="left"],
            &[data-edge="right"] {
                width: 1px;
                top: 0;
                bottom: 0;
            }
            &[data-edge="top"] {
                top: 0;
            }
            &[data-edge="bottom"] {
                bottom: 0;
            }
            &[data-edge="left"] {
                left: 0;
            }
            &[data-edge="right"] {
                right: 0;
            }
        }
    }
    .scroll-shadow {
        position: absolute;
        pointer-events: none;
        // value between LabelContainer (editor) and FloatingArrow
        z-index: 55;
        &.top,
        &.bottom {
            left: 0;
            right: 0;
            height: 5px;
        }
        &.left,
        &.right {
            top: 0;
            bottom: 0;
            width: 5px;
        }
        &.top {
            top: var(--inset-top, 0);
            box-shadow: $shadow-top;
        }
        &.bottom {
            bottom: var(--inset-bottom, 0);
            box-shadow: $shadow-bottom;
        }
        &.left {
            left: var(--inset-left, 0);
            box-shadow: $shadow-left;
        }
        &.right {
            right: var(--inset-right, 0);
            box-shadow: $shadow-right;
        }
    }
</style>
