# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
from __future__ import annotations

import enum
import json
import re
from typing import Any, Callable, Optional, List

import aqt
from anki.sync import SyncStatus
from aqt import gui_hooks
from aqt.qt import *
from aqt.sync import get_sync_status
from aqt.theme import theme_manager
from aqt.utils import tr
from aqt.webview import AnkiWebView, AnkiWebViewKind


class HideMode(enum.IntEnum):
    FULLSCREEN = 0
    ALWAYS = 1


class Toolbar:
    def __init__(self, mw: aqt.AnkiQt) -> None:
        self.mw = mw
        self.link_handlers: dict[str, Callable] = {
            "study": self._studyLinkHandler,
            "decks": self._deckLinkHandler,
            "add": self._addLinkHandler,
            "browse": self._browseLinkHandler,
            "stats": self._statsLinkHandler,
            "sync": self._syncLinkHandler,
        }

    def args(
        self,
    ) -> dict:
        return {
            "centerTrayContent": self._center_tray_content(),
            "leftTrayContent": self._left_tray_content(),
            "rightTrayContent": self._right_tray_content(),
        }

    def redraw(self) -> None:
        self.set_sync_active(self.mw.media_syncer.is_syncing())
        self.update_sync_status()
        gui_hooks.top_toolbar_did_redraw(self)

    # Available links
    ######################################################################

    # We create our links in TS, but some add-ons probably rely on this method
    def create_link(
        self,
        cmd: str,
        label: str,
        func: Callable,
        tip: str | None = None,
        id: str | None = None,
    ) -> str:
        """Generates HTML link element and registers link handler

        Arguments:
            cmd {str} -- Command name used for the JS → Python bridge
            label {str} -- Display label of the link
            func {Callable} -- Callable to be called on clicking the link

        Keyword Arguments:
            tip {Optional[str]} -- Optional tooltip text to show on hovering
                                   over the link (default: {None})
            id: {Optional[str]} -- Optional id attribute to supply the link with
                                   (default: {None})

        Returns:
            str -- HTML link element
        """

        self.link_handlers[cmd] = func

        title_attr = f'title="{tip}"' if tip else ""
        id_attr = f'id="{id}"' if id else ""

        return (
            f"""<a class=hitem tabindex="-1" aria-label="{label}" """
            f"""{title_attr} {id_attr} href=# onclick="return pycmd('{cmd}')">"""
            f"""{label}</a>"""
        )

    # Add-ons
    ######################################################################

    def _center_tray_content(self) -> List[str]:
        center_tray_content: list[str] = []
        gui_hooks.top_toolbar_did_init_links(center_tray_content, self)
        return center_tray_content

    def _left_tray_content(self) -> List[str]:
        left_tray_content: list[str] = []
        gui_hooks.top_toolbar_will_set_left_tray_content(left_tray_content, self)
        return left_tray_content

    def _right_tray_content(self) -> List[str]:
        right_tray_content: list[str] = []
        gui_hooks.top_toolbar_will_set_right_tray_content(right_tray_content, self)
        return right_tray_content

    # Sync
    ######################################################################

    def set_sync_active(self, active: bool) -> None:
        self.mw.web.eval("")#f"anki.setSyncActive({json.dumps(active)}); ")

    def set_sync_status(self, status: SyncStatus) -> None:
        self.mw.web.eval("")#f"anki.setSyncStatus({status.required}); ")

    def update_sync_status(self) -> None:
        get_sync_status(self.mw, self.mw.toolbar.set_sync_status)

    # JS Bridge
    ######################################################################

    def _deckLinkHandler(self) -> None:
        self.mw.moveToState("deckBrowser")

    def _studyLinkHandler(self) -> None:
        # if overview already shown, switch to review
        if self.mw.state == "overview":
            self.mw.col.startTimebox()
            self.mw.moveToState("review")
        else:
            self.mw.onOverview()

    def _addLinkHandler(self) -> None:
        self.mw.onAddCard()

    def _browseLinkHandler(self) -> None:
        self.mw.onBrowse()

    def _statsLinkHandler(self) -> None:
        self.mw.onStats()

    def _syncLinkHandler(self) -> None:
        self.mw.on_sync_button_clicked()
