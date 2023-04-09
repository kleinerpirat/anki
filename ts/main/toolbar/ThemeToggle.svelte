<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { pageTheme } from "sveltelib/theme";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import IconConstrain from "components/IconConstrain.svelte";
    import { darkIcon, lightIcon } from "../icons";
</script>

<div
    class="theme-switch"
    title={tr.preferencesToggleTheme()}
    on:click={() => bridgeCommand("toggleTheme")}
>
    <IconConstrain>
        {@html $pageTheme.isDark ? lightIcon : darkIcon}
    </IconConstrain>
</div>

<style lang="scss">
    .theme-switch {
        display: inline-block;
        cursor: pointer;
    }
</style>
