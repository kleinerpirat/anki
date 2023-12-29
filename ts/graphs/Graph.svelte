<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import Container from "../components/Container.svelte";

    export let title: string;
    export let subtitle: string | null = null;
    export let hideTitle = false;
</script>

<Container class="d-flex flex-column">
    <h1 class="title" hidden={hideTitle}>{title}</h1>
    <div class="graph d-flex flex-grow-1 flex-column justify-content-center">
        {#if subtitle}
            <div class="subtitle">{subtitle}</div>
        {/if}
        <slot />
    </div>
</Container>

<style lang="scss">
    @use "sass/props";

    .graph {
        /* See graph-styles.ts for constants referencing global styles */
        :global(.graph-element-clickable) {
            cursor: pointer;
        }

        /* Customizing the standard x and y tick markers and text on the graphs.
         * The `tick` class is automatically added by d3. */
        :global(.tick) {
            :global(line) {
                opacity: 0.1;
            }

            :global(text) {
                opacity: props.$opacity-idle;
                font-size: 10px;

                @media only screen and (max-width: 800px) {
                    font-size: 13px;
                }

                @media only screen and (max-width: 600px) {
                    font-size: 16px;
                }
            }
        }

        :global(.tick-odd) {
            @media only screen and (max-width: 600px) {
                /* on small screens, hide every second row on graphs that have
                 * marked the ticks as odd */
                display: none;
            }
        }

        &:focus {
            outline: 0;
        }
    }

    .subtitle {
        text-align: center;
        margin-bottom: 1em;
    }
</style>
