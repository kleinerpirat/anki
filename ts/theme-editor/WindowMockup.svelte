<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import IconConstrain from "../components/IconConstrain.svelte";

    import { backgroundIcon, paletteIcon } from "./icons";
    import { adjustPath } from "./ThemeEditor.svelte";
    import Input from "./background/CSSInput.svelte";
    import { EditorMode } from "./types";
    import type { Background } from "./types";

    export let bg: Background;
    export let theme: "light" | "dark";
    export let active = false;
    export let filter: string;
    export let opacity: number;
    export let mode: EditorMode;

    $: editing = mode === EditorMode.BACKGROUND;

    let themeName =
        theme === "light" ? tr.preferencesThemeLight() : tr.preferencesThemeDark();
</script>

<div
    class="mockup fake-root"
    class:night-mode={theme === "dark"}
    class:active
    class:inactive={!active}
    on:click
    style:--background={adjustPath(bg.background)}
    style:--filter={filter}
    style:--opacity={opacity}
    style:--bg-crop="{bg.blur}px"
>
    <div class="toolbar">{themeName}</div>
    <div class="content">
        {#if active}
            {#if editing}
                <button class="close" on:click={() => (mode = EditorMode.THEME)}
                    >X</button
                >
                <Input bind:bg />
            {:else}
                <div class="split">
                    <div class="pane" on:click={() => (mode = EditorMode.BACKGROUND)}>
                        <IconConstrain iconSize={150}>
                            {@html backgroundIcon}
                        </IconConstrain>
                        <h3>{tr.preferencesBackground()}</h3>
                    </div>
                    <div class="pane" on:click={() => (mode = EditorMode.PALETTE)}>
                        <IconConstrain iconSize={150}>
                            {@html paletteIcon}
                        </IconConstrain>
                        <h3>{tr.preferencesColors()}</h3>
                    </div>
                </div>
            {/if}
        {/if}
    </div>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;
    @use "sass/background-mixins" as background;

    .mockup {
        display: inline-block;
        color: colors.$fg;
        margin-inline: 0.5em;
        height: 120px;
        min-width: 200px;
        position: relative;
        border-radius: props.$border-radius-medium props.$border-radius-medium
            props.$border-radius props.$border-radius;
        transition: all props.$transition ease-in-out;
        @include elevation(5);
        overflow: hidden;

        &:hover {
            @include elevation(7);
        }

        &.active {
            min-width: 240px;
            .content {
                background: colors.$glass;
                backdrop-filter: blur(props.$blur);
            }
        }

        &.inactive {
            opacity: 0.75;
            transform: scale(0.8);
            &:hover {
                opacity: 1;
                transform: scale(0.82);
            }

            .content::after {
                @include background.pseudo(center);
                background: var(--background);
                filter: var(--filter);
                opacity: var(--opacity);
            }
        }
        .content {
            display: flex;
            height: 100%;
            flex-direction: column;
            padding: 0.5em;

            .split {
                display: flex;
                flex-direction: row;
                > .pane {
                    & > :global(span) {
                        margin-top: 1em;
                    }
                    & > h3 {
                        text-align: center;
                        margin: 0 0 0.25rem 0;
                    }
                    flex-grow: 1;
                    display: grid;
                    height: 80px;
                    overflow: hidden;
                    &:hover {
                        @include elevation(4);
                    }

                    &:first-child {
                        border-right: 1px solid colors.$fg-subtle;
                    }
                }
            }
        }
    }

    .toolbar {
        text-align: center;
        font-weight: bold;
        height: 1.5em;
        width: 100%;
        background: colors.$glass;
        position: relative;
    }
</style>
