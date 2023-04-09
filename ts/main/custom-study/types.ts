// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL | version 3 or later; http://www.gnu.org/licenses/agpl.html

export enum CustomStudyMode {
    INCREASE_NEW_LIMIT,
    INCREASE_REVIEW_LIMIT,
    REVIEW_FORGOTTEN,
    REVIEW_AHEAD,
    PREVIEW,
    CRAM,
}

export type CustomStudyOption = {
    mode: CustomStudyMode;
    desc: string;
    icon: string;
};
