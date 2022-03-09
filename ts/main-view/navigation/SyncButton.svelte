<script lang="ts">
    import IconConstrain from "../../components/IconConstrain.svelte";
    import WithCommand from "../../components/WithCommand.svelte";
    import { syncIcon, syncActiveIcon } from "../icons";
    export let active = false;
</script>

<WithCommand cmd="sync" keyCombination="Y">
    <IconConstrain iconSize={100}>
        {@html active ? syncActiveIcon : syncIcon}
    </IconConstrain>
</WithCommand>
