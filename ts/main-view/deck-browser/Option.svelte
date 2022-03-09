<script lang="ts">
    import IconConstrain from "../../components/IconConstrain.svelte";
    export let node: any;
</script>

<span>
    <IconConstrain iconSize={65}>
        <slot />
    </IconConstrain>
</span>

<style lang="scss">
    span {
        margin-left: 1rem;
    }
</style>
