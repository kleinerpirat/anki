// Execute addon scripts inserted via HTML
export function loadAddonScripts(el: HTMLDivElement) {
    Array.from(document.body.querySelectorAll("script")).forEach((script) => {
        const newScript = document.createElement("script");
        Array.from(script.attributes).forEach((attr) => {
            newScript.setAttribute(attr.name, attr.value);
        });
        newScript.text = script.text;
        script.parentNode?.removeChild(script);
        el.appendChild(newScript);
    });
}
