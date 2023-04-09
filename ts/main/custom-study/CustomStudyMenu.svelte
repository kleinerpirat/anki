<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import IconConstrain from "components/IconConstrain.svelte";
    import Container from "components/Container.svelte";
    import {
        increaseLimitIcon,
        reviewAheadIcon,
        reviewForgottenIcon,
        previewNewIcon,
        stateTagIcon,
    } from "./icons";

    import type { CustomStudyOption } from "./types";
    import { CustomStudyMode } from "./types";

    const options: CustomStudyOption[] = [
        {
            mode: CustomStudyMode.INCREASE_NEW_LIMIT,
            desc: tr.customStudyIncreaseTodaysNewCardLimit(),
            icon: increaseLimitIcon,
        },
        {
            mode: CustomStudyMode.INCREASE_REVIEW_LIMIT,
            desc: tr.customStudyIncreaseTodaysReviewCardLimit(),
            icon: increaseLimitIcon,
        },
        {
            mode: CustomStudyMode.REVIEW_AHEAD,
            desc: tr.customStudyReviewAhead(),
            icon: reviewAheadIcon,
        },
        {
            mode: CustomStudyMode.REVIEW_FORGOTTEN,
            desc: tr.customStudyReviewForgottenCards(),
            icon: reviewForgottenIcon,
        },
        {
            mode: CustomStudyMode.PREVIEW,
            desc: tr.customStudyPreviewNewCards(),
            icon: previewNewIcon,
        },
        {
            mode: CustomStudyMode.CRAM,
            desc: tr.customStudyStudyByCardStateOrTag(),
            icon: stateTagIcon,
        },
    ];

    let activeMode: CustomStudyMode;

    function selectMode(mode: CustomStudyMode) {
        activeMode = mode;
    }
</script>

<h1>{tr.actionsCustomStudy()}</h1>

<div class="mode-selector">
    {#each options as { mode, desc, icon }}
        <div
            class="mode"
            class:active={activeMode === mode}
            on:click={() => selectMode(mode)}
        >
            <Container withBackground>
                <div class="mode-icon">
                    <IconConstrain iconSize={500}>
                        {@html icon}
                    </IconConstrain>
                </div>
                <span class="mode-desc">{desc}</span>
            </Container>
        </div>
    {/each}
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    .mode-selector {
        display: grid;
        gap: 1rem;
    }
    .mode {
        width: 150px;
        height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s ease-out;
    }

    .mode-icon {
        width: 50%;
        height: auto;
        margin-bottom: 1rem;
    }

    .mode-desc {
        font-size: 1.2rem;
        text-align: center;
    }

    .mode:hover {
        transform: scale(1.1);
        z-index: 1;
    }

    .mode.active {
        transform: scale(1.2);
        z-index: 2;
    }
</style>
