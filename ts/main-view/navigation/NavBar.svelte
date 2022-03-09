<script lang="ts">
    import * as tr from "../../lib/ftl";

    import Hamburger from "./Hamburger.svelte";
    import Profile from "./Profile.svelte";
    import Nav from "./Nav.svelte";
    import SyncButton from "./SyncButton.svelte";
    import ThemeButton from "./ThemeButton.svelte";
    import Fixed from "../../components/Fixed.svelte";

    export let sidebar = false;
    export let profileName: string;
</script>

<Fixed left top right>
    <header class="d-flex justify-content-between align-items-center">
        <Nav>
            <Hamburger bind:open={sidebar} />
        </Nav>

        <Nav>
            <Profile {profileName} />
            <ThemeButton />
            <SyncButton />
        </Nav>
    </header>
</Fixed>

<style lang="scss">
</style>
