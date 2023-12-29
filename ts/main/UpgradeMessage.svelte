<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";
    import * as tr from "@tslib/ftl";
</script>

<center>
    <div class="callout">
        <div>
            {tr.schedulingUpdateRequired()}
        </div>
        <div>
            <button on:click={() => bridgeCommand("v2upgrade")}>
                {tr.schedulingUpdateButton()}
            </button>
            <button on:click={() => bridgeCommand("v2upgradeinfo")}>
                {tr.schedulingUpdateMoreInfoButton()}
            </button>
        </div>
    </div>
</center>

<style lang="scss">
    @use "sass/colors";

    .callout {
        background: colors.$border;
        padding: 1em;
        margin: 1em;

        div {
            margin: 1em;
        }
    }
</style>
