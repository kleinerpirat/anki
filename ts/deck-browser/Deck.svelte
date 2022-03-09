<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { slide } from "svelte/transition";
    import * as tr from "../lib/ftl";
    import { chevronDownIcon, chevronRightIcon } from "./icons";
    import IconConstrain from "../components/IconConstrain.svelte";
    import Col from "../components/Col.svelte";
    import Row from "../components/Row.svelte";
    import Options from "./Options.svelte";

    export let node: any;
    export let current = false;
    console.log(node);
</script>

<div data-did={node.deckId} transition:slide={{ duration: 200 }}>
    <Row --cols={8} --gutter-block="0.2rem">
        <Col --col-size={5}>
            <div
                class="deck-container align-self-stretch"
                class:empty={!(node.newCount || node.learnCount || node.reviewCount)}
                style="--level: {node.level}"
            >
                <IconConstrain iconSize={60}>
                    {@html node.children
                        ? node.collapsed
                            ? chevronRightIcon
                            : chevronDownIcon
                        : ""}
                </IconConstrain>
                <span class="deck">{node.name}</span>
            </div>
            {#if current}
                <Options node />
            {/if}
        </Col>
        <Col --col-justify="flex-end">
            <span
                class="new-count"
                class:zero-count={!node.newCount}
                title={tr.actionsNew()}
            >
                {node.newCount || 0}
            </span>
        </Col>
        <Col --col-justify="flex-end">
            <span
                class="learn-count"
                class:zero-count={!node.learnCount}
                title={tr.schedulingLearning()}
            >
                {node.learnCount || 0}
            </span>
        </Col>
        <Col --col-justify="flex-end">
            <span
                class="review-count"
                class:zero-count={!node.reviewCount}
                title={tr.schedulingReview()}
            >
                {node.reviewCount || 0}
            </span>
        </Col>
    </Row>
</div>
{#if node.children && !node.collapsed}
    {#each node.children as child}
        <svelte:self node={child} />
    {/each}
{/if}

<style lang="scss">
    span[class*="count"] {
        text-align: right;
        &:not(.zero-count) {
            cursor: pointer;
        }
    }
    .deck-container {
        cursor: pointer;
        margin-left: calc(var(--level) * 1.5em);
    }
    .deck {
        border-radius: 0.5rem;
        cursor: pointer;
        &:hover {
            background: var(--highlight-bg);
        }
    }
</style>
