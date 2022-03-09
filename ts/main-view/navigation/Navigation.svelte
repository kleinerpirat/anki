<script lang="ts">
    import NavBar from "./NavBar.svelte";
    import Sidebar from "./Sidebar.svelte";
    import Toolbar from "./Toolbar.svelte";

    let open = false;
    export let profileName: string;
</script>

<Sidebar bind:open>
    <Toolbar />
</Sidebar>
<NavBar {profileName} bind:sidebar={open} />

<style lang="scss">
</style>
