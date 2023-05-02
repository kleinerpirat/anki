<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let blur: number;
</script>

<input type="range" min="0" max="20" step="0.1" bind:value={blur} />

<style lang="scss">
    input[type="range"]::-webkit-slider-runnable-track {
        position: fixed;
        left: 0;
        bottom: 0;
        right: 0;
        height: 15px;

        cursor: pointer;

        &::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0;
            backdrop-filter: blur(20px);
            mask: linear-gradient(transparent, black 50%);
        }
    }
</style>
