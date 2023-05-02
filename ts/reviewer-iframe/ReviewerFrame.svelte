<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { fade } from "svelte/transition";
    import type { ReviewerArgs } from "./types";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import { Side } from "./types";
    import { pageTheme } from "sveltelib/theme";
    import type { IframeCommand } from "./types";
    import ReviewerUi from "./ReviewerUI.svelte";

    let args: ReviewerArgs;
    export { args as reviewerArgs };

    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    $: questionArgs = args.questionArgs;
    $: answerArgs = args.answerArgs;

    let side: Side;

    let selectedButton = 2;
    export function selectedAnswerButton(): number {
        return selectedButton;
    }

    let iframe: HTMLIFrameElement;
    let targetOrigin: string;

    let reviewerReady = false;

    const reviewerPromise = new Promise<void>((resolve) => {
        window.addEventListener(
            "message",
            function handleMessage(event) {
                if (event.data.directive === "ready") {
                    reviewerReady = true;
                    resolve();
                }
            },
            { once: true },
        );
    });

    // Update card inside iframe
    $: if (questionArgs) {
        (async () => {
            if (!reviewerReady) {
                await reviewerPromise;
            }
            side = Side.FRONT;
            iframe.contentWindow!.postMessage(
                { directive: "showQuestion", args: questionArgs },
                window.origin,
            );
        })();
    }
    $: if (answerArgs) {
        (async () => {
            if (!reviewerReady) {
                await reviewerPromise;
            }
            side = Side.FRONT;
            iframe.contentWindow!.postMessage(
                { directive: "showAnswer", args: answerArgs },
                window.origin,
            );
        })();
    }

    // Handle postMessages from Reviewer inside iframe
    window.addEventListener("message", (event) => {
        if (event.origin !== targetOrigin) {
            return;
        }
        const { directive, args } = event.data as IframeCommand;

        switch (directive) {
            case "bridgeCommand":
                bridgeCommand(args.cmd);
                break;
        }
    });
</script>

<iframe
    title="reviewer"
    src={`${args.serverURL}_anki/pages/reviewer-iframe.html#${
        $pageTheme.isDark ? "night" : ""
    }?rtl=${rtl}`}
    sandbox={[
        "allow-downloads",
        "allow-forms",
        "allow-modals",
        "allow-pointer-lock",
        "allow-popups",
        "allow-popups-to-escape-sandbox",
        "allow-same-origin",
        "allow-scripts",
    ].join(" ")}
    transition:fade
    bind:this={iframe}
/>

<ReviewerUi
    {side}
    on:select={(e) => (selectedButton = e.detail.index)}
    time={0}
    args={side === Side.FRONT ? questionArgs : answerArgs}
/>

<style lang="scss">
    iframe {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
    }
</style>
