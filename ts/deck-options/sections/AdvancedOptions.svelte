<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { HelpPage } from "@tslib/help-page";

    import DynamicallySlottable from "components/DynamicallySlottable.svelte";
    import Item from "components/Item.svelte";
    import TitledContainer from "components/TitledContainer.svelte";
    import CardStateCustomizer from "../CardStateCustomizer.svelte";
    import WithHelpModal from "components/WithHelpModal.svelte";
    import type { DeckOptionsState } from "../lib";
    import SettingLabel from "../SettingLabel.svelte";
    import SpinBoxFloatRow from "../SpinBoxFloatRow.svelte";
    import SpinBoxRow from "../SpinBoxRow.svelte";
    import type { Section } from "components/HelpSection.svelte";

    export let state: DeckOptionsState;
    export let api: Record<string, never>;

    const config = state.currentConfig;
    const defaults = state.defaults;
    const cardStateCustomizer = state.cardStateCustomizer;

    const settings = {
        maximumInterval: {
            title: tr.schedulingMaximumInterval(),
            help: tr.deckConfigMaximumIntervalTooltip(),
            url: HelpPage.DeckOptions.maximumInterval,
        },
        startingEase: {
            title: tr.schedulingStartingEase(),
            help: tr.deckConfigStartingEaseTooltip(),
            url: HelpPage.DeckOptions.startingEase,
        },
        easyBonus: {
            title: tr.schedulingEasyBonus(),
            help: tr.deckConfigEasyBonusTooltip(),
            url: HelpPage.DeckOptions.easyBonus,
        },
        intervalModifier: {
            title: tr.schedulingIntervalModifier(),
            help: tr.deckConfigIntervalModifierTooltip(),
            url: HelpPage.DeckOptions.intervalModifier,
        },
        hardInterval: {
            title: tr.schedulingHardInterval(),
            help: tr.deckConfigHardIntervalTooltip(),
            url: HelpPage.DeckOptions.hardInterval,
        },
        newInterval: {
            title: tr.schedulingNewInterval(),
            help: tr.deckConfigNewIntervalTooltip(),
            url: HelpPage.DeckOptions.newInterval,
        },
        customScheduling: {
            title: tr.deckConfigCustomScheduling(),
            help: tr.deckConfigCustomSchedulingTooltip(),
            url: "https://faqs.ankiweb.net/the-2021-scheduler.html#add-ons-and-custom-scheduling",
        },
    };
    const helpSections = Object.values(settings) as Section[];
</script>

<TitledContainer title={tr.deckConfigAdvancedTitle()}>
    <WithHelpModal
        title={tr.deckConfigAdvancedTitle()}
        url={HelpPage.DeckOptions.advanced}
        {helpSections}
        let:openHelp
    >
        <DynamicallySlottable slotHost={Item} {api}>
            <Item>
                <SpinBoxRow
                    bind:value={$config.maximumReviewInterval}
                    defaultValue={defaults.maximumReviewInterval}
                    min={1}
                    max={365 * 100}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("maximumInterval"))}
                        >{settings.maximumInterval.title}</SettingLabel
                    >
                </SpinBoxRow>
            </Item>

            <Item>
                <SpinBoxFloatRow
                    bind:value={$config.initialEase}
                    defaultValue={defaults.initialEase}
                    min={1.31}
                    max={5}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("startingEase"))}
                        >{settings.startingEase.title}</SettingLabel
                    >
                </SpinBoxFloatRow>
            </Item>

            <Item>
                <SpinBoxFloatRow
                    bind:value={$config.easyMultiplier}
                    defaultValue={defaults.easyMultiplier}
                    min={1}
                    max={5}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("easyBonus"))}
                        >{settings.easyBonus.title}</SettingLabel
                    >
                </SpinBoxFloatRow>
            </Item>

            <Item>
                <SpinBoxFloatRow
                    bind:value={$config.intervalMultiplier}
                    defaultValue={defaults.intervalMultiplier}
                    min={0.5}
                    max={2}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("intervalModifier"))}
                        >{settings.intervalModifier.title}</SettingLabel
                    >
                </SpinBoxFloatRow>
            </Item>

            <Item>
                <SpinBoxFloatRow
                    bind:value={$config.hardMultiplier}
                    defaultValue={defaults.hardMultiplier}
                    min={0.5}
                    max={1.3}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("hardInterval"))}
                        >{settings.hardInterval.title}</SettingLabel
                    >
                </SpinBoxFloatRow>
            </Item>

            <Item>
                <SpinBoxFloatRow
                    bind:value={$config.lapseMultiplier}
                    defaultValue={defaults.lapseMultiplier}
                    max={1}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("newInterval"))}
                        >{settings.newInterval.title}</SettingLabel
                    >
                </SpinBoxFloatRow>
            </Item>

            {#if state.v3Scheduler}
                <Item>
                    <CardStateCustomizer
                        title={settings.customScheduling.title}
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("customScheduling"))}
                        bind:value={$cardStateCustomizer}
                    />
                </Item>
            {/if}
        </DynamicallySlottable>
    </WithHelpModal>
</TitledContainer>
