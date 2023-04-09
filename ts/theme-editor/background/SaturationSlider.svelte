<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let saturation: number;
</script>

<input
    class="vertical"
    type="range"
    min="0"
    max="1"
    step="0.02"
    bind:value={saturation}
/>

<style lang="scss">
    input {
        -webkit-appearance: slider-vertical;
    }
    input[type="range"]::-webkit-slider-runnable-track {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: 15px;
        cursor: pointer;
        background: linear-gradient(to bottom, transparent, black);
        filter: saturate(0);
    }
</style>
