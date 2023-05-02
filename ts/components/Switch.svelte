<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    export let id: string | undefined;
    export let value: boolean;
    export let disabled = false;
    export let label = "";
</script>

<div class="switch">
    <label for="switch">
        {label}
    </label>
    <input
        {id}
        type="checkbox"
        name="switch"
        class="switch-input"
        bind:checked={value}
    />
    <div class="toggle" />
</div>

<style lang="scss">
    @use "sass/colors";

    .switch {
        display: flex;

        input {
            opacity: 0; // hides checkbox
            position: absolute;
            & + .toggle {
                position: relative;
                display: inline-block;
                user-select: none;
                transition: 0.4s ease;
                height: 30px;
                width: 50px;
                border: 1px solid colors.$border-subtle;
                border-radius: 60px;

                &::before,
                &::after {
                    content: "";
                    position: absolute;
                    display: block;
                }
                &:before {
                    transition: 0.2s cubic-bezier(0.24, 0, 0.5, 1);
                    height: 30px;
                    width: 51px;
                    top: 0;
                    left: 0;
                    border-radius: 30px;
                }
                &:after {
                    box-shadow: 0 0 0 1px hsla(0, 0%, 0%, 0.1),
                        0 4px 0px 0 hsla(0, 0%, 0%, 0.04),
                        0 4px 9px hsla(0, 0%, 0%, 0.13), 0 3px 3px hsla(0, 0%, 0%, 0.05);
                    transition: 0.35s cubic-bezier(0.54, 1.6, 0.5, 1);
                    background: colors.$canvas-secondary;
                    height: 28px;
                    width: 28px;
                    top: 1px;
                    left: 0px;
                    border-radius: 60px;
                }
            }
            &:checked {
                & + .toggle:before {
                    background: colors.$accent-primary;
                    transition: width 0.2s cubic-bezier(0, 0, 0, 0.1);
                }
                & + .toggle:after {
                    left: 54px - 30px;
                }
            }
        }
    }
</style>
