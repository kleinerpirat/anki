// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import { scheduler, decks } from "@tslib/proto";
import { Decks, Scheduler } from "@tslib/proto";

export async function counts(
    did: Decks.DeckId,
    queue: { newCount: number; learningCount: number; reviewCount: number },
): Promise<{
    new: number;
    learn: number;
    review: number;
}> {
    const deckNode = await deckDueTree(did);
    return {
        new: deckNode.newCount - queue.newCount,
        learn: deckNode.learnCount - queue.learningCount,
        review: deckNode.reviewCount - queue.reviewCount,
    };
}
/**
 * Returns a tree of decks with counts.
 * Translated to TS from SchedulerBase in pylib/anki/scheduler/base.py
 */ export async function deckDueTree(
    topDeckId: Decks.DeckId | undefined,
): Promise<Decks.DeckTreeNode> {
    const tree = decks.deckTree(
        Decks.DeckTreeRequest.fromObject({ now: new Date().getTime() / 1000 }),
    );
    if (topDeckId) {
        return findDeckInTree(tree, topDeckId);
    }
    return tree;
}

/**
 * Translated to TS from DeckManager in pylib/anki/decks.py
 */
function findDeckInTree(
    node: Decks.DeckTreeNode,
    deckId: Decks.DeckId,
): Decks.DeckTreeNode | null {
    if (node.deckId == deckId.did) {
        return node;
    }
    for (const child of node.children) {
        const match = findDeckInTree(child, deckId);
        if (match) {
            return match;
        }
    }
    return null;
}
