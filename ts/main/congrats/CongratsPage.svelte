<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeLink } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";
    import type { Scheduler } from "@tslib/proto";

    import Col from "../../components/Col.svelte";
    import TitledContainer from "../../components/TitledContainer.svelte";
    import { buildNextLearnMsg } from "./lib";

    export let info: Scheduler.CongratsInfoResponse;

    const congrats = tr.schedulingCongratulationsFinished();
    let nextLearnMsg: string;
    $: nextLearnMsg = buildNextLearnMsg(info);
    const today_reviews = tr.schedulingTodayReviewLimitReached();
    const today_new = tr.schedulingTodayNewLimitReached();

    const unburyThem = bridgeLink("unbury", tr.schedulingUnburyThem());
    const buriedMsg = tr.schedulingBuriedCardsFound({ unburyThem });
    const customStudy = bridgeLink("customStudy", tr.schedulingCustomStudy());
    const customStudyMsg = tr.schedulingHowToCustomStudy({
        customStudy,
    });
</script>

<div class="congrats-page">
    <TitledContainer
        --gutter-block="1rem"
        --gutter-inline="2px"
        title={congrats}
        breakpoint="xs"
    >
        <Col --col-justify="center">
            <p>{nextLearnMsg}</p>

            {#if info.reviewRemaining}
                <p>{today_reviews}</p>
            {/if}

            {#if info.newRemaining}
                <p>{today_new}</p>
            {/if}

            {#if info.bridgeCommandsSupported}
                {#if info.haveSchedBuried || info.haveUserBuried}
                    <p>
                        {@html buriedMsg}
                    </p>
                {/if}

                {#if !info.isFilteredDeck}
                    <p>
                        {@html customStudyMsg}
                    </p>
                {/if}
            {/if}

            {#if info.deckDescription}
                <div class="description">
                    {@html info.deckDescription}
                </div>
            {/if}
        </Col>
    </TitledContainer>
</div>

<style lang="scss">
    @use "sass/colors";

    .congrats-page {
        display: flex;
        justify-content: center;
        margin: 2em 1em 1em 1em;
        font-size: var(--font-size);

        :global(a) {
            color: colors.$link;
            text-decoration: none;
        }
    }

    .description {
        border: 1px solid colors.$border;
        padding: 1em;
    }
</style>
