<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { bridgeCommand } from "@tslib/bridgecommand";

    import { SyncStatus } from "./types";

    export let active = false;
    export let status: SyncStatus;
</script>

<a
    class="hitem"
    class:normal-sync={status === SyncStatus.NORMAL_SYNC}
    class:full-sync={status === SyncStatus.FULL_SYNC}
    tabindex="-1"
    aria-label={tr.qtMiscSync()}
    title={tr.actionsShortcutKey({ val: "Y" })}
    id="sync"
    on:click={() => bridgeCommand("sync")}
>
    {tr.qtMiscSync()}

    <!-- svelte-ignore a11y-missing-attribute -->
    <img id="sync-spinner" class:spin={active} src="/_anki/imgs/refresh.svg" />
</a>

<style lang="scss">
    @use "sass/colors";
    @use "sass/props";

    @keyframes spin {
        0% {
            -webkit-transform: rotate(0deg);
        }
        100% {
            -webkit-transform: rotate(360deg);
        }
    }

    .spin {
        width: 16px !important;
        animation: spin;
        animation-duration: 2s;
        animation-iteration-count: infinite;
        display: inline-block;
        visibility: visible !important;
        animation-timing-function: linear;
        transition: all props.$transition ease-in;
    }

    #sync-spinner {
        height: 16px;
        margin-bottom: -3px;
        visibility: hidden;
        width: 0;
    }

    .normal-sync {
        color: colors.$card-new !important;
    }

    .full-sync {
        color: colors.$card-learn !important;
    }
</style>
