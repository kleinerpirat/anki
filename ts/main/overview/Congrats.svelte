<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeLink } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";
    import { naturalUnit, unitAmount, unitName } from "@tslib/time";
    import type { Scheduler } from "@tslib/proto";

    export let info: Scheduler.CongratsInfoResponse;

    function buildNextLearnMsg(info: Scheduler.CongratsInfoResponse): string {
        const secsUntil = info.secsUntilNextLearn;
        // next learning card not due today?
        if (secsUntil >= 86_400) {
            return "";
        }

        const unit = naturalUnit(secsUntil);
        const amount = Math.round(unitAmount(unit, secsUntil));
        const unitStr = unitName(unit);
        const nextLearnDue = tr.schedulingNextLearnDue({
            amount,
            unit: unitStr,
        });
        const remaining = tr.schedulingLearnRemaining({
            remaining: info.learnRemaining,
        });
        return `${nextLearnDue} ${remaining}`;
    }

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
    <h2>{congrats}</h2>
    {#if nextLearnMsg}
        <p>{nextLearnMsg}</p>
    {/if}

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
</div>

<style lang="scss">
    @use "sass/colors";

    .congrats-page {
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
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
