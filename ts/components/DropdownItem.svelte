<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let id: string | undefined = undefined;
    let className = "";
    export { className as class };

    export let buttonRef: HTMLButtonElement | undefined = undefined;

    export let tooltip: string | undefined = undefined;

    export let active = false;
    export let disabled = false;

    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    $: if (buttonRef && active) {
        buttonRef!.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
        });
    }

    function arrowNavigation(e: KeyboardEvent) {
        const el = e.target as HTMLButtonElement;
        /* Arrow key navigation */
        switch (e.code) {
            case "ArrowUp": {
                const prevSibling = el.previousElementSibling as HTMLElement;
                if (prevSibling) {
                    prevSibling.focus();
                } else {
                    // close popover
                    document.body.click();
                }
                break;
            }
            case "ArrowDown": {
                const nextSibling = el.nextElementSibling as HTMLElement;
                if (nextSibling) {
                    nextSibling.focus();
                } else {
                    // close popover
                    document.body.click();
                }
                break;
            }
        }
    }

    export let tabbable = false;
</script>

<button
    bind:this={buttonRef}
    {id}
    tabindex={tabbable ? 0 : -1}
    class="dropdown-item {className}"
    class:active
    class:rtl
    title={tooltip}
    {disabled}
    on:mouseenter
    on:focus
    on:click
    on:mousedown|preventDefault
    on:keydown={arrowNavigation}
>
    <slot />
</button>

<style lang="scss">
    @use "sass/colors";

    button {
        display: flex;
        justify-content: start;
        width: 100%;
        padding: 0.25rem 1rem;
        white-space: nowrap;
        font-size: var(--dropdown-font-size, small);

        background: none;
        box-shadow: none !important;
        border: none;
        border-radius: 0;
        color: colors.$fg;

        &:hover:not([disabled]) {
            background: colors.$text-highlighted-bg;
            color: colors.$text-highlighted-fg;
        }

        &[disabled] {
            cursor: default;
            color: colors.$fg-disabled;
        }

        /* selection highlight */
        &:not(.rtl) {
            border-left: 3px solid transparent;
        }
        &.rtl {
            border-right: 3px solid transparent;
        }
        &.active {
            &:not(.rtl) {
                border-left-color: colors.$focus;
            }
            &.rtl {
                border-right-color: colors.$focus;
            }
        }
    }
</style>
