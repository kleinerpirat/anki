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
    import WithHelpModal from "components/WithHelpModal.svelte";
    import type { DeckOptionsState } from "../lib";
    import SettingLabel from "../SettingLabel.svelte";
    import SwitchRow from "../SwitchRow.svelte";
    import type { Section } from "components/HelpSection.svelte";

    export let state: DeckOptionsState;
    export let api: Record<string, never>;

    const config = state.currentConfig;
    const defaults = state.defaults;

    const priorityTooltip = state.v3Scheduler
        ? "\n\n" + tr.deckConfigBuryPriorityTooltip()
        : "";

    const settings = {
        buryNewSiblings: {
            title: tr.deckConfigBuryNewSiblings(),
            help: tr.deckConfigBuryNewTooltip() + priorityTooltip,
        },
        buryReviewSiblings: {
            title: tr.deckConfigBuryReviewSiblings(),
            help: tr.deckConfigBuryReviewTooltip() + priorityTooltip,
        },
        buryInterdayLearningSiblings: {
            title: tr.deckConfigBuryInterdayLearningSiblings(),
            help: tr.deckConfigBuryInterdayLearningTooltip() + priorityTooltip,
        },
    };
    const helpSections = Object.values(settings) as Section[];
</script>

<TitledContainer title={tr.deckConfigBuryTitle()}>
    <WithHelpModal
        title={tr.deckConfigBuryTitle()}
        url={HelpPage.Studying.siblingsAndBurying}
        {helpSections}
        let:openHelp
    >
        <DynamicallySlottable slotHost={Item} {api}>
            <Item>
                <SwitchRow bind:value={$config.buryNew} defaultValue={defaults.buryNew}>
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("buryNewSiblings"))}
                        >{settings.buryNewSiblings.title}</SettingLabel
                    >
                </SwitchRow>
            </Item>

            <Item>
                <SwitchRow
                    bind:value={$config.buryReviews}
                    defaultValue={defaults.buryReviews}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(
                                Object.keys(settings).indexOf("buryReviewSiblings"),
                            )}>{settings.buryReviewSiblings.title}</SettingLabel
                    >
                </SwitchRow>
            </Item>

            {#if state.v3Scheduler}
                <Item>
                    <SwitchRow
                        bind:value={$config.buryInterdayLearning}
                        defaultValue={defaults.buryInterdayLearning}
                    >
                        <SettingLabel
                            on:click={() =>
                                openHelp(
                                    Object.keys(settings).indexOf(
                                        "buryInterdayLearningSiblings",
                                    ),
                                )}
                            >{settings.buryInterdayLearningSiblings.title}</SettingLabel
                        >
                    </SwitchRow>
                </Item>
            {/if}
        </DynamicallySlottable>
    </WithHelpModal>
</TitledContainer>
