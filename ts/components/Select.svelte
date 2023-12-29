<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { createEventDispatcher, setContext } from "svelte";
    import { writable } from "svelte/store";

    import { selectKey } from "./context-keys";
    import IconConstrain from "./IconConstrain.svelte";
    import { chevronDown } from "./icons";
    import Popover from "./Popover.svelte";
    import WithFloating from "./WithFloating.svelte";

    export let id: string | undefined = undefined;

    let className = "";
    export { className as class };

    export let disabled = false;
    export let label = "<br>";
    export let value = 0;

    const dispatch = createEventDispatcher();

    function setValue(v: number) {
        value = v;
        dispatch("change", { value });
    }

    export let element: HTMLElement | undefined = undefined;

    export let tooltip: string | undefined = undefined;

    const rtl = window.getComputedStyle(document.body).direction == "rtl";
    let hover = false;

    let showFloating = false;

    export function show(): void {
        showFloating = true;
    }
    let clientWidth: number;

    async function handleKey(e: KeyboardEvent) {
        if (e.code === "Enter") {
            e.preventDefault();
            showFloating = !showFloating;
        }
    }

    const selectStore = writable({ value, setValue });
    $: $selectStore.value = value;
    setContext(selectKey, selectStore);
</script>

<WithFloating
    bind:show={showFloating}
    offset={0}
    shift={0}
    hideArrow
    inline
    showOnClick
    closeOnInsideClick
    keepOnKeyup
>
    <div
        {id}
        class="{className} select-container"
        slot="reference"
        class:rtl
        class:hover
        class:disabled
        title={tooltip}
        tabindex="0"
        on:keypress={handleKey}
        on:mouseenter={() => (hover = true)}
        on:mouseleave={() => (hover = false)}
        on:click={() => (showFloating = !showFloating)}
        bind:this={element}
        bind:clientWidth
    >
        <div class="inner">
            <div class="label">{@html label}</div>
        </div>
        <div class="chevron">
            <IconConstrain iconSize={80}>
                {@html chevronDown}
            </IconConstrain>
        </div>
    </div>
    <Popover slot="floating" scrollable --popover-width="{clientWidth}px">
        <slot />
    </Popover>
</WithFloating>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/button-mixins" as button;

    $padding-inline: 0.5rem;

    .select-container {
        @include button.select($with-disabled: false);
        line-height: 1.5;
        height: 100%;
        position: relative;
        display: flex;
        flex-flow: row;
        justify-content: space-between;

        .inner {
            flex-grow: 1;
            position: relative;
            .label {
                position: absolute;
                top: 0;
                right: $padding-inline;
                bottom: 0;
                left: $padding-inline;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        }

        &.disabled {
            opacity: props.$opacity-disabled;
        }
    }

    .chevron {
        height: 100%;
        align-self: flex-end;
        border-left: 1px solid colors.$border-subtle;
    }

    :global([dir="rtl"]) {
        .chevron {
            border-left: none;
            border-right: 1px solid colors.$border-subtle;
        }
    }
</style>
