<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "../lib/ftl";
    import Row from "../components/Row.svelte";
    import Col from "../components/Col.svelte";
    import Select from "../components/Select.svelte";
    import type { ChangeNotetypeState, MapContext } from "./lib";
    import type { SelectOption } from "../components/types";


    export let state: ChangeNotetypeState;
    export let ctx: MapContext;
    export let newIndex: number;

    let info = state.info;

    function onChange(evt: CustomEvent<SelectOption>) {
        const oldIdx = evt.detail.idx;
        state.setOldIndex(ctx, newIndex, oldIdx);
    }
</script>

<Row --cols={2}>
    <Col --col-size={1}>
        <!-- svelte-ignore a11y-no-onchange -->
        <Select
            class="flex-grow-1"
            options={$info.getOldNames(ctx)}
            value={$info.getOldIndex(ctx, newIndex)}
            placeholder={tr.changeNotetypeNothing()}
            on:change={onChange}
        />
    </Col>
    <Col --col-size={1}>
        {$info.getNewName(ctx, newIndex)}
    </Col>
</Row>
