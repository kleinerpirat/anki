<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import { noop } from "@tslib/functional";
    import { createEventDispatcher, getContext } from "svelte";

    import ButtonToolbar from "../components/ButtonToolbar.svelte";
    import Select from "../components/Select.svelte";
    import SelectOption from "../components/SelectOption.svelte";
    import type { ConfigListEntry, DeckOptionsState } from "./lib";
    import SaveButton from "./SaveButton.svelte";
    import TextInputModal from "./TextInputModal.svelte";

    export let state: DeckOptionsState;
    const configList = state.configList;
    const dispatch = createEventDispatcher();
    const dispatchPresetChange = () => dispatch("presetchange");

    $: value = $configList.findIndex((entry) => entry.current);
    $: label = configLabel($configList[value]);

    function configLabel(entry: ConfigListEntry): string {
        const count = tr.deckConfigUsedByDecks({ decks: entry.useCount });
        return `${entry.name} (${count})`;
    }

    function blur(e: CustomEvent): void {
        state.setCurrentIndex(e.detail.value);
        dispatchPresetChange();
    }

    function onAddConfig(e: CustomEvent): void {
        const trimmed = e.detail.text.trim();
        if (trimmed.length) {
            state.addConfig(trimmed);
            dispatchPresetChange();
        }
    }

    function onCloneConfig(e: CustomEvent): void {
        const trimmed = e.detail.text.trim();
        if (trimmed.length) {
            state.cloneConfig(trimmed);
            dispatchPresetChange();
        }
    }

    function onRenameConfig(e: CustomEvent): void {
        state.setCurrentName(e.detail.text);
    }

    let modalStartingValue = "";
    let modalTitle = "";
    let modalSuccess: (e: CustomEvent) => any = noop;

    function promptToAdd() {
        modalTitle = tr.deckConfigAddGroup();
        modalSuccess = onAddConfig;
        modalStartingValue = "";
        showModal = true;
    }

    function promptToClone() {
        modalTitle = tr.deckConfigCloneGroup();
        modalSuccess = onCloneConfig;
        modalStartingValue = state.getCurrentName();
        showModal = true;
    }

    function promptToRename() {
        modalTitle = tr.deckConfigRenameGroup();
        modalSuccess = onRenameConfig;
        showModal = true;
    }

    let showModal = false;
</script>

<TextInputModal
    title={modalTitle}
    prompt={tr.deckConfigNamePrompt()}
    value={modalStartingValue}
    on:accept={modalSuccess}
    show={showModal}
/>

<div class="config-selector">
    <ButtonToolbar class="justify-content-between flex-grow-1" wrap={false}>
        <Select class="flex-grow-1" bind:value {label} on:change={blur}>
            {#each $configList as entry}
                <SelectOption value={entry.idx}>{configLabel(entry)}</SelectOption>
            {/each}
        </Select>

        <SaveButton
            {state}
            on:add={promptToAdd}
            on:clone={promptToClone}
            on:rename={promptToRename}
            on:remove={dispatchPresetChange}
        />
    </ButtonToolbar>
</div>
