<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import Modal from "components/Modal.svelte";

    export let title: string;
    export let prompt: string;
    export let value = "";
    export let show: boolean;

    const dispatch = createEventDispatcher();

    function onAccept(): void {
        dispatch("accept", { text: value });
        show = false;
        value = "";
    }

    function focus(input: HTMLInputElement) {
        input.focus();
    }
</script>

<Modal {title} {show} on:accept={onAccept}>
    <form on:submit|preventDefault={onAccept}>
        <label for="prompt-input">{prompt}:</label>
        <input id="prompt-input" type="text" bind:value use:focus />
    </form>
</Modal>

<style lang="scss">
    @use "sass/colors";
</style>
