<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import ColorPicker from "../../components/ColorPicker.svelte";
    import WithRevertButton from "../../components/WithRevertButton.svelte";
    import WithTooltip from "../../components/WithTooltip.svelte";

    import { validateColor } from "./utils";

    export let name: string;
    export let comment: string;
    export let value: string;
    export let defaultValue: string;

    let input: HTMLInputElement;
    let valid = validateColor(value);

    function setColor({ currentTarget }: Event): void {
        const color = (currentTarget! as HTMLInputElement).value;
        valid = validateColor(color);

        if (valid) {
            value = color;
        }
    }
</script>

<div class="color">
    <WithRevertButton bind:value {defaultValue} withPopover={false}>
        <span class="name">
            <div class="swatch" style="background: {value}">
                <ColorPicker {value} on:input={setColor} />
            </div>
            <WithTooltip tooltip={comment}>
                {`${name.replace(/_/g, "-").toLowerCase()}: `}
            </WithTooltip>
        </span>
        <input
            class="color-input"
            class:invalid={!valid}
            data-name={name}
            type="text"
            {value}
            bind:this={input}
            on:input={setColor}
        />
    </WithRevertButton>
</div>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";
    @use "sass/elevation" as *;
    @use "sass/background-mixins" as background;

    .color {
        padding: 0.25rem;
        margin-top: 0.25rem;
    }
    .name,
    input {
        font-size: 12px;
        padding: 0.2rem;
        font-family: Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace;
    }
    .swatch {
        display: inline-block;
        background: attr(data-color);
        min-width: 20px;
        min-height: 20px;
        width: 20px;
        height: 20px;
        border: colors.$border;
        border-radius: props.$border-radius;
        @include elevation(3);

        &:hover {
            @include elevation(4);
        }
        margin-right: 0.5rem;
    }
    input {
        display: block;
        border: 1px solid colors.$border-subtle;
        outline: none;
        background: colors.$canvas-secondary;
        border-radius: props.$border-radius;
        direction: ltr;
        width: 90%;

        &:focus,
        &.invalid {
            outline-offset: -1px;
            outline: 2px solid !important;
        }
        &:focus {
            outline-color: colors.$focus !important;
        }
        &.invalid {
            outline-color: colors.$warning !important;
        }
    }
</style>
