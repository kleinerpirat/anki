# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from __future__ import annotations
from google.protobuf.json_format import MessageToJson

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

import aqt
import aqt.operations
from anki.collection import OpChanges
from anki.decks import DeckCollapseScope, DeckId, DeckTreeNode
from aqt import AnkiQt, gui_hooks
from aqt.deckoptions import display_options_for_deck_id
from aqt.operations.scheduling import (
    empty_filtered_deck,
    rebuild_filtered_deck,
    unbury_deck,
)
from aqt.operations import QueryOp
from aqt.operations.deck import (
    add_deck_dialog,
    remove_decks,
    rename_deck,
    reparent_decks,
    set_current_deck,
    set_deck_collapsed,
    update_deck_dict,
)
from aqt.profiles import VideoDriver
from aqt.qt import *
from aqt.sound import av_player
from aqt.utils import (
    askUserDialog,
    openLink,
    shortcut,
    tooltip,
    tr,
    getOnlyText,
    showInfo,
)


@dataclass
class DeckBrowserContent:
    """Stores sections of HTML content that the deck browser will be
    populated with.

    Attributes:
        tree {str} -- HTML of the deck tree section
        stats {str} -- HTML of the stats section
    """

    tree: str
    stats: str


@dataclass
class OverviewContent:
    """Stores HTML strings that can be modified by add-ons.

    Attributes:
        deck {str} -- Plain text deck name
        shareLink {str} -- HTML for the share link section
        desc {str} -- HTML for the deck description section
        table {str} -- HTML for the deck stats section
    """

    deck: str
    shareLink: str
    desc: str
    table: str


@dataclass
class RenderDeckNodeContext:
    current_deck_id: DeckId


class DeckBrowser:
    _dueTree: DeckTreeNode
    loaded: bool

    def __init__(self, mw: AnkiQt) -> None:
        self.mw = mw
        self.web = mw.web
        self.loaded = False
        self.scrollPos = QPoint(0, 0)
        self._v1_message_dismissed_at = 0
        self._refresh_needed = False

    def show(self) -> None:
        av_player.stop_and_clear_queue()
        self.refresh()

    def refresh(self) -> None:
        self._refresh_needed = False
        self.mw.col.reset()
        self._renderPage()
        # redraw top bar for theme change
        self.mw.toolbar.redraw()
        self.mw.web.setFocus()
        gui_hooks.overview_did_refresh(self)

    def refresh_if_needed(self) -> None:
        if self._refresh_needed:
            self.refresh()

    def op_executed(
        self, changes: OpChanges, handler: object | None, focused: bool
    ) -> bool:
        if changes.study_queues and handler is not self:
            self._refresh_needed = True

        if focused:
            self.refresh_if_needed()

        return self._refresh_needed


    # Legacy Deck Browser events
    ##########################################################################

    def set_current_deck(self, deck_id: DeckId) -> None:
        set_current_deck(parent=self.mw, deck_id=deck_id).success(
            lambda _: self.mw.onOverview()
        ).run_in_background(initiator=self)

    def _renderPage(self, reuse: bool = False) -> None:
        if not reuse:
            self._dueTree = self.mw.col.sched.deck_due_tree()
            self.__renderPage(None)
            return
        self.web.evalWithCallback("window.pageYOffset", self.__renderPage)

    def __renderPage(self, offset: int) -> None:
        deckBrowserArgs = {
            "currentDeckId": self.mw.col.conf["curDeck"],
            "schedulerVersion": self.mw.col.sched_ver(),
            "studiedToday": self.mw.col.studied_today(),
        }

        self.deck = self.mw.col.decks.current()
        self.sid = self.deck.get("sharedFrom")
        self.sidVer = self.deck.get("ver", None)

        overviewArgs = {
            "deck": {
                "name": self.deck["name"],
                "finished": self.mw.col.sched._is_finished(),
                "isDyn": self.mw.col.decks.current()["dyn"] == 1,
                "description": self.deck.get("desc", ""),
                "hasBuried": self.mw.col.sched.have_buried(),
                "url": f"{aqt.appShared}info/{self.sid}?v={self.sidVer}"
                if self.sid
                else "",
            },
            "markdown": self.deck.get("md", True),
            "days": self.mw.pm.default_stats_days(),
        }

        reviewerArgs = {
            "softwareDriver": self.mw.pm.video_driver() == VideoDriver.Software,
            "extraContent": self.mw.col.conf.get("reviewExtra"),
        }

        self.web.eval(
            f"""anki.setupDeckBrowser(
                {MessageToJson(self._dueTree)},
                {json.dumps(deckBrowserArgs)},
                {json.dumps(overviewArgs)},
                {json.dumps(self.mw.toolbar.args())},
                {json.dumps(reviewerArgs)},
                {json.dumps(self.mw.serverURL())}
            ); """
        )

        if offset is not None:
            self._scrollToOffset(offset)
        gui_hooks.deck_browser_did_render(self)

    def _scrollToOffset(self, offset: int) -> None:
        self.web.eval("window.scrollTo(0, %d, 'instant');" % offset)

    # Options
    ##########################################################################

    def _showOptions(self, did: str) -> None:
        m = QMenu(self.mw)
        a = m.addAction(tr.actions_rename())
        qconnect(a.triggered, lambda b, did=did: self._rename(DeckId(int(did))))
        a = m.addAction(tr.actions_options())
        qconnect(a.triggered, lambda b, did=did: self._options(DeckId(int(did))))
        a = m.addAction(tr.actions_export())
        qconnect(a.triggered, lambda b, did=did: self._export(DeckId(int(did))))
        a = m.addAction(tr.actions_delete())
        qconnect(a.triggered, lambda b, did=did: self._delete(DeckId(int(did))))
        gui_hooks.deck_browser_will_show_options_menu(m, int(did))
        m.popup(QCursor.pos())

    def _export(self, did: DeckId) -> None:
        self.mw.onExport(did=did)

    def _rename(self, did: DeckId) -> None:
        def prompt(name: str) -> None:
            new_name = getOnlyText(tr.decks_new_deck_name(), default=name)
            if not new_name or new_name == name:
                return
            else:
                rename_deck(parent=self.mw, deck_id=did, new_name=new_name).success(
                    lambda _: self._renderPage(reuse=True)
                ).run_in_background()

        QueryOp(
            parent=self.mw, op=lambda col: col.decks.name(did), success=prompt
        ).run_in_background()

    def _options(self, did: DeckId) -> None:
        display_options_for_deck_id(did)

    def _set_collapsed(self, did: DeckId, collapsed: bool) -> None:
        node = self.mw.col.decks.find_deck_in_tree(self._dueTree, did)
        if node:
            set_deck_collapsed(
                parent=self.mw,
                deck_id=did,
                collapsed=collapsed,
                scope=DeckCollapseScope.REVIEWER,
            ).success(lambda _: self._renderPage(reuse=True)).run_in_background()

    def _handle_drag_and_drop(self, source: DeckId, target: DeckId) -> None:
        reparent_decks(parent=self.mw, deck_ids=[source], new_parent=target).success(
            lambda _: self._renderPage(reuse=True)
        ).run_in_background()

    def _delete(self, did: DeckId) -> None:
        remove_decks(parent=self.mw, deck_ids=[did]).success(
            lambda _: self._renderPage(reuse=True)
        ).run_in_background()

    # Legacy Overview events
    ##########################################################################

    def _current_deck_is_filtered(self) -> int:
        return self.mw.col.decks.current()["dyn"]

    def rebuild_current_filtered_deck(self) -> None:
        rebuild_filtered_deck(
            parent=self.mw, deck_id=self.mw.col.decks.selected()
        ).run_in_background()

    def empty_current_filtered_deck(self) -> None:
        empty_filtered_deck(
            parent=self.mw, deck_id=self.mw.col.decks.selected()
        ).run_in_background()

    def onCustomStudyKey(self) -> None:
        if not self._current_deck_is_filtered():
            self.onStudyMore()

    def on_unbury(self) -> None:
        mode = UnburyDeck.Mode.ALL
        if self.mw.col.sched_ver() != 1:
            info = self.mw.col.sched.congratulations_info()
            if info.have_sched_buried and info.have_user_buried:
                opts = [
                    tr.studying_manually_buried_cards(),
                    tr.studying_buried_siblings(),
                    tr.studying_all_buried_cards(),
                    tr.actions_cancel(),
                ]

                diag = askUserDialog(tr.studying_what_would_you_like_to_unbury(), opts)
                diag.setDefault(0)
                ret = diag.run()
                if ret == opts[0]:
                    mode = UnburyDeck.Mode.USER_ONLY
                elif ret == opts[1]:
                    mode = UnburyDeck.Mode.SCHED_ONLY
                elif ret == opts[3]:
                    return

        unbury_deck(
            parent=self.mw, deck_id=self.mw.col.decks.get_current_id(), mode=mode
        ).run_in_background()

    onUnbury = on_unbury

    def _save_description(self, description: str, markdown: bool) -> None:
        self.deck["desc"] = description
        self.deck["md"] = markdown
        update_deck_dict(parent=self.mw, deck=self.deck).run_in_background()

    # Studying more
    ######################################################################

    def onStudyMore(self) -> None:
        import aqt.customstudy

        aqt.customstudy.CustomStudy.fetch_data_and_show(self.mw)

    # Toolbar buttons
    ######################################################################

    def _onShared(self, search: str) -> None:
        openLink(f"{aqt.appShared}decks/{search}")

    def _on_create(self) -> None:
        if op := add_deck_dialog(parent=self.mw):
            op.run_in_background()

    ######################################################################

    def _confirm_upgrade(self) -> None:
        self.mw.col.mod_schema(check=True)
        self.mw.col.upgrade_to_v2_scheduler()

        showInfo(tr.scheduling_update_done())
        self.refresh()
