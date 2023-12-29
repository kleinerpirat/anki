<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import SpinBox from "components/SpinBox.svelte";
    export let value: number;
    export let label: string;
</script>

<div class="custom-study-spinner">
    <div class="label">
        <slot name="label" />
    </div>
    <div class="spinner">
        {@html label}
        <SpinBox bind:value />
    </div>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
</style>
