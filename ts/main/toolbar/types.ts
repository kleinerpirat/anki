// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL | version 3 or later; http://www.gnu.org/licenses/agpl.html

export enum SyncStatus {
    NO_CHANGES = 0,
    NORMAL_SYNC = 1,
    FULL_SYNC = 2,
}

export type ToolbarArgs = {
    centerTrayContent: string[];
    leftTrayContent: string[];
    rightTrayContent: string[];
};
