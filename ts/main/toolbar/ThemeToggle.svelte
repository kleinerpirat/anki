<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { pageTheme } from "sveltelib/theme";
    import { bridgeCommand } from "@tslib/bridgecommand";
    import Badge from "components/Badge.svelte";
    import { darkIcon, lightIcon } from "../icons";
</script>

<div
    class="theme-switch"
    title={tr.preferencesToggleTheme()}
    on:click={() => bridgeCommand("toggleTheme")}
>
    <Badge>
        {@html $pageTheme.isDark ? lightIcon : darkIcon}
    </Badge>
</div>

<style lang="scss">
    @use "sass/feedback";

    .theme-switch {
        --icon-align: -webkit-baseline-middle;
        padding-inline-end: 5px;
        display: inline-block;
    }
</style>
