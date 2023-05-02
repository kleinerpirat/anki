<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let label: string;
    export let id: string | undefined = undefined;
    export let title: string | undefined = undefined;
</script>

<a {id} class="hitem" tabindex="-1" aria-label={label} {title} on:click>
    {label}
</a>

<style lang="scss">
    @use "sass/colors";

    :global(a) {
        &:hover {
            text-decoration: none !important;
            color: colors.$fg;
        }
    }
</style>
