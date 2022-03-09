<script lang="ts">
    import * as tr from "../../lib/ftl";
    import IconConstrain from "../../components/IconConstrain.svelte";
    import WithCommand from "../../components/WithCommand.svelte";
    import { decksIcon, addIcon, browseIcon, statsIcon } from "../icons";

    const items = [
        {
            cmd: "decks",
            icon: decksIcon,
            shortcut: "D",
        },
        {
            cmd: "add",
            icon: addIcon,
            shortcut: "A",
        },
        {
            cmd: "browse",
            icon: browseIcon,
            shortcut: "B",
        },
        {
            cmd: "stats",
            icon: statsIcon,
            shortcut: "T",
        },
    ];
</script>

<div class="toolbar d-flex flex-column justify-content-start">
    {#each items as item}
        <WithCommand cmd={item.cmd} keyCombination={item.shortcut}>
            <IconConstrain --buttons-size="32px">
                {@html item.icon}
            </IconConstrain>
        </WithCommand>
    {/each}
</div>

<style lang="scss">
    .toolbar {
        margin-top: calc(32px + 0.5rem);
        line-height: calc(32px + 2rem);
    }
</style>
