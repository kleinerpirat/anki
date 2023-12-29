// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import { registerPackage } from "@tslib/runtime-require";
import { writable } from "svelte/store";
import { MainPageContext } from "./types";

export const mwContext = writable<MainPageContext>(MainPageContext.HOME);

registerPackage("anki/MainPage", {
    mwContext,
});
