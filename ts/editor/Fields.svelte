<script lang="ts">
    import ScrollArea from "../components/ScrollArea.svelte";
</script>

<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<ScrollArea --margin-y="5px">
    <div class="fields">
        <slot />
    </div>
</ScrollArea>

<style lang="scss">
    .fields {
        display: grid;
        grid-auto-rows: min-content;
        grid-gap: 4px;
    }
</style>
