<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import Modal from "components/Modal.svelte";

    import Badge from "components/Badge.svelte";
    import HelpSection from "./HelpSection.svelte";
    import type { Section } from "./HelpSection.svelte";
    import { helpIcon, manualIcon } from "./icons";
    import ScrollArea from "./ScrollArea.svelte";

    export let title: string;
    export let url: string;
    export let startIndex = 0;
    export let helpSections: Section[];

    const rtl = window.getComputedStyle(document.body).direction == "rtl";

    let activeIndex = startIndex;

    let showModal = false;
    export function openHelp(chapterIndex = startIndex): void {
        activeIndex = chapterIndex;
        showModal = true;
    }
</script>

<Modal {title} show={showModal} breakpoint="sm">
    <div class="help-modal">
        <div class="header">
            {#if url}
                <a class="manual-badge" href={url}>
                    <Badge
                        iconSize={120}
                        tooltip={tr.helpOpenManualChapter({ name: title })}
                    >
                        {@html manualIcon}
                    </Badge>
                </a>
            {/if}
            <h1>{title}</h1>
        </div>
        <nav>
            <ul>
                {#each helpSections as section, i}
                    <li
                        tabindex="-1"
                        on:keydown={(e) => {
                            if (e.key === "Enter") {
                                activeIndex = i;
                            }
                        }}
                        on:click={() => (activeIndex = i)}
                    >
                        <span class="section-name" class:active={i == activeIndex}>
                            {section.title}
                        </span>
                    </li>
                {/each}
            </ul>
        </nav>
        <div class="body">
            <ScrollArea>
                {#each helpSections as section, i}
                    <div class="section-content" class:active={i == activeIndex}>
                        <HelpSection {section} />
                    </div>
                {/each}
            </ScrollArea>
        </div>
    </div>
</Modal>

<div class="help-modal-relative">
    <div class="help-badge" class:rtl>
        <Badge iconSize={100} on:click={() => openHelp()}>
            {@html helpIcon}
        </Badge>
    </div>

    <slot {openHelp} />
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/feedback";

    .help-modal-relative {
        position: relative;
    }

    .help-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        color: colors.$fg-subtle;
        transition: color props.$transition linear;
        &:hover {
            transition: none;
            color: colors.$fg;
        }
        &.rtl {
            right: unset;
            left: 10px;
        }
    }

    .help-modal {
        display: grid;
        grid-template:
            "header header" min-content
            "nav body" 1fr / min-content 1fr;

        .header {
            grid-area: header;
            display: flex;
        }
        .body {
            grid-area: body;
            display: flex;
            flex-direction: column;
        }
        nav {
            grid-area: nav;
            margin-bottom: 1.5rem;

            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;

                .section-name {
                    display: block;
                    padding: 0.5rem 0.75rem;
                    text-decoration: none;
                    cursor: pointer;
                    &:hover {
                        background-color: colors.$input-bg;
                    }
                    &.active {
                        border-left: 4px solid colors.$focus;
                    }
                }
            }
        }

        .section-content {
            display: none;
            &.active {
                display: block;
            }
        }
    }
</style>
