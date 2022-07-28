<script lang="ts">
    import ScrollArea from "../components/ScrollArea.svelte";
</script>

<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<ScrollArea class="fields">
    <slot />
</ScrollArea>

<style lang="scss">
    :global(.fields) {
        display: grid;
        grid-auto-rows: min-content;
        grid-gap: 4px;

        padding: 5px 3px 0;

        > :global(:last-child) {
            /* bottom padding is eaten by overflow-x */
            margin-bottom: 5px;
        }
    }
</style>
