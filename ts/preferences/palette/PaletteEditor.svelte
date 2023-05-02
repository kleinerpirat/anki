<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";

    import { EditorMode } from "../types";
    import type { Palette } from "../types";
    import Color from "./Color.svelte";
    // import PaletteSelector from "./PaletteSelector.svelte";
    import ScrollArea from "../../components/ScrollArea.svelte";

    // export let state: PaletteEditorState;

    export let palette: Palette;
    export let mode: EditorMode;

    function createJSON(): void {
        const colors: string[] = [];
        for (const input of document.querySelectorAll(".color-input")) {
            colors.push(`${input.getAttribute("data-name")!}=${input.value}`);
        }
        bridgeCommand(`applyPalette:${colors.join(":")}`);
    }

    let onPaletteChange: () => void;
</script>

<div class="palette-editor">
    <!-- <PaletteSelector {state} on:palettechange={onPaletteChange} /> -->
    <ScrollArea>
        <button class="close" on:click={() => (mode = EditorMode.THEME)}>X</button>

        {#each palette as { name, comment, value }, i}
            <Color {name} {comment} {value} defaultValue={value} />
        {/each}
    </ScrollArea>
</div>

<button on:click={createJSON}>Apply Palette</button>

<style lang="scss">
    @use "sass/colors";

    .palette-editor {
        background: colors.$canvas;
        column-count: 2;
    }

    .close {
        width: 20px;
        height: 20px;
        position: fixed;
        top: 0;
        right: 0;
        display: grid;
        align-items: center;
        align-content: center;
    }
</style>
