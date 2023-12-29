// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

export function validateColor(str: string): boolean {
    // Qt doesn't support hsl or hsla
    const hslRegex = /^hsl\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*\)$/;
    const hslaRegex = /^hsla\(\s*\d+\s*,\s*\d+%?\s*,\s*\d+%?\s*,\s*(0(\.\d+)?|1(\.0+)?)\s*\)$/;
    // CSS supports named variables with spaces, but Qt doesn't
    const namedRegex = /\b\w+\s+\w+\b/;

    if (namedRegex.test(str) || hslRegex.test(str) || hslaRegex.test(str)) {
        return false;
    }

    return CSS.supports("color", str);
}
