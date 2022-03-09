<script lang="ts">
    import * as tr from "../../lib/ftl";
    import { newIcon, learningIcon, reviewIcon } from "../icons";
    import Col from "../../components/Col.svelte";
    import Row from "../../components/Row.svelte";
    import Absolute from "../../components/Absolute.svelte";
    import Container from "../../components/Container.svelte";
    import TooltipIcon from "./TooltipIcon.svelte";
</script>

<Absolute left top right>
    <Container --gutter-block="0.5rem">
        <Row class="flex-nowrap justify-content-between" --cols={2} --gutter-block="0">
            <Col><h2>{tr.browsingSidebarDecks()}</h2></Col>
            <Col>
                <TooltipIcon class="new-count" tooltip={tr.actionsNew()}>
                    {@html newIcon}
                </TooltipIcon>

                <TooltipIcon class="learn-count" tooltip={tr.schedulingLearning()}
                    >{@html learningIcon}
                </TooltipIcon>

                <TooltipIcon class="review-count" tooltip={tr.schedulingReview()}
                    >{@html reviewIcon}
                </TooltipIcon>
            </Col>
        </Row>
    </Container>
</Absolute>
