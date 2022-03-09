<script lang="ts">
    import * as tr from "../lib/ftl";
    import { newIcon, learningIcon, reviewIcon } from "./icons";
    import Col from "../components/Col.svelte";
    import Row from "../components/Row.svelte";
    import StickyContainer from "../components/StickyContainer.svelte";
    import TooltipIcon from "./TooltipIcon.svelte";
</script>

<StickyContainer --gutter-block="0.5rem">
    <Row --cols={8} --gutter-block="0">
        <Col --col-size={5}><h2>{tr.browsingSidebarDecks()}</h2></Col>
        <Col --col-justify="flex-end">
            <TooltipIcon class="new-count" tooltip={tr.actionsNew()}>
                {@html newIcon}
            </TooltipIcon>
        </Col>
        <Col --col-justify="flex-end">
            <TooltipIcon class="learn-count" tooltip={tr.schedulingLearning()}
                >{@html learningIcon}
            </TooltipIcon>
        </Col>
        <Col --col-justify="flex-end">
            <TooltipIcon class="review-count" tooltip={tr.schedulingReview()}
                >{@html reviewIcon}
            </TooltipIcon>
        </Col>
    </Row>
</StickyContainer>
