<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Container from "./Container.svelte";
    import type { Breakpoint } from "./types";

    const rtl: boolean = window.getComputedStyle(document.body).direction == "rtl";

    export let id: string | undefined = undefined;
    let className: string = "";
    export { className as class };

    export let title: string;
    export let titleAlign: "start" | "center" | "end" = "start";

    export let breakpoint: Breakpoint | "fluid" = "fluid";
</script>

<div class="titled-container">
    <Container
        {id}
        class={className}
        --title-align={titleAlign}
        {breakpoint}
        withBackground
    >
        <div class="position-relative">
            <h2 class="title">{title}</h2>
            <div class="help-badge position-absolute" class:rtl>
                <slot name="tooltip" />
            </div>
        </div>
        <slot />
    </Container>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    .titled-container {
        display: contents;
        --gutter-block-start: 1rem;
        --gutter-block-end: 0.75rem;
        --gutter-inline-start: 1.25rem;
        --gutter-inline-end: 1.75rem;
    }

    .title {
        text-align: var(--title-align, start);
        border-bottom: 1px solid colors.$border;
    }

    .help-badge {
        right: 0;
        bottom: 4px;
        color: colors.$fg-subtle;
        transition: color props.$transition linear;
        &:hover {
            transition: none;
            color: colors.$fg;
        }
        &.rtl {
            right: unset;
            left: 0;
        }
    }
</style>
