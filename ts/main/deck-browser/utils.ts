// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

export function scrollIntoViewIfNeeded(el: HTMLElement) {
    const rect = el.getBoundingClientRect();
    const elemTop = rect.top;
    const elemBottom = rect.bottom;

    // Only scroll if el is outside of viewport
    if (elemTop < 0 || elemBottom > window.innerHeight) {
        el.scrollIntoView({
            behavior: "smooth",
            block: elemTop < window.innerHeight / 2 ? "start" : "end",
            inline: "nearest",
        });
    }
}
