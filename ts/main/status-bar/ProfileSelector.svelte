<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";
    import IconConstrain from "components/IconConstrain.svelte";
    import { profileIcon } from "../icons";
    import WithFloating from "components/WithFloating.svelte";
    import Popover from "components/Popover.svelte";
    import DropdownItem from "components/DropdownItem.svelte";
    import type { MainPageArgs } from "main/types";

    export let profiles: MainPageArgs["profiles"];
</script>

<WithFloating offset={0} shift={0} hideArrow showOnClick closeOnInsideClick keepOnKeyup>
    <div class="profile-selector" slot="reference">
        <IconConstrain>
            {@html profileIcon}
        </IconConstrain>

        {profiles.current}
    </div>
    <Popover slot="floating" scrollable>
        {#each profiles.other as name}
            <DropdownItem on:click={() => bridgeCommand(`profile:${name}`)} tabbable>
                {name}
            </DropdownItem>
        {/each}
    </Popover>
</WithFloating>

<style lang="scss">
    @use "sass/feedback";

    .profile-selector {
        display: flex;
        align-items: center;
        height: 22px;
        gap: 5px;
        @include feedback.clickable;
    }
</style>
