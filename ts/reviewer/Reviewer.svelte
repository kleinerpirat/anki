<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { fade } from "svelte/transition";
    import { pageTheme } from "sveltelib/theme";
    import type { ReviewerArgs } from "../main/types";
    export let serverURL: string;

    let args: ReviewerArgs;
    export { args as reviewerArgs };
</script>

<iframe
    title="reviewer"
    src={`${serverURL}_anki/pages/reviewer.html${$pageTheme.isDark ? "#night" : ""}`}
    sandbox={[
        "allow-downloads",
        "allow-forms",
        "allow-modals",
        "allow-pointer-lock",
        "allow-popups",
        "allow-popups-to-escape-sandbox",
        "allow-same-origin",
        "allow-scripts",
    ].join(" ")}
/>

<style lang="scss">
    iframe {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
    }
</style>
