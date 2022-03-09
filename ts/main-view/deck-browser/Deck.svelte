<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { slide } from "svelte/transition";
    import * as tr from "../../lib/ftl";
    import { chevronDownIcon, chevronRightIcon } from "../icons";
    import IconConstrain from "../../components/IconConstrain.svelte";
    import Col from "../../components/Col.svelte";
    import Row from "../../components/Row.svelte";
    import Options from "./Options.svelte";

    export let node: any;
    export let current = false;
    $: parent = node.children && !node.collapsed;
</script>

<div
    class="deck"
    class:current
    class:parent
    data-did={node.deckId}
    transition:slide={{ duration: 200 }}
>
    <Row
        class="flex-nowrap"
        --cols={2}
        --gutter-block="0.2rem"
        --col-justify="flex-end"
    >
        <Col>
            <div
                class="deck-container"
                class:empty={!(node.newCount || node.learnCount || node.reviewCount)}
            >
                <span class="deck-name">
                    {#if node.children}
                        <IconConstrain iconSize={60}>
                            {@html node.collapsed ? chevronRightIcon : chevronDownIcon}
                        </IconConstrain>
                    {/if}
                    {node.name}
                </span>
            </div>
            {#if current}
                <Options node />
            {/if}
        </Col>
        <Col>
            <div
                class="new-count"
                class:zero-count={!node.newCount}
                title={tr.actionsNew()}
            >
                {node.newCount || 0}
            </div>

            <div
                class="learn-count"
                class:zero-count={!node.learnCount}
                title={tr.schedulingLearning()}
            >
                {node.learnCount || 0}
            </div>

            <div
                class="review-count"
                class:zero-count={!node.reviewCount}
                title={tr.schedulingReview()}
            >
                {node.reviewCount || 0}
            </div>
        </Col>
    </Row>

    {#if node.children && !node.collapsed}
        {#each node.children as child}
            <svelte:self node={child} />
        {/each}
    {/if}
</div>

<style lang="scss">
    div.deck {
        margin-left: clamp(10px, 5%, 24px);
        position: relative;
        &::before {
            content: "";
            position: absolute;
            opacity: 0;
            transition: opacity 0.3s ease-in;
            border-left: thin solid var(--zero-count);
            top: 20px;
            left: 10px;
            height: calc(100% - 24px);
        }
    }
    :global(.deck-browser:hover) div.deck.parent::before,
    div.deck.current.parent::before {
        opacity: 1;
    }
    div.deck.current.parent::before {
        opacity: 1;
        border-color: var(--border);
    }
    div[class*="count"] {
        text-align: right;
        margin-left: clamp(1rem, 5vw, 2rem);
        &:not(.zero-count) {
            cursor: pointer;
        }
    }
    .deck-container {
        cursor: pointer;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-right: auto;
    }
    .deck-name {
        border-radius: 0.5rem;
        cursor: pointer;
        &:hover {
            background: var(--highlight-bg);
        }
    }
</style>
