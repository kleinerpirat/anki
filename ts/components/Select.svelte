<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "../lib/ftl";
    import { pageTheme } from "../sveltelib/theme";
    import { createEventDispatcher, onMount } from "svelte";
    import { slide } from "svelte/transition";
    import IconConstrain from "./IconConstrain.svelte";
    import { chevronIcon, revertIcon, crossIcon } from "./icons";
    import type { SelectOption } from "./types";
    let rtl = window.getComputedStyle(document.body).direction == "rtl";

    let el: HTMLDivElement;
    export let id: string | undefined = undefined;
    let className: string | undefined = undefined;
    export { className as class };
    export let value: number = 0;
    export let options: string[];
    export let name: string | undefined = undefined;
    export let title: string | undefined = undefined;
    export let placeholder: string | undefined = undefined;
    export let noOptionsMessage: string | undefined = undefined;
    export let tabindex: number = -1;
    export let isButton: boolean = false;
    export let disabled: boolean = false;
    export let searchable: boolean = true;
    export let clearable: boolean = true;

    $: btnClass = isButton ? ($pageTheme.isDark ? "btn-night" : "btn-day") : "";
    let fallbackOption: SelectOption = placeholder
        ? { name: placeholder, idx: -1 }
        : { name: options[0], idx: 0 };
    let optionsList: SelectOption[] = [fallbackOption];
    $: for (let i = 0; i < options.length; i++) {
        optionsList[i] = { name: options[i], idx: i };
    }

    let selected: SelectOption = optionsList[value] || fallbackOption;

    const dispatch = createEventDispatcher();
    onMount(() => dispatch("mount", el));

    let activeOption: SelectOption;
    let input: HTMLInputElement;
    let searchText: string;
    let optionsExpanded = false;

    $: matchingOptions = searchText
        ? optionsList.filter((option) =>
              option.name.toLowerCase().includes(searchText.toLowerCase()),
          )
        : optionsList;
    $: if (
        (activeOption && !matchingOptions.includes(activeOption)) ||
        (!activeOption && searchText)
    )
        activeOption = matchingOptions[0];

    function selectOption(item: SelectOption) {
        if (item === activeOption) return;
        selected = item;
        collapseOptions();
        dispatch("change", selected);
    }

    function clear() {
        selected = fallbackOption;
        dispatch("change", selected);
    }
    function expandOptions(): void {
        optionsExpanded = true;
        input?.focus();
    }
    function collapseOptions(): void {
        optionsExpanded = false;
        input?.blur();
    }
    function handleKeydown(event: KeyboardEvent) {
        switch (event.key) {
            case "Enter": {
                if (activeOption) {
                    selectOption(activeOption);
                } else expandOptions();
                break;
            }
            case "ArrowDown":
            case "ArrowUp": {
                const increment = event.key === "ArrowUp" ? -1 : 1;
                const newActiveIdx = matchingOptions.indexOf(activeOption) + increment;
                if (newActiveIdx < 0) {
                    activeOption = matchingOptions[matchingOptions.length - 1];
                } else {
                    if (newActiveIdx === matchingOptions.length)
                        activeOption = matchingOptions[0];
                    else activeOption = matchingOptions[newActiveIdx];
                }
                break;
            }
            case "Backspace": {
                if (!searchText) {
                    selected = fallbackOption;
                    searchText = "";
                }
                break;
            }
        }
    }

    $: isSelected = (option: SelectOption) => {
        return selected === option;
    };

    const handleEnterAndSpaceKeys = (handler: () => void) => (event: KeyboardEvent) => {
        if (["Enter", "Space"].includes(event.code)) {
            event.preventDefault();
            handler();
        }
    };
</script>

<div
    {id}
    class="select d-flex position-relative align-items-center {className} {btnClass}"
    class:rtl
    class:optionsExpanded
    {name}
    {title}
    {disabled}
    {tabindex}
    on:click={expandOptions}
    on:blur={collapseOptions}
    on:blur={() => dispatch("blur")}
    bind:this={el}
>
    <ul class="items d-flex flex-wrap">
        <li on:click={expandOptions}>
            {selected.name}
        </li>
        {#if searchable}
            <input
                bind:this={input}
                autocomplete="off"
                bind:value={searchText}
                on:click={expandOptions}
                on:keydown|preventDefault|stopPropagation={handleKeydown}
                on:blur={collapseOptions}
                on:blur={() => dispatch("blur")}
            />
        {/if}
    </ul>
    {#if clearable}
        <div
            type="button"
            class="clear-btn"
            title={tr.actionsClearSelection()}
            on:click={() => clear()}
            on:keydown={handleEnterAndSpaceKeys(clear)}
            style={selected == fallbackOption ? "display: none;" : ""}
        >
            <IconConstrain iconSize={50}>{@html crossIcon}</IconConstrain>
        </div>
    {/if}
    <IconConstrain id="chevronIcon" iconSize={50}>{@html chevronIcon}</IconConstrain>

    {#if optionsExpanded}
        <ul
            class="options"
            class:hidden={!optionsExpanded}
            in:slide={{ duration: 150 }}
        >
            {#each matchingOptions as option}
                <li
                    on:mousedown|preventDefault|stopPropagation={() => {
                        selectOption(option);
                    }}
                    class:selected={isSelected(option)}
                    class:active={activeOption === option}
                >
                    {option.name}
                </li>
            {:else}
                {noOptionsMessage}
            {/each}
        </ul>
    {/if}
</div>

<style lang="scss">
    @use "sass/button-mixins" as button;

    .select {
        height: 100%;
        background: var(--frame-bg);
        border: 1px solid var(--medium-border);
        border-radius: 0.25rem;
        line-height: 1.5;
        &:active {
            border-color: var(--focus-border);
        }
        input {
            color: var(--text-fg);
            border: none;
            outline: none;
            background: none;
            min-width: 2em;
            cursor: text;
        }
    }
    .clear-btn {
        color: var(--slightly-grey-text);
        border: none;
        outline: none;
        opacity: 0.6;
        align-items: center;
        border-radius: 50%;
        display: flex;
        transition: 0.2s;
        &:focus,
        :hover {
            opacity: 1;
            transform: scale(1.1);
        }
    }

    ul {
        li {
            cursor: pointer;
        }
        &.items {
            padding: 0;
            margin: 0;
            flex: 1;
            li {
                align-items: center;
                border-radius: 0.25rem;
                display: flex;
                margin: 2px;
                padding: 0 0 0 1em;
                transition: 0.3s;
                white-space: nowrap;
                height: 16px;
            }
        }
        &.options {
            z-index: 1;
            list-style: none;
            max-height: 80vh;
            padding: 0;
            top: 100%;
            width: 100%;
            position: absolute;
            border-radius: 0.25rem;
            overflow: auto;
            background: var(--frame-bg);
            &.hidden {
                visibility: hidden;
            }
            li {
                padding: 3px 2em;
                border-left: 3px solid transparent;
                &.active {
                    background: var(--border);
                }
                &.selected {
                    border-left-color: var(--highlight-bg);
                    background: var(--medium-border);
                }
            }
            li:not(.selected):hover {
                border-left-color: var(--focus-shadow);
            }
        }
    }

    @include button.btn-day($with-hover: false, $with-active: false);
    @include button.btn-night($with-hover: false, $with-active: false);
</style>
