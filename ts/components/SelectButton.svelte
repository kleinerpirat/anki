<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import Select from "../components/Select.svelte";

    export let options: string[];
    export let id: string | undefined = undefined;
    let className = "";
    export { className as class };

    export let tooltip: string | undefined = undefined;
    export let disabled = false;
    export let searchable = false;

    const dispatch = createEventDispatcher();
    function onMount(event: CustomEvent<HTMLDivElement>) {
        dispatch("mount", { button: event.detail });
    }
</script>

<!-- svelte-ignore a11y-no-onchange -->
<Select
    {id}
    {options}
    class="flex-grow-1 {className}"
    {disabled}
    title={tooltip}
    {searchable}
    isButton={true}
    clearable={false}
    on:mount={onMount}
    on:change
/>
