<script lang="ts">
    import * as tr from "@tslib/ftl";
    import type { AnswerArgs, QuestionArgs } from "./types";
    import { Side } from "./types";
    import { bridgeCommand } from "./Reviewer.svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import type { AnswerButton } from "./types";

    export let side: Side;
    export let time: number;

    export let maxTime = 0;
    export let args: AnswerArgs | QuestionArgs;

    let answerButtons: AnswerButton[];

    $: if (side === Side.BACK) {
        answerButtons = (args as AnswerArgs).answerButtons;
    }

    let timeNode: HTMLElement;
    let timeString: string;
    let maxTimeReached = false;

    onMount(() => {
        updateTime();
        setInterval(function () {
            time += 1;
            updateTime();
        }, 1000);
    });

    function updateTime(): void {
        if (maxTime === 0) {
            timeString = "";
            return;
        }
        time = Math.min(maxTime, time);
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timeString = `${minutes}:${String(seconds).padStart(2, "0")}`;
        maxTimeReached = maxTime === time;
    }

    const dispatch = createEventDispatcher();
</script>

<button
    title={tr.actionsShortcutKey({ val: tr.studyingSpace() })}
    id="ansbut"
    on:click={() => bridgeCommand("ans")}
>
    {tr.studyingShowAnswer()}
    <!--
    <span class="stattxt">{args.remaining}</span>
    -->
</button>

{#if side === Side.BACK}
    <div class="answer-buttons">
        {#each answerButtons as button, i}
            <button
                class:default-ease={button.default}
                title={tr.actionsShortcutKey({ val: i })}
                data-ease={i}
                on:focus={() => dispatch("select", { index: i })}
                on:click={() => bridgeCommand(`ease${i}`)}
            >
                {@html button.label + button.due}
            </button>
        {/each}
    </div>
{/if}

<div class="time" bind:this={timeNode} class:maxed={maxTimeReached}>
    {timeString}
</div>

<style lang="scss">
    @use "sass/colors";

    .time {
        &.maxed {
            color: colors.$warning;
        }
    }
</style>
