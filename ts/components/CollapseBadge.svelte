<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import IconConstrain from "../components/IconConstrain.svelte";
    import { chevronDown } from "./icons";

    export let collapsed = false;
    export let iconSize = 80;
</script>

<div class="collapse-badge" class:collapsed>
    <IconConstrain {iconSize}>{@html chevronDown}</IconConstrain>
</div>

<style lang="scss">
    @use "sass/props";

    .collapse-badge {
        display: inline-block;
        opacity: props.$opacity-idle;
        transition: opacity props.$transition ease-in-out,
            transform props.$transition ease-in;
        :global(.collapse-label:hover) & {
            opacity: 1;
        }
        &.collapsed {
            transform: rotate(-90deg);
        }
    }

    :global([dir="rtl"]) {
        .collapse-badge.collapsed {
            transform: rotate(90deg);
        }
    }
</style>
