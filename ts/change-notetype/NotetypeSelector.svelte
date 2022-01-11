<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import type { ChangeNotetypeState } from "./lib";
    import type { SelectOption } from "../components/types";
    import StickyContainer from "../components/StickyContainer.svelte";
    import ButtonToolbar from "../components/ButtonToolbar.svelte";
    import Item from "../components/Item.svelte";
    import ButtonGroup from "../components/ButtonGroup.svelte";
    import ButtonGroupItem from "../components/ButtonGroupItem.svelte";
    import LabelButton from "../components/LabelButton.svelte";
    import Badge from "../components/Badge.svelte";
    import { arrowRightIcon, arrowLeftIcon } from "./icons";
    import SelectButton from "../components/SelectButton.svelte";
    import SaveButton from "./SaveButton.svelte";

    export let state: ChangeNotetypeState;
    let notetypes = state.notetypes;
    let info = state.info;

    async function blur(event: CustomEvent<SelectOption>): Promise<void> {
        await state.setTargetNotetypeIndex(
            event.detail.idx,
        );
    }
</script>

<StickyContainer
    --gutter-block="0.1rem"
    --gutter-inline="0.25rem"
    --sticky-borders="0 0 1px"
    --sticky-z-index="3"
>
    <ButtonToolbar class="justify-content-between" size={2.3} wrap={false}>
        <Item>
            <ButtonGroupItem>
                <LabelButton disabled={true}>
                    {$info.oldNotetypeName}
                </LabelButton>
            </ButtonGroupItem>
        </Item>
        <Item>
            <Badge iconSize={70}>
                {#if window.getComputedStyle(document.body).direction == "rtl"}
                    {@html arrowLeftIcon}
                {:else}
                    {@html arrowRightIcon}
                {/if}
            </Badge>
        </Item>
        <Item>
            <ButtonGroup class="flex-grow-1">
                <ButtonGroupItem>
                    <SelectButton
                        options={Array.from($notetypes, (entry) => entry.name)}
                        class="flex-grow-1"
                        searchable={true}
                        on:change={blur}
                    />
                </ButtonGroupItem>
            </ButtonGroup>
        </Item>

        <Item>
            <SaveButton {state} />
        </Item>
    </ButtonToolbar>
</StickyContainer>
