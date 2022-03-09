<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { handleClick } from "./lib";

    import Container from "../components/Container.svelte";
    import Deck from "./Deck.svelte";
    import Header from "./Header.svelte";
    import NavBar from "./NavBar.svelte";
    import Overview from "./Overview.svelte";

    export let args: any;
    export function refresh(newArgs): void {
        args = newArgs;
    }
    $: top = JSON.parse(args.tree);
    $: curDeck = args.curDeck;
</script>

<Container>
    <NavBar />

    <Container --gutter-block="1rem" --gutter-inline="2px" breakpoint="xs">
        <div on:click={handleClick}>
            <Header />

            {#each top.children as child}
                <Deck node={child} current={child.deckId == curDeck} />
            {/each}
        </div>
    </Container>

    <Overview />
</Container>

<style lang="scss">
</style>
