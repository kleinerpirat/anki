<script lang="ts">
    import IconConstrain from "../../components/IconConstrain.svelte";
    import WithCommand from "../../components/WithCommand.svelte";
    import { darkThemeIcon, lightThemeIcon } from "../icons";
    export let light = false;
</script>

<WithCommand cmd="toggleTheme" keyCombination="N">
    <IconConstrain iconSize={100}>
        {@html light ? darkThemeIcon : lightThemeIcon}
    </IconConstrain>
</WithCommand>
