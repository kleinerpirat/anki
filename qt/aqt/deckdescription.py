# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from __future__ import annotations

import json
import aqt
import aqt.main
import aqt.operations
from anki.decks import DeckDict
from aqt.operations import QueryOp
from aqt.operations.deck import update_deck_dict
from aqt.qt import *


class DeckDescriptionDialog:
    def __init__(self, mw: aqt.main.AnkiQt) -> None:
        self.mw = mw
        # set on success
        self.deck: DeckDict

        QueryOp(
            parent=self.mw,
            op=lambda col: col.decks.current(),
            success=self._setup_and_show,
        ).run_in_background()

    def _setup_and_show(self, deck: DeckDict) -> None:
        if deck["dyn"]:
            return

        self.deck = deck
        args = {
            "description": self.deck.get("desc", ""),
            "markdown": self.deck.get("md", False),
        }
        self.mw.web.eval(f"""anki.setupDeckEditor({json.dumps(args)}); """)


    def save_and_accept(self) -> None:
        self.deck["desc"] = self.description.toPlainText()
        self.deck["md"] = self.enable_markdown.isChecked()

        update_deck_dict(parent=self, deck=self.deck).success(
            lambda _: self.accept()
        ).run_in_background()
