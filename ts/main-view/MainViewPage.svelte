<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Container from "../components/Container.svelte";
    import DeckBrowser from "./deck-browser/DeckBrowser.svelte";
    import Deck from "./deck-browser/Deck.svelte";
    import Navigation from "./navigation/Navigation.svelte";
    import Overview from "./Overview.svelte";

    export let args: any;
    export function refresh(newArgs): void {
        args = newArgs;
    }
    export function setSyncStatus(active: boolean): void {
        return;
    }
    export function updateSyncColor(active: boolean): void {
        return;
    }
    $: top = JSON.parse(args.tree);
    $: curDeck = args.curDeck;
    $: profileName = args.profileName;
</script>

<Navigation {profileName} />

<DeckBrowser>
    {#each top.children as child}
        <Deck node={child} current={child.deckId == curDeck} />
    {/each}
</DeckBrowser>

<Overview />

<style lang="scss">
</style>
