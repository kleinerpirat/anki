<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { marked } from "marked";

    import Col from "../components/Col.svelte";
    import Container from "../components/Container.svelte";
    import ScrollArea from "../components/ScrollArea.svelte";
    import Row from "../components/Row.svelte";
    import * as tr from "../lib/ftl";
    import { ChangeNotetypeState, MapContext } from "./lib";
    import Mapper from "./Mapper.svelte";
    import NotetypeSelector from "./NotetypeSelector.svelte";
    import Header from "./Header.svelte";

    export let state: ChangeNotetypeState;
    $: info = state.info;
    let offset: number;
</script>

<div bind:offsetHeight={offset}>
    <NotetypeSelector {state} />
</div>

<div class="change-notetype-page" style="--gutter-inline: var(--gutter-small);">
    <ScrollArea>
        <Row class="gx-0" --cols={2}>
            <Col --col-size={1} breakpoint="md">
                <Container>
                    <Header {state} ctx={MapContext.Field} />
                    <Mapper {state} ctx={MapContext.Field} />
                </Container>
            </Col>
            <Col --col-size={1} breakpoint="md">
                <Container>
                    <Header {state} ctx={MapContext.Template} />
                    {#if $info.templates}
                        <Mapper {state} ctx={MapContext.Template} />
                    {:else}
                        <div>{@html marked(tr.changeNotetypeToFromCloze())}</div>
                    {/if}
                </Container>
            </Col>
        </Row>
    </ScrollArea>
</div>

<style>
    .change-notetype-page {
        padding: 0;
        overflow: hidden auto;
        display: flex;
        flex-direction: column;
    }
</style>
