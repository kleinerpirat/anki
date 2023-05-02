<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { withoutUnicodeIsolation } from "@tslib/i18n";
    import { slide } from "svelte/transition";

    import Row from "../components/Row.svelte";

    export let warning: string;
</script>

{#if warning}
    <Row>
        <div class="warning" in:slide out:slide>
            {withoutUnicodeIsolation(warning)}
        </div>
    </Row>
{/if}

<style lang="scss">
    @use "sass/props";
    @use "sass/feedback";

    .warning {
        position: relative;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: props.$border-radius;
    }
</style>
