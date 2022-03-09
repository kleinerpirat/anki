<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "../lib/ftl";
    import { bridgeCommand } from "../lib/bridgecommand";
    import Shortcut from "./Shortcut.svelte";

    let className = "";
    export { className as class };

    export let cmd = "";
    export let keyCombination = "";
</script>

<div
    class="command {className}"
    on:click={() => bridgeCommand(cmd)}
    title={tr.actionsShortcutKey({ val: keyCombination })}
>
    <slot />
</div>

{#if keyCombination}
    <Shortcut {keyCombination} on:action={() => bridgeCommand(cmd)} />
{/if}

<style lang="scss">
    .command {
        cursor: pointer;
    }
</style>
