<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { tweened } from "svelte/motion";
    import { cubicOut } from "svelte/easing";
    import type { MainPageArgs } from "../types";
    export let deck: MainPageArgs["dueTree"];

    function ternaryPlot(a: number, b: number, c: number) {
        const total = a + b + c;

        const x = Math.round((b / total + c / (2 * total)) * 100);
        const y = Math.round((Math.sqrt(3) / 2) * (c / total) * 100);

        return { x: x, y: y };
    }

    let point: {x: number, y: number};
    const tweenedPoint = tweened({ x: 0, y: 0 }, { duration: 180, easing: cubicOut });
    tweenedPoint.subscribe((value) => point = value)

    $: tweenedPoint.set(
        ternaryPlot(deck.learnCount ?? 0, deck.reviewCount ?? 0, deck.newCount ?? 0),
    );

    const height = (Math.sqrt(3) / 2) * 100;
</script>

<svg viewBox="0 0 100 100" width="100%" height="100%">
    <polygon class="learn" points={`100,0 ${point.x},${point.y}, 50,${height}`} />
    <polygon class="new" points={`0,0 100,0 ${point.x},${point.y}`} />
    <polygon class="review" points={`0,0 50,${height} ${point.x},${point.y}`} />
</svg>

<style lang="scss">
    @use "sass/colors";
    @use "sass/elevation" as *;

    svg {
        stroke: colors.$border;
        stroke-width: 2;
        transform: rotate(-90deg) scale(0.8);

        polygon {
            fill: transparent;
            stroke: colors.$border;
            stroke-width: 2;
            &.learn {
                fill: colors.$card-learn;
            }
            &.review {
                fill: colors.$card-review;
            }
            &.new {
                fill: colors.$card-new;
            }
        }
        @include elevation(3, $drop-shadow: true);
    }
</style>
