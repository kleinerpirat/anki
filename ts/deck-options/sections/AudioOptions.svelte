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

    const settings = {
        disableAutoplay: {
            title: tr.deckConfigDisableAutoplay(),
            help: tr.deckConfigDisableAutoplayTooltip(),
        },
        skipQuestionWhenReplaying: {
            title: tr.deckConfigSkipQuestionWhenReplaying(),
            help: tr.deckConfigAlwaysIncludeQuestionAudioTooltip(),
        },
    };
    const helpSections = Object.values(settings) as Section[];
</script>

<TitledContainer title={tr.deckConfigAudioTitle()}>
    <WithHelpModal
        title={tr.deckConfigAudioTitle()}
        url={HelpPage.DeckOptions.audio}
        {helpSections}
        let:openHelp
    >
        <DynamicallySlottable slotHost={Item} {api}>
            <Item>
                <SwitchRow
                    bind:value={$config.disableAutoplay}
                    defaultValue={defaults.disableAutoplay}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(Object.keys(settings).indexOf("disableAutoplay"))}
                        >{settings.disableAutoplay.title}</SettingLabel
                    >
                </SwitchRow>
            </Item>

            <Item>
                <SwitchRow
                    bind:value={$config.skipQuestionWhenReplayingAnswer}
                    defaultValue={defaults.skipQuestionWhenReplayingAnswer}
                >
                    <SettingLabel
                        on:click={() =>
                            openHelp(
                                Object.keys(settings).indexOf(
                                    "skipQuestionWhenReplaying",
                                ),
                            )}>{settings.skipQuestionWhenReplaying.title}</SettingLabel
                    >
                </SwitchRow>
            </Item>
        </DynamicallySlottable>
    </WithHelpModal>
</TitledContainer>
