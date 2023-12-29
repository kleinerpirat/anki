<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Col from "../components/Col.svelte";
    import Row from "../components/Row.svelte";
    import WithRevertButton from "../components/WithRevertButton.svelte";
    import SettingLabel from "./SettingLabel.svelte";

    export let value: string;
    export let title: string;
</script>

<Row>
    <Col>
        <div class="text">
            <WithRevertButton class="flex-grow-1" bind:value defaultValue="">
                <SettingLabel on:click>{title}</SettingLabel>
            </WithRevertButton>
        </div>
    </Col>
</Row>

<textarea
    class="card-state-customizer"
    bind:value
    spellcheck="false"
    autocapitalize="none"
/>

<style lang="scss">
    @use "sass/colors";

    .text {
        width: 100%;
        min-height: 2em;
    }

    .card-state-customizer {
        background-color: colors.$canvas-code;
        border: 1px solid colors.$border-subtle;
        width: 100%;
        height: 10em;
        font-family: monospace;
    }

    @supports (-webkit-touch-callout: none) {
        // mobile compat
        .card-state-customizer {
            font-size: 16px;
            overflow-x: hidden;
        }
    }
</style>
