<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { Breakpoint } from "./types";
    import { pageTheme } from "../sveltelib/theme";

    export let id: string | undefined = undefined;
    let className: string = "";
    export { className as class };

    /* width: 100% if viewport < breakpoint otherwise with gutters */
    export let breakpoint: Breakpoint | "fluid" = "fluid";

    export let withBackground = false;
</script>

<div
    {id}
    class="container {className}"
    class:light={!$pageTheme.isDark}
    class:dark={$pageTheme.isDark}
    class:with-background={withBackground}
    class:container-xxs={breakpoint === "xxs"}
    class:container-xs={breakpoint === "xs"}
    class:container-sm={breakpoint === "sm"}
    class:container-md={breakpoint === "md"}
    class:container-lg={breakpoint === "lg"}
    class:container-xl={breakpoint === "xl"}
    class:container-xxl={breakpoint === "xxl"}
    class:container-fluid={breakpoint === "fluid"}
>
    <slot />
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/breakpoints";
    @use "sass/elevation" as *;

    .container {
        display: flex;
        flex-direction: var(--container-direction, column);
        margin: 0 auto;

        padding-block-start: var(--gutter-block-start, var(--gutter-block, 0));
        padding-block-end: var(--gutter-block-end, var(--gutter-block, 0));
        padding-inline-end: var(--gutter-inline-end, var(--gutter-inline, 0));
        padding-inline-start: var(--gutter-inline-start, var(--gutter-inline, 0));

        &.with-background {
            background: colors.$glass;
            backdrop-filter: blur(props.$blur);
            border: 1px solid colors.$glass;
            border-radius: props.$border-radius-medium;

            &.light {
                @include elevation(2, $opacity-boost: -0.08);
                &:hover,
                &:focus-within {
                    @include elevation(3);
                }
            }
            &.dark {
                @include elevation(3, $opacity-boost: -0.08);
                &:hover,
                &:focus-within {
                    @include elevation(4);
                }
            }
        }

        transition: box-shadow props.$transition ease-in-out;
        page-break-inside: avoid;

        &.container-fluid {
            width: 100%;
            height: 100%;

            margin: 0;
        }
    }

    @include breakpoints.with-breakpoints-upto(
        "container",
        (
            "max-width": (
                "xxs": 150px,
                "xs": 360px,
                "sm": 540px,
                "md": 720px,
                "lg": 960px,
                "xl": 1140px,
                "xxl": 1320px,
            ),
        )
    );
</style>
