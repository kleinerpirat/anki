<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "../lib/ftl";
    import { renameIcon, shareIcon, optionsIcon } from "./icons";
    import Option from "./Option.svelte";

    export let node: any;
</script>

<span class="text-nowrap align-self-end">
    <Option node>{@html renameIcon}</Option>
    <Option node>{@html optionsIcon}</Option>
    <Option node>{@html shareIcon}</Option>
</span>

<style lang="scss">
</style>
