<script lang="ts">
    import Badge from "../../components/Badge.svelte";
    import IconConstrain from "../../components/IconConstrain.svelte";

    import WithTooltip from "../../components/WithTooltip.svelte";
    let className = "";
    export { className as class };

    export let tooltip: string;
</script>

<WithTooltip
    {tooltip}
    showDelay={250}
    offset={[0, 20]}
    placement="left"
    let:createTooltip
>
    <span class={className}>
        <IconConstrain
            iconSize={80}
            on:mount={(event) => createTooltip(event.detail.span)}
        >
            <slot />
        </IconConstrain>
    </span>
</WithTooltip>
