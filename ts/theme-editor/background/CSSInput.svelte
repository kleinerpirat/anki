<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";

    import type { Background } from "../types";
    import { cssFilter } from "../ThemeEditor.svelte";

    export let bg: Background;

    function onInput(e: Event) {
        const input = e.target as HTMLTextAreaElement;
        const text = input.value;

        const backgroundMatch = text.match(/background:\s*(.*);/);
        const saturationMatch = text.match(/saturate\((.*)\)/);
        const opacityMatch = text.match(/opacity:\s*(\d*\.?\d*);/);
        const blurMatch = text.match(/blur\((\d*\.?\d+px)\)/);

        Object.assign(bg, {
            background: backgroundMatch ? backgroundMatch[1] : "var(--canvas)",
            saturation: saturationMatch ? saturationMatch[1] : 1,
            opacity: opacityMatch ? opacityMatch[1] : 1,
            blur: blurMatch ? blurMatch[1] : 0,
        });
        // trigger reactivity
        bg = bg;
    }

    $: hasFilter = bg.saturation < 1 || bg.blur > 0;
    $: css =
        `background: ${bg.background};` +
        (hasFilter ? `\nfilter: ${cssFilter(bg)};` : "") +
        (bg.opacity < 1 ? `\nopacity: ${bg.opacity};` : "");
</script>

<div class="controls">
    <textarea value={css} on:input={onInput} />
    <button on:click={() => bridgeCommand("file")}>Open File</button>
</div>

<style lang="scss">
    .controls {
        margin: 0.2rem;
        padding: 0.2rem 0.4rem;
        display: flex;
        flex-direction: column;
        border-top-left-radius: var(--border-radius-medium);
        border-bottom-left-radius: var(--border-radius-medium);
    }
    textarea {
        font-size: small;
        flex-grow: 1;
        padding: 0.25em 0.5em;
        min-width: 200px;
        min-height: 80px;
        resize: none;
        outline: none;
        border: none;
        overflow: auto;
    }
</style>
