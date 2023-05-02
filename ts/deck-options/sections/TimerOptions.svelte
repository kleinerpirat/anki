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
    import SpinBoxRow from "../SpinBoxRow.svelte";
    import SwitchRow from "../SwitchRow.svelte";
    import type { Section } from "components/HelpSection.svelte";
    import Warning from "../Warning.svelte";

    export let state: DeckOptionsState;
    export let api: Record<string, never>;

    const config = state.currentConfig;
    const defaults = state.defaults;

    $: maximumAnswerSecondsAboveRecommended =
        $config.capAnswerTimeToSecs > 600
            ? tr.deckConfigMaximumAnswerSecsAboveRecommended()
            : "";

    const settings = {
        maximumAnswerSecs: {
            title: tr.deckConfigMaximumAnswerSecs(),
            help: tr.deckConfigMaximumAnswerSecsTooltip(),
        },
        showAnswerTimer: {
            title: tr.schedulingShowAnswerTimer(),
            help: tr.deckConfigShowAnswerTimerTooltip(),
        },
    };
    const helpSections = Object.values(settings) as Section[];
</script>

<TitledContainer title={tr.deckConfigTimerTitle()}>
    <WithHelpModal
        title={tr.deckConfigTimerTitle()}
        url={HelpPage.DeckOptions.timer}
        {helpSections}
        let:openHelp
    >
        <DynamicallySlottable slotHost={Item} {api}>
            <Item>
                <SpinBoxRow
                    bind:value={$config.capAnswerTimeToSecs}
                    defaultValue={defaults.capAnswerTimeToSecs}
                    min={1}
                    max={7200}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(
                                Object.keys(settings).indexOf("maximumAnswerSecs"),
                            )}>{settings.maximumAnswerSecs.title}</SettingLabel
                    >
                </SpinBoxRow>
            </Item>

            <Item>
                <Warning warning={maximumAnswerSecondsAboveRecommended} />
            </Item>

            <Item>
                <!-- AnkiMobile hides this -->
                <div class="show-timer-switch" style="display: contents;">
                    <SwitchRow
                        bind:value={$config.showTimer}
                        defaultValue={defaults.showTimer}
                    >
                        <SettingLabel
                            on:click={() =>
                                openHelp(
                                    Object.keys(settings).indexOf("showAnswerTimer"),
                                )}>{settings.showAnswerTimer.title}</SettingLabel
                        >
                    </SwitchRow>
                </div>
            </Item>
        </DynamicallySlottable>
    </WithHelpModal>
</TitledContainer>
