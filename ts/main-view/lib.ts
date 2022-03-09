// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import { bridgeCommand } from "../lib/bridgecommand";

export function handleClick(event) {
    const el = event.target;
    const did = el.closest("[data-did]")?.dataset.did;

    if (el.classList.contains("deck")) {
        bridgeCommand(`open:${did}`);
    } else {
        const count = el.closest(".new-count, .learn-count, .review-count");
        if (count) {
            const state = count.className.match(/([^\s]+)-count/)[1];
            bridgeCommand(
                `browserSearch:${
                    did ? `did:${did} ` : ""
                }is:${state} -is:suspended (prop:due=0 OR -prop:due=0)`,
            );
        } else {
            bridgeCommand(`collapse:${did}`);
        }
    }
}
