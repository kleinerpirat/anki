<!--
    Copyright: Ankitects Pty Ltd and contributors
    License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import RevertButton from "./RevertButton.svelte";
    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    let className = "";
    export { className as class };

    export let value: any;
    export let defaultValue: any;
    export let withPopover = true;
</script>

<div class="revertable-input justify-content-end {className}">
    <div class="revert" class:rtl>
        <RevertButton bind:value {defaultValue} {withPopover} />
    </div>
    <slot />
</div>

<style lang="scss">
    @use "sass/colors";

    .revert {
        position: absolute;
        right: var(--revert-offset, -20px);
        color: colors.$fg-subtle;
        &.rtl {
            right: unset;
            left: var(--revert-offset, -20px);
        }
    }
    .revertable-input {
        position: relative;

        &:hover,
        &:focus-within {
            .revert {
                color: colors.$fg-subtle;
            }
        }
        .revert:hover {
            color: colors.$fg;
        }
    }
</style>
