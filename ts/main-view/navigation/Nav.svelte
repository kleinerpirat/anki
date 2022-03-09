<script lang="ts">
    let className = "";
    export { className as class };
</script>

<nav class="d-flex {className}">
    <slot />
</nav>

<style lang="scss">
    nav {
        flex: 0 1 auto;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);

        &:first-child,
        &:last-child {
            position: unset;
            left: unset;
            transform: none;
        }
        &:first-child {
            margin-right: auto;
        }
        &:last-child {
            margin-left: auto;
        }
    }
</style>
