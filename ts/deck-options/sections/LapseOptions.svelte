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
    import EnumSelectorRow from "../EnumSelectorRow.svelte";
    import WithHelpModal from "components/WithHelpModal.svelte";
    import type { DeckOptionsState } from "../lib";
    import SettingLabel from "../SettingLabel.svelte";
    import SpinBoxRow from "../SpinBoxRow.svelte";
    import StepsInputRow from "../StepsInputRow.svelte";
    import type { Section } from "components/HelpSection.svelte";
    import Warning from "../Warning.svelte";

    export let state: DeckOptionsState;
    export let api = {};

    const config = state.currentConfig;
    const defaults = state.defaults;

    let stepsExceedMinimumInterval: string;
    $: {
        const lastRelearnStepInDays = $config.relearnSteps.length
            ? $config.relearnSteps[$config.relearnSteps.length - 1] / 60 / 24
            : 0;
        stepsExceedMinimumInterval =
            lastRelearnStepInDays > $config.minimumLapseInterval
                ? tr.deckConfigRelearningStepsAboveMinimumInterval()
                : "";
    }

    const leechChoices = [tr.actionsSuspendCard(), tr.schedulingTagOnly()];

    const settings = {
        relearningSteps: {
            title: tr.deckConfigRelearningSteps(),
            help: tr.deckConfigRelearningStepsTooltip(),
            url: HelpPage.DeckOptions.relearningSteps,
        },
        minimumInterval: {
            title: tr.schedulingMinimumInterval(),
            help: tr.deckConfigMinimumIntervalTooltip(),
            url: HelpPage.DeckOptions.minimumInterval,
        },
        leechThreshold: {
            title: tr.schedulingLeechThreshold(),
            help: tr.deckConfigLeechThresholdTooltip(),
            url: HelpPage.Leeches.leeches,
        },
        leechAction: {
            title: tr.schedulingLeechAction(),
            help: tr.deckConfigLeechActionTooltip(),
            url: HelpPage.Leeches.waiting,
        },
    };
    const helpSections = Object.values(settings) as Section[];
</script>

<TitledContainer title={tr.schedulingLapses()}>
    <WithHelpModal
        title={tr.schedulingLapses()}
        url={HelpPage.DeckOptions.lapses}
        {helpSections}
        let:openHelp
    >
        <DynamicallySlottable slotHost={Item} {api}>
            <Item>
                <StepsInputRow
                    bind:value={$config.relearnSteps}
                    defaultValue={defaults.relearnSteps}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("relearningSteps"))}
                        >{settings.relearningSteps.title}</SettingLabel
                    >
                </StepsInputRow>
            </Item>

            <Item>
                <SpinBoxRow
                    bind:value={$config.minimumLapseInterval}
                    defaultValue={defaults.minimumLapseInterval}
                    min={1}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("minimumInterval"))}
                        >{settings.minimumInterval.title}</SettingLabel
                    >
                </SpinBoxRow>
            </Item>

            <Item>
                <Warning warning={stepsExceedMinimumInterval} />
            </Item>

            <Item>
                <SpinBoxRow
                    bind:value={$config.leechThreshold}
                    defaultValue={defaults.leechThreshold}
                    min={1}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("leechThreshold"))}
                        >{settings.leechThreshold.title}</SettingLabel
                    >
                </SpinBoxRow>
            </Item>

            <Item>
                <EnumSelectorRow
                    bind:value={$config.leechAction}
                    defaultValue={defaults.leechAction}
                    choices={leechChoices}
                    breakpoint="md"
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("leechAction"))}
                        >{settings.leechAction.title}</SettingLabel
                    >
                </EnumSelectorRow>
            </Item>
        </DynamicallySlottable>
    </WithHelpModal>
</TitledContainer>
