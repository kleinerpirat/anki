<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import ButtonGroup from "../components/ButtonGroup.svelte";
    import Col from "../components/Col.svelte";
    import LabelButton from "../components/LabelButton.svelte";
    import Row from "../components/Row.svelte";
    import Shortcut from "../components/Shortcut.svelte";
    import * as tr from "../lib/ftl";
    import { getPlatformString } from "../lib/shortcuts";

    export let path: string;
    export let onImport: () => void;

    const keyCombination = "Control+Enter";

    function basename(path: String): String {
        return path.split(/[\\/]/).pop()!;
    }
</script>

<div class="footer">
    <Row --cols={5}>
        <Col --col-size={4}>{basename(path)}</Col>
        <Col --col-justify="end">
            <ButtonGroup size={2}>
                <LabelButton
                    theme="primary"
                    tooltip={getPlatformString(keyCombination)}
                    on:click={onImport}
                    --border-left-radius="5px"
                    --border-right-radius="5px"
                >
                    {tr.actionsImport()}
                </LabelButton>
                <Shortcut {keyCombination} on:action={onImport} />
            </ButtonGroup>
        </Col>
    </Row>
</div>

<style lang="scss">
    .footer {
        margin: 1em;
        & :global(.row) {
            min-height: initial;
        }
    }
</style>
