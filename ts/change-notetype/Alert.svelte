<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { slide } from "svelte/transition";

    import Badge from "../components/Badge.svelte";
    import { minusIcon, plusIcon } from "./icons";
    import { MapContext } from "./lib";

    export let unused: string[];
    export let ctx: MapContext;

    let unusedMsg: string;
    $: unusedMsg =
        ctx === MapContext.Field
            ? tr.changeNotetypeWillDiscardContent()
            : tr.changeNotetypeWillDiscardCards();

    const maxItems: number = 3;
    let collapsed: boolean = true;
    $: collapseMsg = collapsed
        ? tr.changeNotetypeExpand()
        : tr.changeNotetypeCollapse();
    $: icon = collapsed ? plusIcon : minusIcon;
</script>

<div class="alert" in:slide out:slide>
    {#if unused.length > maxItems}
        <div on:click={() => (collapsed = !collapsed)}>
            <Badge iconSize={80}>
                {@html icon}
            </Badge>
            <span class="collapse-message">
                {collapseMsg}
            </span>
        </div>
    {/if}
    {unusedMsg}
    {#if collapsed}
        <div>
            {unused.slice(0, maxItems).join(", ")}
            {#if unused.length > maxItems}
                ... (+{unused.length - maxItems})
            {/if}
        </div>
    {:else}
        <ul>
            {#each unused as entry}
                <li>{entry}</li>
            {/each}
        </ul>
    {/if}
</div>

<style lang="scss">
    @use "sass/props";
    @use "sass/feedback";

    .alert {
        position: relative;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: props.$border-radius;
    }
    .collapse-message {
        @include feedback.clickable;
    }
</style>
