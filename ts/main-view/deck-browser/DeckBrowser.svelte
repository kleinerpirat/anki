<script lang="ts">
    import { handleClick } from "../lib";

    import Container from "../../components/Container.svelte";
    import Header from "./Header.svelte";
</script>

<Container
    class="h-100 position-relative"
    --gutter-block="1rem"
    --gutter-inline="2px"
    breakpoint="xs"
>
    <div class="deck-browser" on:click={handleClick}>
        <Header />
        <slot />
    </div>
</Container>
