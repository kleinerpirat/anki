<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Select from "../components/Select.svelte";
    export let choices: string[];
    export let value: number = 0;
</script>

<Select
    class="enum-selector form-select"
    options={choices}
    bind:value
    clearable={false}
    searchable={false}
/>
