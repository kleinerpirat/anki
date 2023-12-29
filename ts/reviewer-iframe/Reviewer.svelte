<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script context="module" lang="ts">
    import { maybePreloadExternalCss } from "./css";
    import { applyReviewerHacks } from "./lib";
    //import "css-browser-selector/css_browser_selector.min";
    // import { default as $, default as jQuery } from "jquery/dist/jquery";

    import { mutateNextCardStates } from "./answering";
    type Callback = () => void | Promise<void>;

    export function bridgeCommand(cmd: string) {
        window.parent.postMessage(
            { directive: "bridgeCommand", args: { cmd } },
            window.origin,
        );
    }
</script>

<script lang="ts">
    import { allImagesLoaded, maybePreloadImages, preloadAnswerImages } from "./images";

    import { renderError, runHook } from "./lib";
    import { refreshInsertedHTML } from "@tslib/helpers";
    import type { AnswerArgs, ContentPart, QuestionArgs } from "./types";
    import SoundLink from "./SoundLink.svelte";
    import { Side } from "./types";
    import { pageTheme } from "sveltelib/theme";
    import Badge from "components/Badge.svelte";
    import { flagIcon, markIcon } from "./icons";
    import type { IframeCommand } from "./types";
    import { tick } from "svelte";

    Object.assign(globalThis, {
        anki: globalThis.anki || {},
        ankiPlatform: "desktop",
        onUpdateHook: [] as Array<Callback>,
        onShownHook: [] as Array<Callback>,
        pycmd: bridgeCommand,
    });

    globalThis.anki.mutateNextCardStates = mutateNextCardStates;

    applyReviewerHacks();

    const urlParams = new URLSearchParams(window.location.search);
    let rtl = urlParams.get("rtl")!;

    let side: Side;
    let cardIndex: number;

    $: {
        document.body.classList.add("card", `card${cardIndex}`);
        document.body.classList.toggle("front", side === Side.FRONT);
        document.body.classList.toggle("back", side === Side.BACK);
        document.body.classList.toggle("night-mode", $pageTheme.isDark);
    }

    // Handle postMessages from ReviewerFrame
    window.addEventListener("message", (event) => {
        if (event.origin !== window.origin) {
            return;
        }
        const { directive, args } = event.data as IframeCommand;

        switch (directive) {
            case "showQuestion":
                const questionArgs = args as QuestionArgs;
                side = Side.FRONT;
                newContents = questionArgs.content;
                cardIndex = questionArgs.ord;

                // return to top of window
                window.scrollTo(0, 0);
                break;
            case "showAnswer":
                const answerArgs = args as AnswerArgs;
                side = Side.BACK;
                newContents = answerArgs.content;
                cardIndex = answerArgs.ord;
                break;
        }
    });

    function joinContents(contents: ContentPart[]): string {
        return contents.map((part) => part.content).join("");
    }

    $: (async () => {
        const plainHTML = joinContents(newContents);
        // prevent flash of unstyled content when external css used
        // prevent flickering & layout shift on image load

        await Promise.all([
            maybePreloadExternalCss(plainHTML),
            maybePreloadImages(plainHTML),
        ]);

        cardContents = newContents;
        await tick();
        await runHook(globalThis.onUpdateHook);
    })();

    window.parent.postMessage({ directive: "ready" }, window.origin);

    let cardContents: ContentPart[];
    let newContents: ContentPart[];

    let flagHidden = false;
    let markHidden = false;

    let error: string;
    function runUserContent(qa: HTMLElement) {
        globalThis.onUpdateHook.length = 0;
        globalThis.onShownHook.length = 0;

        try {
            refreshInsertedHTML(qa).then(async () => {
                if (side === Side.FRONT) {
                    // focus typing area if visible
                    const typeans = document.getElementById(
                        "typeans",
                    ) as HTMLInputElement;
                    if (typeans) {
                        typeans.focus();
                    }
                    // preload images
                    // allImagesLoaded().then(() => preloadAnswerImages(q, a));

                    // wait for mathjax to ready
                    await globalThis.MathJax.startup.promise
                        .then(() => {
                            // clear MathJax buffers from previous typesets
                            globalThis.MathJax.typesetClear();

                            return globalThis.MathJax.typesetPromise([qa]);
                        })
                        .catch(renderError("MathJax"));

                    await runHook(globalThis.onShownHook);
                } else {
                    // avoid scrolling to the answer until images load
                    allImagesLoaded().then(() =>
                        document.getElementById("answer")?.scrollIntoView(),
                    );
                }
            });
        } catch (error) {
            error = renderError("html")(error);
        }
    }
</script>

<div id="_mark" class:rtl hidden={markHidden}>
    <Badge>
        {@html markIcon}
    </Badge>
</div>
<div id="_flag" class:rtl hidden={flagHidden}>
    {@html flagIcon}
</div>
{#if error}
    <div class="error-message">
        {@html error}
    </div>
{:else if cardContents}
    <div id="qa" use:runUserContent>
        {#each cardContents as { type, content }}
            {#if type === 2}
                <SoundLink cmd={content} />
            {:else}
                {@html content}
            {/if}
        {/each}
    </div>
{/if}

<style lang="scss">
    #_flag,
    #_mark {
        position: fixed;
    }
    #_flag {
        inset: 10px 10px auto auto;
        &.rtl {
            left: 10px;
            right: auto;
        }
    }

    #_mark {
        inset: 0 auto auto 10px;
        left: 10px;
        &.rtl {
            right: 10px;
            left: auto;
        }
        color: yellow;
    }
</style>
