<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script context="module" lang="ts">
    export function cssFilter(bg: Background): string {
        return `saturate(${bg.saturation}) blur(${bg.blur}px)`;
    }

    export function adjustPath(backgroundString: string) {
        return backgroundString.replace(/url\(["']*(.*)["']*\)/, "url(../../$1)");
    }
</script>

<script lang="ts">
    import { pageTheme } from "../sveltelib/theme";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import type { Background, Palette, Theme } from "./types";
    import { EditorMode } from "./types";
    import WindowMockup from "./WindowMockup.svelte";
    import OpacitySlider from "./background/OpacitySlider.svelte";
    import SaturationSlider from "./background/SaturationSlider.svelte";
    import BlurSlider from "./background/BlurSlider.svelte";
    import PaletteEditor from "./palette/PaletteEditor.svelte";

    let mode = EditorMode.THEME;
    $: bridgeCommand(`mode:${mode}`);

    export let light: Theme;
    export let dark: Theme;

    $: currentBg = $pageTheme.isDark ? dark.bg : light.bg;

    $: darkFilter = cssFilter(dark.bg);
    $: darkOpacity = dark.bg.opacity;

    $: lightFilter = cssFilter(light.bg);
    $: lightOpacity = light.bg.opacity;

    export function setBackgroundImage(name: string) {
        const urlRegex = /url\(.*\)/;
        if (urlRegex.test(currentBg.background)) {
            currentBg.background = currentBg.background.replace(
                urlRegex,
                `url(${name})`,
            );
        } else {
            currentBg.background = `url(${name})`;
        }
        currentBg = currentBg;
        bridgeCommand(
            "apply" +
                `:${currentBg.background}` +
                `:${currentBg.saturation}` +
                `:${currentBg.opacity}` +
                `:${currentBg.blur}`,
        );
    }

    $: bridgeCommand(
        "apply" +
            `:${currentBg.background}` +
            `:${currentBg.saturation}` +
            `:${currentBg.opacity}` +
            `:${currentBg.blur}`,
    );

    // const state = new PaletteEditorState(did, info);
</script>

{#if mode === EditorMode.PALETTE}
    <PaletteEditor
        palette={$pageTheme.isDark ? dark.palette : light.palette}
        bind:mode
    />
{:else}
    <div
        class="theme-editor"
        class:editing={mode === EditorMode.BACKGROUND}
        style:--background={adjustPath(currentBg.background)}
        style:--filter={$pageTheme.isDark ? darkFilter : lightFilter}
        style:--opacity={$pageTheme.isDark ? darkOpacity : lightOpacity}
        style:--bg-crop="{currentBg.blur}px"
    >
        <div class="preview" class:flipped={$pageTheme.isDark}>
            <WindowMockup
                bind:bg={light.bg}
                filter={lightFilter}
                opacity={lightOpacity}
                active={!$pageTheme.isDark}
                theme="light"
                on:click={() => bridgeCommand("theme:1")}
                bind:mode
            />
            <WindowMockup
                bind:bg={dark.bg}
                filter={darkFilter}
                opacity={darkOpacity}
                active={$pageTheme.isDark}
                theme="dark"
                on:click={() => bridgeCommand("theme:2")}
                bind:mode
            />
        </div>

        {#if mode === EditorMode.BACKGROUND}
            <SaturationSlider bind:saturation={currentBg.saturation} />
            <OpacitySlider bind:opacity={currentBg.opacity} />
            <BlurSlider bind:blur={currentBg.blur} />
        {/if}
    </div>
{/if}

<style lang="scss">
    @use "sass/props";
    @use "sass/background-mixins" as background;

    .theme-editor {
        margin-top: 1em;
        margin-bottom: 0.5em;
        height: 100%;
        background: none;
        position: relative;

        display: grid;
        justify-content: center;
        align-content: center;

        &::after {
            @include background.pseudo(center);
            background: var(--background);
            filter: var(--filter);
            opacity: var(--opacity);
        }
    }
    .preview {
        margin: 0 auto;
        border-radius: 5px;
        height: 100%;
        border-radius: props.$border-radius-medium;
        grid-area: preview;
        display: flex;
    }
</style>
