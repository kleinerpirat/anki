// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

export type Callback = () => void;

export function removeItem<T>(items: T[], item: T): void {
    const index = items.findIndex((i: T): boolean => i === item);

    if (index >= 0) {
        items.splice(index, 1);
    }
}

/**
 * Run scripts and videos inserted as plain text via innerHTML (e.g. as part of
 * a card template or add-on content inserted via the Python toolbar/status bar API)
 */
export async function refreshInsertedHTML(el: Element): Promise<void> {
    async function replaceScript(oldScript: HTMLScriptElement): Promise<void> {
        let inline = !oldScript.hasAttribute("src");

        const newScript = document.createElement("script");
        for (const attribute of oldScript.attributes) {
            newScript.setAttribute(attribute.name, attribute.value);
        }
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.replaceWith(newScript);

        if (inline) {
            return;
        }
        await Promise.race([
            new Promise((resolve) => newScript.addEventListener("load", resolve)),
            new Promise((resolve) => newScript.addEventListener("error", resolve)),
        ]);
    }

    // Play videos
    for (const oldVideo of el.getElementsByTagName("video")) {
        oldVideo.pause();
        while (oldVideo.firstChild) {
            oldVideo.removeChild(oldVideo.firstChild);
        }
        oldVideo.load();
    }
    // Run scripts
    for (const oldScript of el.getElementsByTagName("script")) {
        await replaceScript(oldScript);
    }
}
