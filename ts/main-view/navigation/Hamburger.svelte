<script lang="ts">
    export let open = false;
</script>

<div class:open on:click={() => (open = !open)}>
    <svg width="32" height="24">
        <line id="top" x1="0" y1="2" x2="32" y2="2" />
        <line id="middle" x1="0" y1="12" x2="32" y2="12" />
        <line id="bottom" x1="0" y1="22" x2="32" y2="22" />
    </svg>
</div>

<style lang="scss">
    div {
        z-index: 2;
        margin-right: 2rem;
    }
    svg line {
        stroke: currentColor;
        stroke-width: 4;
        transition: all 0.15s ease;
    }

    .open {
        #top {
            transform-origin: center center;
            transform: rotate(45deg) translateY(10px);
        }
        #middle {
            transform: scaleX(0);
            opacity: 0;
        }
        #bottom {
            transform-origin: center center;
            transform: rotate(-45deg) translateY(-10px);
        }
    }
</style>
