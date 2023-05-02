// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

export enum Side {
    FRONT,
    BACK,
}

export type IframeCommand = {
    directive: string;
    args?: any;
};

export type ReviewerArgs = {
    serverURL: string;
    hidePlayButtons: boolean;
    backgroundEnabled: boolean;
    showCounts: boolean;
    softwareDriver: boolean;
    extraContent: string;
    questionArgs: QuestionArgs;
    answerArgs: AnswerArgs;
};

export enum ContentType {
    TEXT = 1,
    SOUND = 2,
    TYPE_ANS = 3,
}
export type ContentPart = {
    type: ContentType;
    content: string;
};

type CardArgs = {
    content: ContentPart[];
    ord: number;
    counts: {
        new: number;
        learn: number;
        review: number;
    };
    countIndex: number;
    showTimer: boolean;
    maxTime: number;
    flag: number;
    marked: boolean;
};

export interface QuestionArgs extends CardArgs {
    aText: string;
}

export type AnswerButton = {
    default: boolean;
    label: string;
    due: string;
};

export interface AnswerArgs extends CardArgs {
    answerButtons: AnswerButton[];
}
