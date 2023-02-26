<!--
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
-->
<script lang="ts">
    import { bridgeCommand } from "@tslib/bridgecommand";

    export let backgroundCSS: string;

    function setBackgroundImage(img: string) {
        if (!img) {
            // remove rule
            backgroundCSS = backgroundCSS.replace(/\s*url\([^\)]*\)/, "");
            backgroundCSS = backgroundCSS.replace(/\n*background:\s*;/, "").trim();
            return;
        }
        let replaced = backgroundCSS.replace(/url\(.+\)/, `url(${img})`);
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        replaced = backgroundCSS.replace(
            /background:(.+);/,
            `background: url(${img})$1;`,
        );
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        backgroundCSS += `\nbackground: url(${img});`;
    }

    let saturation = 1;
    let opacity = 1;
    let blur = 0;

    Object.assign(globalThis, {
        setBackgroundImage,
    });

    function onSaturationChange(e) {
        saturation = e.target.value;
        if (saturation == 1) {
            // remove rule
            backgroundCSS = backgroundCSS.replace(/\s*saturate\([^\)]*\)/, "");
            backgroundCSS = backgroundCSS.replace(/\n*filter:\s*;/, "").trim();
            return;
        }
        let replaced = backgroundCSS.replace(
            /saturate\([\d\.]+(.+)\)/,
            `saturate(${saturation}$1)`,
        );
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        replaced = backgroundCSS.replace(
            /filter:(.+);/,
            `filter:$1 saturate(${saturation});`,
        );
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        backgroundCSS += `\nfilter: saturate(${saturation});`;
    }

    function onOpacityChange(e) {
        opacity = e.target.value;
        if (opacity == 1) {
            // remove rule
            backgroundCSS = backgroundCSS.replace(/\n*opacity:.*;/, "").trim();
            return;
        }
        let replaced = backgroundCSS.replace(
            /opacity:\s*[\d\.]+/,
            `opacity: ${opacity}`,
        );
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        backgroundCSS += `\nopacity: ${opacity};`;
    }

    function onBlurChange(e) {
        blur = e.target.value;
        if (blur == 0) {
            // remove rule
            backgroundCSS = backgroundCSS.replace(/\s*blur\([^\)]*\)/, "");
            backgroundCSS = backgroundCSS.replace(/\n*filter:\s*;/, "").trim();
            return;
        }
        let replaced = backgroundCSS.replace(/blur\([\d\.]+(.+)\)/, `blur(${blur}$1)`);
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        replaced = backgroundCSS.replace(/filter:(.+);/, `filter:$1 blur(${blur}px);`);
        if (replaced != backgroundCSS) {
            backgroundCSS = replaced;
            return;
        }
        backgroundCSS += `\nfilter: blur(${blur}px);`;
    }

    function onCSSChange(e) {
        backgroundCSS = e.target.value;
        updateSliders();
    }

    function updateSliders() {
        const saturationMatch = backgroundCSS.match(
            /filter:[^;]*saturation\(([\d\.]+)\)/,
        );
        if (saturationMatch) {
            saturation = parseInt(saturationMatch[1]);
        }
        const opacityMatch = backgroundCSS.match(/opacity:\s*([\d]+)/);
        if (opacityMatch) {
            opacity = parseFloat(opacityMatch[1]);
        }
        const blurMatch = backgroundCSS.match(/filter:[^;]*blur\(([\d\.]+)px\)/);
        if (blurMatch) {
            blur = parseInt(blurMatch[1]);
        }
    }
</script>

{@html `<style>.background-editor::after{${backgroundCSS.replace(
    /url\(["']*(.*)["']*\)/,
    "url(../../$1)",
)};</style>`}

<div class="background-editor glass">
    <div class="preview">
        <div class="controls">
            <div>
                <label for="background-saturation">Saturation:</label>
                <input
                    id="background-saturation"
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    bind:value={saturation}
                    on:input={onSaturationChange}
                />
            </div>
            <div>
                <label for="background-opacity">Opacity:</label>
                <input
                    id="background-opacity"
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    bind:value={opacity}
                    on:input={onOpacityChange}
                />
            </div>
            <div>
                <label for="background-blur">Blur:</label>
                <input
                    id="background-blur"
                    type="range"
                    min="0"
                    max="20"
                    step="0.1"
                    bind:value={blur}
                    on:input={onBlurChange}
                />
            </div>
        </div>
    </div>

    <textarea id="background-css" bind:value={backgroundCSS} on:input={onCSSChange} />
    <button on:click={() => bridgeCommand("file")}>Open File</button>
    <button on:click={() => bridgeCommand(`apply:${backgroundCSS}`)}>Apply</button>
</div>

<style lang="scss">
    @use "sass/elevation" as *;
    @use "sass/background-mixins" as *;

    .background-editor {
        margin-bottom: 0.5em;
        height: 100%;
        display: flex;
        flex-flow: row;
        border-radius: var(--border-radius-medium);
        background: none;
        @include elevation(5);
        position: relative;
        overflow: hidden;

        &::after {
            @include pseudo(center);
            position: absolute !important;
            border-radius: var(--border-radius-medium);
        }
    }

    .preview {
        width: 288px;
        display: grid;
        place-items: end start;
    }

    .controls {
        border-top-right-radius: var(--border-radius-large);
    }

    .controls,
    textarea,
    button {
        color: var(--fg);
        display: inline-block;
        padding: 0.25em 0.5em;
        .glass & {
            background: var(--glass);
            backdrop-filter: blur(var(--blur));
        }
    }
</style>
