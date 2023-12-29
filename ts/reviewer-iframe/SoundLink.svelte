<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";
    import Badge from "components/Badge.svelte";
    import { playIcon } from "./icons";
    export let cmd: string;
</script>

<Badge
    iconSize={120}
    class="replay-button soundLink"
    on:click={() => bridgeCommand(cmd)}
>
    {@html playIcon}
</Badge>

<style lang="scss">
    :global(.replay-button) {
        text-decoration: none;
        display: inline-flex;
        vertical-align: middle;
        margin: 3px;
    }
</style>
