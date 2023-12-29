<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import * as tr from "@tslib/ftl";
    import ReviewerFrame from "../reviewer/ReviewerFrame.svelte";
</script>

<div class="previewer">
    <ReviewerFrame />
</div>

<style lang="scss">
    .previewer {
        height: 100vh;
        width: 100vw;
    }
</style>
