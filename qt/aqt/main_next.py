from __future__ import annotations

import json
from argparse import Namespace
from dataclasses import asdict, dataclass

import aqt
from aqt import *
from aqt import gui_hooks
from aqt.sound import av_player
from aqt.overview import Overview
from aqt.deckbrowser import DeckBrowser
from aqt.customstudy import CustomStudy
from aqt.debug_console import show_debug_console
from aqt.main import AnkiQt, MainWebView, MainWindowState
from aqt.toolbar_next import Toolbar, StatusBar
from aqt.theme import theme_manager
from aqt.webview import AnkiWebView, AnkiWebViewKind
from aqt.profiles import ProfileManager as ProfileManagerType
from anki._backend import RustBackend as _RustBackend
from typing import Any, Literal
from anki.decks import DeckCollapseScope, DeckId
from aqt.deckoptions import display_options_for_deck, display_options_for_deck_id
from aqt.utils import KeyboardModifiersPressed
from google.protobuf.json_format import MessageToJson

from aqt.operations.scheduling import (
    empty_filtered_deck,
    rebuild_filtered_deck,
    unbury_deck,
)

from aqt.operations.deck import set_deck_collapsed, set_current_deck

# Ideally everyone should use JavaScript as soon as an API is available,
# but I think it's unrealistic to go completely Python-less in the near future
# TODO: Allow restricting content to specific MainPageContext (e.g. CUSTOM_STUDY)


@dataclass
class DeckBrowserContent:
    toolbar: [str]


@dataclass
class OverviewContent:
    body: [str]


@dataclass
class AddonContent:
    """Stores dictionaries containing lists of HTML strings
    that can extended by add-ons to add content to the main page (see ts/main)

    Attributes:
        tree {str} -- HTML of the deck tree section
        stats {str} -- HTML of the stats section
    """

    deckBrowser: DeckBrowserContent
    toolbar: aqt.toolbar_next.ToolbarContent
    status_bar: aqt.toolbar_next.StatusBarContent
    overview: OverviewContent


class MainPage:
    _dueTree: DeckTreeNode

    def __init__(self, mw: AnkiQtNext) -> None:
        self.mw = mw
        self.web = mw.web
        self._addon_content_fetched = False
        # legacy classes (share methods while legacy and next coexist)
        self._legacy_deck_browser = DeckBrowser(self.mw)
        self._legacy_overview = Overview(self.mw)

        self.web.set_bridge_command(self._bridge, self.mw)
        self.web.load_ts_page("main")

    def show(self) -> None:
        av_player.stop_and_clear_queue()
        self.refresh()

    def refresh(self) -> None:
        self._refresh_needed = False
        self.mw.col.reset()
        self.updateWeb()
        self.web.setFocus()

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

    # Webview setup
    ##########################################################################

    def updateWeb(self, reuse: bool = False) -> None:
        """Update webview variables to display changed state"""

        if not reuse:
            self._dueTree = self.mw.col.sched.deck_due_tree()
        self.__updateWeb()

    def __updateWeb(self) -> None:
        from aqt.toolbar_next import ToolbarContent, StatusBarContent

        self.deck = self.mw.col.decks.current()
        self.sid = self.deck.get("sharedFrom")
        self.sidVer = self.deck.get("ver", None)

        if not self._addon_content_fetched:
            legacy_toolbar_content = self.mw.toolbar.content()
            self.addon_content = asdict(
                AddonContent(
                    deckBrowser=DeckBrowserContent(toolbar=[""]),
                    toolbar=legacy_toolbar_content,
                    status_bar=StatusBarContent(
                        leftTrayContent=[""], rightTrayContent=[""]
                    ),
                    overview=OverviewContent(body=[""]),
                )
            )
            # TODO: implement hook
            # gui_hooks.main_page_will_update(self, self.addon_content)

            self._addon_content_fetched = True

        args = {
            "profiles": {
                "current": self.mw.pm.name,
                "other": [p for p in self.mw.pm.profiles() if p != self.mw.pm.name],
            },
            "schedulerVersion": self.mw.col.sched_ver(),
            "deck": {
                "id": self.deck["id"],
                "name": self.deck["name"],
                "description": self.deck.get("desc", ""),
                "markdownDescription": self.deck.get("md", True),
                "finished": self.mw.col.sched._is_finished(),
                "hasBuried": self.mw.col.sched.have_buried(),
                "isDyn": self.mw.col.decks.current()["dyn"] == 1,
                "url": f"{aqt.appShared}info/{self.sid}?v={self.sidVer}"
                if self.sid
                else "",
            },
            "defaultStatsDays": self.mw.pm.default_stats_days(),
            "addonContent": self.addon_content,
        }

        # self._dueTree: DeckTreeNode is a protobuf message and needs special handling
        self.web.eval(
            f"""anki.updateMainPage(Object.assign({json.dumps(args)}, {{dueTree: {MessageToJson(self._dueTree)} }})); """
        )

        # legacy hook
        gui_hooks.deck_browser_did_render(self)

    def _bridge(self, cmd: str) -> bool:
        handled = True

        if self.mw.state == "review" and self.reviewer._linkHandler(cmd):
            return True

        if ":" in cmd:
            (cmd, arg) = cmd.split(":", 1)
        else:
            cmd = cmd

        # Common commands
        ##########################################################################

        if cmd == "browserSearch":
            browser = aqt.dialogs.open("Browser", self.mw)
            browser.search_for(arg)

        # Toolbar commands
        ##########################################################################

        elif cmd == "home":
            self.mw.on_home()
        elif cmd == "add":
            self.mw.onAddCard()
        elif cmd == "browse":
            self.mw.onBrowse()
        elif cmd == "stats":
            self.mw.on_stats()
        elif cmd == "toggleTheme":
            theme_manager.toggle_temp_dark_mode()

        # former deckbrowser.py commands
        if cmd == "select" and arg != self.deck:
            self._set_current_deck(DeckId(int(arg)))
        elif cmd == "context":
            self._legacy_deck_browser._showOptions(arg)
        elif cmd == "shared":
            self._legacy_deck_browser._onShared()
        elif cmd == "import":
            self.mw.onImport()
        elif cmd == "create":
            self._legacy_deck_browser._on_create()
        elif cmd == "drag":
            source, target = arg.split(",")
            self._legacy_deck_browser._handle_drag_and_drop(
                DeckId(int(source)), DeckId(int(target or 0))
            )
        elif cmd == "collapse":
            self._set_collapsed(DeckId(int(arg)), True)
        elif cmd == "expand":
            self._set_collapsed(DeckId(int(arg)), False)
        elif cmd == "v2upgrade":
            self._legacy_deck_browser._confirm_upgrade()
        elif cmd == "v2upgradeinfo":
            openLink("https://faqs.ankiweb.net/the-anki-2.1-scheduler.html")
        # former overview.py commands
        elif cmd == "study":
            self.mw.col.startTimebox()
            self.mw.moveToState("review")
            if self.mw.state == "home":
                tooltip(tr.studying_no_cards_are_due_yet())
        elif cmd == "opts":
            display_options_for_deck(self.mw.col.decks.current())
        elif cmd == "cram":
            aqt.dialogs.open("FilteredDeckConfigDialog", self)
        elif cmd == "refresh":
            self.legacy_overview.rebuild_current_filtered_deck()
        elif cmd == "empty":
            self.legacy_overview.empty_current_filtered_deck()
        elif cmd == "decks":
            self.web.eval("anki.showDecks(); ")
        elif cmd == "studymore" or cmd == "customStudy":
            self.on_study_more()
        elif cmd == "unbury":
            self.legacy_overview.on_unbury()
        elif cmd.startswith("description:"):
            (_, md, desc) = cmd.split(":", 2)
            markdown = md == "true"
            self.save_description(desc, markdown)
        elif cmd.lower().startswith("http"):
            openLink(cmd)

        elif cmd == "profile":
            self.mw.switch_profile(arg)

        # Add-on commands (lowest precedence to prevent conflicts)
        ##########################################################################

        elif cmd in self.mw.addon_link_handler:
            self.mw.addon_link_handler[cmd]()
        else:
            handled = False

        return handled


    def _set_current_deck(self, deck_id: DeckId):
        set_current_deck(parent=self.mw, deck_id=deck_id).success(
            lambda _: self.updateWeb()
        ).run_in_background(initiator=self)

    def on_study_more(self) -> None:
        self.web.eval("anki.setupCustomStudy(); ")

    # Deck context menu
    def _show_deck_context_menu(self, deck_id: str) -> None:
        m = QMenu(self.mw)
        a = m.addAction(tr.actions_rename())
        qconnect(
            a.triggered,
            lambda b, did=deck_id: self._legacy_deck_browser._rename(DeckId(int(deck_id))),
        )
        a = m.addAction(tr.actions_options())
        qconnect(
            a.triggered,
            lambda b, did=deck_id: self._legacy_deck_browser._showOptions(DeckId(int(deck_id))),
        )
        a = m.addAction(tr.actions_export())
        qconnect(
            a.triggered,
            lambda b, did=deck_id: self._legacy_deck_browser._export(DeckId(int(deck_id))),
        )
        a = m.addAction(tr.actions_delete())
        qconnect(
            a.triggered,
            lambda b, did=deck_id: self._legacy_deck_browser._delete(DeckId(int(deck_id))),
        )
        gui_hooks.deck_browser_will_show_options_menu(m, int(deck_id))
        m.popup(QCursor.pos())

    def _set_collapsed(self, deck_id: DeckId, collapsed: bool) -> None:
        node = self.mw.col.decks.find_deck_in_tree(self._dueTree, deck_id)
        if node:
            set_deck_collapsed(
                parent=self.mw,
                deck_id=deck_id,
                collapsed=collapsed,
                scope=DeckCollapseScope.REVIEWER,
            ).success(lambda _: self.updateWeb(reuse=True)).run_in_background()

    # adapted from deckdescription.py
    def save_description(self, description: str, markdown: bool) -> None:
        self.deck["desc"] = description
        self.deck["md"] = markdown
        update_deck_dict(parent=self, deck=self.deck).run_in_background()


class AnkiQtNext(AnkiQt):
    addon_link_handler: dict[str, Callable]

    def __init__(
        self,
        app: aqt.AnkiApp,
        profileManager: ProfileManagerType,
        backend: _RustBackend,
        opts: Namespace,
        args: list[Any],
    ) -> None:
        self.addon_link_handler = {}
        super().__init__(app, profileManager, backend, opts, args)
        self.deckBrowser = self.overview = self.main_page
        self.setup_keys()

    # Used by ProfileSelector in MainPage.svelte
    def switch_profile(self, name: str) -> None:
        """Switch to profile with given name."""

        if name not in self.pm.profiles():
            tooltip(tr.profiles_profile_does_not_exist())
            return

        def loadProfile() -> None:
            self.pm.load(name)
            self.loadProfile()

        self.unloadProfile(loadProfile)

    def set_refresh_needed(self, needed: bool) -> None:
        self.web.eval(f"anki.setRefreshNeeded({json.dumps(needed)}); ")

    def on_home(self) -> None:
        self.col.reset()
        self.moveToState("home")

    def _homeState(self, oldState: MainWindowState) -> None:
        self.web.show()
        self.web.eval("anki.setHomeState(); ")

    def on_stats(self) -> None:
        deck = self._selectedDeck()
        if not deck:
            return
        want_old = KeyboardModifiersPressed().shift
        if want_old:
            aqt.dialogs.open("DeckStats", self)
        elif KeyboardModifiersPressed().control:
            aqt.dialogs.open("NewDeckStats", self)
        else:
            self.web.eval("anki.setupStats(); ")

    def on_find_deck(self) -> None:
        self.web.eval("anki.focusSearch(); ")

    # Override AnkiQt methods
    ##########################################################################

    def show(self) -> None:
        self.main_page.show()
        super().show()

    def interactiveState(self) -> bool:
        "True if not in profile manager, syncing, etc."
        return self.state in ("review", "home")

    def _deckBrowserState(self, oldState: MainWindowState) -> None:
        self.web.eval("anki.setHomeState(); ")

    def _overviewState(self, oldState: MainWindowState) -> None:
        if not self._selectedDeck():
            return self.moveToState("deckBrowser")
        self.web.eval("anki.setHomeState(); ")

    def _reviewState(self, oldState: MainWindowState) -> None:
        self.reviewer.show()

    def _reviewCleanup(self, newState: MainWindowState) -> None:
        if newState != "resetRequired" and newState != "review":
            self.reviewer.cleanup()

    def fade_out_webview(self) -> None:
        self.set_refresh_needed(True)

    def fade_in_webview(self) -> None:
        self.set_refresh_needed(False)

    def onRefreshTimer(self) -> None:
        if self.state == "home":
            self.main_page.refresh()

    def setupMenus(self) -> None:
        super().setupMenus()
        qconnect(self.form.actionFindDeck.triggered, self.on_find_deck)

    def setupMainWindow(self) -> None:
        # main window
        self.form = aqt.forms.main.Ui_MainWindow()
        self.form.setupUi(self)
        # main area
        self.web = MainWebView(self)
        self.main_page = MainPage(self)
        # toolbar
        self.toolbar = Toolbar(self)
        # status bar
        self.status_bar = StatusBar(self)
        # add in a layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.web)
        self.form.centralwidget.setLayout(self.mainLayout)

        # force webengine processes to load before cwd is changed
        if is_win:
            self.web.force_load_hack()

        gui_hooks.card_review_webview_did_init(self.web, AnkiWebViewKind.MAIN)

    # Defer AnkiQt setupKeys until MainPage is set
    ##########################################################################

    def setupKeys(self) -> None:
        self.stateShortcuts: list[QShortcut] = []

    def setup_keys(self) -> None:
        globalShortcuts = [
            ("Ctrl+:", show_debug_console),
            ("Escape", lambda: self.moveToState("home")),
            ("d", lambda: self.web.eval("anki.showDecks(); ")),
            ("s", self.onStudyKey),
            ("a", self.onAddCard),
            ("b", self.onBrowse),
            ("t", self.on_stats),
            ("y", self.on_sync_button_clicked),
            (
                "o",
                lambda: display_options_for_deck(self.col.decks.current()),
            ),
            ("r", self.main_page._legacy_overview.rebuild_current_filtered_deck),
            ("e", self.main_page._legacy_overview.empty_current_filtered_deck),
            ("c", self.main_page._legacy_overview.onCustomStudyKey),
            ("u", self.main_page._legacy_overview.on_unbury),
            ("Ctrl+Shift+I", self.onImport),
        ]
        self.applyShortcuts(globalShortcuts)
