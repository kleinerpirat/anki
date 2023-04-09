// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import { bridgeCommand } from "@tslib/bridgecommand";

export function initializeDragAndDrop() {
    const decks = document.querySelectorAll("tr.deck");

    decks.forEach((deck) => {
        deck.addEventListener("dragstart", (event) => {
            console.log("dragstart");
            event.dataTransfer!.setData("text/plain", deck.id);
            deck.classList.add("dragging");
        });

        deck.addEventListener("dragend", (event) => {
            console.log("dragend");
            deck.classList.remove("dragging");
        });

        deck.addEventListener("dragover", (event) => {
            console.log("dragover");
            deck.classList.add("drag-hovered");
        });

        deck.addEventListener("dragenter", (event) => {
            console.log("dragenter");
            deck.classList.add("drag-hovered");
        });

        deck.addEventListener("dragleave", (event) => {
            console.log("dragleave");
            deck.classList.remove("drag-hovered");
        });

        deck.addEventListener("drop", (event) => {
            console.log("drop");
            const draggedDeckId = event.dataTransfer.getData("text/plain");
            console.log(`Deck ${draggedDeckId} was dropped onto deck ${deck.id}.`);
            deck.classList.remove("drag-hovered");
        });
    });
}
