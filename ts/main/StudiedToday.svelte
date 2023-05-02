<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { studiedToday } from "@tslib/time";
    import type { Stats } from "@tslib/proto";
    export let sourceData: Stats.GraphsResponse | null;

    $: today = sourceData?.today!;
    $: studiedTodayText = sourceData
        ? studiedToday(today.answerCount, today.answerMillis / 1000)
        : "";
</script>

<div id="studiedToday">
    {studiedTodayText}
</div>
