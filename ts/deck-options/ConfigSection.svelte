<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Item from "components/Item.svelte";
    import type { SlotHostProps } from "../sveltelib/dynamic-slotting";

    export let id: string | undefined = undefined;
    export let hostProps: SlotHostProps | undefined = undefined;
</script>

<div class="config-section">
    <Item {id} {hostProps}>
        <slot />
    </Item>
</div>

<style lang="scss">
    @use "sass/breakpoints" as bp;

    .config-section {
        break-inside: avoid;
    }
</style>
