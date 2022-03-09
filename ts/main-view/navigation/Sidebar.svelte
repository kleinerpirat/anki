<script lang="ts">
    import * as tr from "../../lib/ftl";
    import Fixed from "../../components/Fixed.svelte";
    export let open = false;

    const navItems = [
        {
            cmd: "decks",
            label: tr.actionsDecks(),
            tip: tr.actionsShortcutKey({ val: "D" }),
        },
        {
            cmd: "add",
            label: tr.actionsAdd(),
            tip: tr.actionsShortcutKey({ val: "A" }),
        },
        {
            cmd: "browse",
            label: tr.qtMiscBrowse(),
            tip: tr.actionsShortcutKey({ val: "B" }),
        },
        {
            cmd: "stats",
            label: tr.qtMiscStats(),
            tip: tr.actionsShortcutKey({ val: "T" }),
        },
    ];
</script>

<Fixed top left bottom>
    <slot />
    <aside class:open on:blur={() => (open = !open)}>
        <nav>
            {#each navItems as item}
                <div>{item.label}</div>
            {/each}
        </nav>
    </aside>
</Fixed>

<style lang="scss">
    aside {
        position: absolute;
        top: 0;
        left: calc(-50vw - 50px);
        bottom: 0;
        min-width: 250px;
        max-width: 50vw;
        height: 100%;
        transition: left 0.3s ease, box-shadow 0.3s ease;
        z-index: 1;
        background: var(--window-bg);
        &.open {
            left: 0;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.3);
        }
        nav {
            padding: 80px 20px 20px 10px;
            display: grid;
            grid-template-columns: 1fr;
            grid-gap: 5px 0;
            align-content: start;

            div {
                background: var(--frame-bg);
                padding: 10px;

                &:hover {
                    cursor: pointer;
                    background: var(--frame-bg);
                }
            }
        }
    }
</style>
