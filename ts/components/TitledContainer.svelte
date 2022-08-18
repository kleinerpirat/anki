<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Container from "./Container.svelte";

    export let title: string;
</script>

<Container class="flex-grow-1" --gutter-block="2px" --container-margin="0">
    <h1>{title}</h1>

    <slot />
</Container>

<style lang="scss">
    h1 {
        border-bottom: 1px solid var(--medium-border);
    }
</style>
