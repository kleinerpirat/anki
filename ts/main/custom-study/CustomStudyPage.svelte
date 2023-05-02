<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { HelpPage } from "@tslib/help-page";

    import IconConstrain from "components/IconConstrain.svelte";
    import Container from "components/Container.svelte";
    import TitledContainer from "components/TitledContainer.svelte";
    import type { Section } from "components/HelpSection.svelte";

    import {
        reviewAheadIcon,
        reviewForgottenIcon,
        previewNewIcon,
        stateTagIcon,
        increaseNewIcon,
        increaseReviewIcon,
    } from "./icons";

    import type { CustomStudyOption } from "./types";
    import { CustomStudyMode } from "./types";
    import CustomStudySpinner from "./CustomStudySpinner.svelte";
    import WithHelpModal from "components/WithHelpModal.svelte";
    import Tile from "components/Tile.svelte";

    const options: CustomStudyOption[] = [
        {
            mode: CustomStudyMode.NEW_LIMIT,
            icon: increaseNewIcon,
            help: {
                title: tr.customStudyIncreaseTodaysNewCardLimit(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
        {
            mode: CustomStudyMode.REVIEW_LIMIT,
            icon: increaseReviewIcon,
            help: {
                title: tr.customStudyIncreaseTodaysReviewCardLimit(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
        {
            mode: CustomStudyMode.AHEAD,
            icon: reviewAheadIcon,
            help: {
                title: tr.customStudyReviewAhead(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
        {
            mode: CustomStudyMode.FORGOTTEN,
            icon: reviewForgottenIcon,
            help: {
                title: tr.customStudyReviewForgottenCards(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
        {
            mode: CustomStudyMode.PREVIEW,
            icon: previewNewIcon,
            help: {
                title: tr.customStudyPreviewNewCards(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
        {
            mode: CustomStudyMode.CRAM,
            icon: stateTagIcon,
            help: {
                title: tr.customStudyStudyByCardStateOrTag(),
                help: tr.deckConfigMaximumIntervalTooltip(),
                url: HelpPage.DeckOptions.maximumInterval,
            },
        },
    ];

    let activeMode: CustomStudyMode;

    function selectMode(mode: CustomStudyMode) {
        activeMode = mode;
    }
    const helpSections = Object.values(options).map(
        (option) => option.help,
    ) as Section[];
</script>

<WithHelpModal
    title={tr.deckConfigAudioTitle()}
    url={HelpPage.FilteredDecks.customStudy}
    {helpSections}
>
    <TitledContainer title={tr.actionsCustomStudy()} breakpoint="md">
        <div class="mode-selector">
            {#each options as { mode, icon, help }}
                <Tile {icon} text={help.title} on:click={() => selectMode(mode)} />
            {/each}
        </div>

        <div class="settings">
            {#if activeMode === CustomStudyMode.NEW_LIMIT}
                <CustomStudySpinner
                    label={tr.customStudyIncreaseTodaysNewCardLimitBy()}
                    value={0}
                >
                    <span slot="label">
                        {@html tr.customStudyAvailableNewCards({ count: 0 })}
                    </span>
                </CustomStudySpinner>
            {:else if activeMode === CustomStudyMode.REVIEW_LIMIT}
                <CustomStudySpinner
                    label={tr.customStudyIncreaseTodaysReviewLimitBy()}
                    value={0}
                >
                    <span slot="label">
                        {@html tr.customStudyAvailableReviewCards({ count: 0 })}
                    </span>
                </CustomStudySpinner>
            {:else if activeMode === CustomStudyMode.AHEAD}
                <CustomStudySpinner
                    label={tr.customStudyReviewCardsForgottenInLast()}
                    value={0}
                />
            {:else if activeMode === CustomStudyMode.FORGOTTEN}
                <CustomStudySpinner label={tr.customStudyReviewAheadBy()} value={0} />
            {:else if activeMode === CustomStudyMode.PREVIEW}
                <CustomStudySpinner
                    label={tr.customStudyPreviewNewCardsAddedInThe()}
                    value={0}
                />
            {/if}
        </div>
    </TitledContainer>
</WithHelpModal>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    .mode-selector {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1rem;
        @media (max-width: 800px) {
            grid-template: 1fr 1fr / repeat(3, 1fr);
        }
    }
</style>
