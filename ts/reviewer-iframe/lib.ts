// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

type Callback = () => void | Promise<void>;

export function runHook(
    hooks: Array<Callback>,
): Promise<PromiseSettledResult<void | Promise<void>>[]> {
    const promises: (Promise<void> | void)[] = [];

    for (const hook of hooks) {
        try {
            const result = hook();
            promises.push(result);
        } catch (error) {
            console.log("Hook failed: ", error);
        }
    }

    return Promise.allSettled(promises);
}

export const renderError = (type: string) => (error: unknown): string => {
    const errorMessage = String(error).substring(0, 2000);
    let errorStack: string;
    if (error instanceof Error) {
        errorStack = String(error.stack).substring(0, 2000);
    } else {
        errorStack = "";
    }
    return `<div>Invalid ${type} on card: ${errorMessage}\n${errorStack}</div>`.replace(
        /\n/g,
        "<br>",
    );
};

/**
 * Execute a couple of old reviewer hacks
 */
export function applyReviewerHacks(): void {
    // Block Qt's default drag & drop behavior by default
    function handler(evt: DragEvent) {
        evt.preventDefault();
    }
    document.ondragenter = handler;
    document.ondragover = handler;
    document.ondrop = handler;

    // work around WebEngine/IME bug in Qt6
    // https://github.com/ankitects/anki/issues/1952
    const dummyButton = document.createElement("button");
    dummyButton.style.position = "absolute";
    dummyButton.style.left = "-9999px";
    document.addEventListener("focusout", (event) => {
        // Prevent type box from losing focus when switching IMEs
        if (!document.hasFocus()) {
            return;
        }

        const target = event.target;
        if (
            target instanceof HTMLInputElement
            || target instanceof HTMLTextAreaElement
        ) {
            document.body.appendChild(dummyButton);
            dummyButton.focus();
            document.body.removeChild(dummyButton);
        }
    });
}
