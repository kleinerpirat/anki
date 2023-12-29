// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL | version 3 or later; http://www.gnu.org/licenses/agpl.html

import type { Section } from "components/HelpSection.svelte";

export enum CustomStudyMode {
    NEW_LIMIT,
    REVIEW_LIMIT,
    FORGOTTEN,
    AHEAD,
    PREVIEW,
    CRAM,
}

export type CustomStudyOption = {
    mode: CustomStudyMode;
    icon: string;
    help: HelpSection;
};
