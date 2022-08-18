<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { marked } from "marked";

    import Page from "../components/Page.svelte";
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
</script>

<Page class="change-notetype-page" --gutter-inline="0.25rem">
    <NotetypeSelector {state} />

    <ScrollArea>
        <Row class="gx-0" --cols={2}>
            <Col --col-size={1} breakpoint="md">
                <ScrollArea>
                    <Container>
                        <Header {state} ctx={MapContext.Field} />
                        <Mapper {state} ctx={MapContext.Field} />
                    </Container>
                </ScrollArea>
            </Col>
            <Col --col-size={1} breakpoint="md">
                <ScrollArea>
                    <Container>
                        <Header {state} ctx={MapContext.Template} />
                        {#if $info.templates}
                            <Mapper {state} ctx={MapContext.Template} />
                        {:else}
                            <div>{@html marked(tr.changeNotetypeToFromCloze())}</div>
                        {/if}
                    </Container>
                </ScrollArea>
            </Col>
        </Row>
    </ScrollArea>
</Page>
