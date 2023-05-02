<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { Writable } from "svelte/store";
    import { writable } from "svelte/store";
    import DynamicallySlottable from "components/DynamicallySlottable.svelte";
    import ConfigSection from "./ConfigSection.svelte";
    import ScrollArea from "components/ScrollArea.svelte";
    import type { DynamicSvelteComponent } from "../sveltelib/dynamicComponent";
    import Addons from "./sections/Addons.svelte";
    import AdvancedOptions from "./sections/AdvancedOptions.svelte";
    import AudioOptions from "./sections/AudioOptions.svelte";
    import BuryOptions from "./sections/BuryOptions.svelte";
    import ConfigSelector from "./ConfigSelector.svelte";
    import DailyLimits from "./sections/DailyLimits.svelte";
    import DisplayOrder from "./sections/DisplayOrder.svelte";
    import HtmlAddon from "./HtmlAddon.svelte";
    import LapseOptions from "./sections/LapseOptions.svelte";
    import type { DeckOptionsState } from "./lib";
    import NewOptions from "./sections/NewOptions.svelte";
    import TimerOptions from "./sections/TimerOptions.svelte";
    import type { SlotHostProps } from "sveltelib/dynamic-slotting";

    export let state: DeckOptionsState;
    const addons = state.addonComponents;

    export function auxData(): Writable<Record<string, unknown>> {
        return state.currentAuxData;
    }

    export function addSvelteAddon(component: DynamicSvelteComponent): void {
        $addons = [...$addons, component];
    }

    export function addHtmlAddon(html: string, mounted: () => void): void {
        $addons = [
            ...$addons,
            {
                component: HtmlAddon,
                html,
                mounted,
            },
        ];
    }

    export const options = {};
    export const dailyLimits = {};
    export const newOptions = {};
    export const lapseOptions = {};
    export const buryOptions = {};
    export const displayOrder = {};
    export const timerOptions = {};
    export const audioOptions = {};
    export const advancedOptions = {};

    let onPresetChange: () => void;

    interface DynamicSlotHostProps extends SlotHostProps {
        class: string;
    }

    export function createProps(): DynamicSlotHostProps {
        return {
            detach: writable(false),
            class: "section",
        };
    }
</script>

<div class="deck-options-page">
    <ConfigSelector {state} on:presetchange={onPresetChange} />

    <ScrollArea>
        <DynamicallySlottable slotHost={ConfigSection} api={options} {createProps}>
            <div class="deck-options-body">
                <ConfigSection>
                    <DailyLimits {state} api={dailyLimits} bind:onPresetChange />
                </ConfigSection>

                <ConfigSection>
                    <NewOptions {state} api={newOptions} />
                </ConfigSection>

                <ConfigSection>
                    <LapseOptions {state} api={lapseOptions} />
                </ConfigSection>

                {#if state.v3Scheduler}
                    <ConfigSection>
                        <DisplayOrder {state} api={displayOrder} />
                    </ConfigSection>
                {/if}

                <ConfigSection>
                    <TimerOptions {state} api={timerOptions} />
                </ConfigSection>

                <ConfigSection>
                    <BuryOptions {state} api={buryOptions} />
                </ConfigSection>

                <ConfigSection>
                    <AudioOptions {state} api={audioOptions} />
                </ConfigSection>

                <ConfigSection>
                    <Addons {state} />
                </ConfigSection>

                <ConfigSection>
                    <AdvancedOptions {state} api={advancedOptions} />
                </ConfigSection>
            </div>
        </DynamicallySlottable>
    </ScrollArea>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/breakpoints" as bp;
    .deck-options-page {
        overflow-x: hidden;
        background-color: colors.$canvas;
        background .deck-options-body {
            @include bp.with-breakpoint("lg") {
                column-count: 2;
                column-gap: 5rem;
            }
        }
    }
</style>
