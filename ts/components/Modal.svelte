<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import type { Breakpoint } from "./types";
    import { fade } from "svelte/transition";
    import Badge from "./Badge.svelte";
    import { createEventDispatcher, onDestroy } from "svelte";
    export let show: boolean;
    export let title = "";
    export let withAccept = false;
    export let breakpoint: Breakpoint | "fluid" = "fluid";

    const dispatch = createEventDispatcher();

    function close(): void {
        show = false;
    }
    function accept(): void {
        dispatch("accept");
        show = false;
    }
    document.addEventListener(
        "keydown",
        (e: KeyboardEvent) => {
            if (e.key === "Escape") {
                show = false;
            }
        },
        { once: true },
    );
    onDestroy(() => {
        console.log("destroyed");
        dispatch("close");
    });
</script>

{#if show}
    <div class="modal-background" transition:fade>
        <div
            class="modal"
            class:modal-xxs={breakpoint === "xxs"}
            class:modal-xs={breakpoint === "xs"}
            class:modal-sm={breakpoint === "sm"}
            class:modal-md={breakpoint === "md"}
            class:modal-lg={breakpoint === "lg"}
            class:modal-xl={breakpoint === "xl"}
            class:modal-xxl={breakpoint === "xxl"}
            class:modal-fluid={breakpoint === "fluid"}
        >
            <div class="modal-header">
                <h5 class="modal-title" id="modalLabel">{title}</h5>
                <Badge tooltip={tr.actionsClose()} on:click={close} />
            </div>
            <div class="modal-content">
                <slot />
            </div>
            {#if withAccept}
                <div class="modal-footer">
                    <button type="button">{tr.actionsCancel()}</button>
                    <button type="button" class="primary" on:click={accept}>OK</button>
                </div>
            {/if}
        </div>
    </div>
{/if}

<style lang="scss">
    @use "sass/colors";
    @use "sass/breakpoints";
    @use "sass/background";

    .modal-background {
        position: fixed;
        z-index: 200;
        inset: 0;
        @include background.dim;
        display: grid;
        justify-content: center;
        align-content: center;
    }

    .modal {
        display: grid;
        background-color: colors.$canvas;
        grid-template:
            "header" min-content
            "content" 1fr
            "footer" min-content;
    }

    @include breakpoints.with-breakpoints-upto(
        "modal",
        (
            "max-width": (
                "xxs": 200px,
                "xs": 360px,
                "sm": 540px,
                "md": 720px,
                "lg": 960px,
                "xl": 1140px,
                "xxl": 1320px
            )
        )
    );

    .modal-header {
        grid-area: header;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid colors.$border;
    }
    .modal-content {
        grid-area: content;
    }
    .modal-footer {
        grid-area: footer;
        display: flex;
        justify-content: end;
    }
</style>
