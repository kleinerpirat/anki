<script lang="ts">
    import WithCommand from "../../components/WithCommand.svelte";
    export let cmd = "";
</script>

<div>
    <WithCommand {cmd}>
        <slot />
    </WithCommand>
</div>

<style lang="scss">
    div {
        display: inline-block;
    }
</style>
