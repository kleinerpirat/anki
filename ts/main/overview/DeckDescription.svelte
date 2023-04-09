<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { marked } from "marked";

    import { bridgeCommand } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";
    import IconButton from "../../components/IconButton.svelte";
    import { descriptionAcceptIcon, descriptionEditIcon } from "../icons";

    let initialDescriptionText: string;
    export { initialDescriptionText as descriptionText };

    export let isDyn: boolean;
    export let markdown: boolean;

    let editing = false;
    let descriptionText = initialDescriptionText;

    function stripHTML(str: string) {
        const el = document.createElement("div");
        el.innerHTML = str;
        return el.innerText;
    }

    $: if (!editing && descriptionText !== initialDescriptionText) {
        bridgeCommand(
            `description:${markdown}:${
                markdown ? stripHTML(descriptionText) : descriptionText
            }`,
        );
    }
</script>

<div class="description-container" class:dyn={isDyn} class:editing>
    {#if isDyn}
        <p>
            {tr.studyingThisIsASpecialDeckFor()}
            {tr.studyingCardsWillBeAutomaticallyReturnedTo()}
            {tr.studyingDeletingThisDeckFromTheDeck()}
        </p>
    {:else}
        <div class="description">
            {@html markdown ? marked(descriptionText) : descriptionText}
        </div>
        {#if editing}
            <textarea
                bind:value={descriptionText}
                placeholder={markdown
                    ? tr.deckConfigEnterDescriptionInMarkdown()
                    : tr.deckConfigEnterDescriptionInHtml()}
            />
        {/if}
        <div class="description-ui">
            <div>
                <label
                    for="md-checkbox"
                    title={tr.deckConfigDescriptionNewHandlingHint()}
                >
                    {tr.deckConfigDescriptionNewHandling()}
                </label>
                <input id="md-checkbox" type="checkbox" bind:checked={markdown} />
            </div>

            <div class="description-edit">
                <IconButton
                    iconSize={150}
                    tooltip={editing
                        ? tr.deckConfigAcceptDescription()
                        : tr.deckConfigEditDescription()}
                    on:click={() => (editing = !editing)}
                >
                    {#if editing}
                        {@html descriptionAcceptIcon}
                    {:else}
                        {@html descriptionEditIcon}
                    {/if}
                </IconButton>
            </div>
        </div>
    {/if}
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/button-mixins" as button;

    .description-container {
        white-space: pre-wrap;
        margin: 0 auto 0;
        text-align: left;
        &.editing {
            color: colors.$fg-subtle;
            display: grid;
            grid-gap: 2em;
            grid-template:
                "description textarea" 9fr
                "ui ui" 1fr / 1fr 1fr;

            .description {
                backdrop-filter: blur(props.$blur);
                border: 1px solid colors.$border-subtle;
                border-radius: props.$border-radius;
            }
        }

        textarea {
            grid-area: textarea;
            padding: 0.5em 0.75em;
            color: colors.$fg;
            background: colors.$glass;
            backdrop-filter: blur(props.$blur);
            border-radius: props.$border-radius;
        }
        .description {
            grid-area: description;
            padding: 0.5em 0.75em;
            line-height: 1.2;
        }
        .description-ui {
            grid-area: ui;
            display: flex;
            width: 100%;
            justify-content: space-between;
            color: colors.$fg;
        }
        &.dyn {
            text-align: center;
        }
        &:empty {
            display: none;
        }
    }
</style>
