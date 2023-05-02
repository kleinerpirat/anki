<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let position: "start" | "center" | "end";
    export let items: string[];
</script>

<div class="tray" style:justify-content={position}>
    <slot name="before" />
    {#if position === "start"}
        <slot />
    {/if}
    {#if items}
        {#each items as item}
            <div class="tray-item">
                {@html item}
            </div>
        {/each}
    {/if}
    {#if position !== "start"}
        <slot />
    {/if}
    <slot name="after" />
</div>

<style lang="scss">
    .tray {
        display: flex;
        flex-direction: row;

        .tray-item {
            display: inline-block;
        }
    }
</style>
