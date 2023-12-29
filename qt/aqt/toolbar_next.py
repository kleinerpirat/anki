# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
from __future__ import annotations

from dataclasses import dataclass
import enum
from typing import Any, Callable, List

import aqt
from anki._legacy import deprecated
from anki.sync import SyncStatus
from aqt import gui_hooks
from aqt.qt import *
from aqt.sync import get_sync_status

class HideMode(enum.IntEnum):
    FULLSCREEN = 0
    ALWAYS = 1

@dataclass
class ToolbarContent:
    leftTrayContent: [str]
    centerTrayContent: [str]
    rightTrayContent: [str]

@dataclass
class StatusBarContent:
    leftTrayContent: [str]
    rightTrayContent: [str]

class Bar:
    def __init__(self, mw: aqt.AnkiQtNext, name: str) -> None:
        self.mw = mw
        self._name = name

    def content(
        self,
    ) -> ToolbarContent | StatusBarContent:
        return (
            {
                "leftTrayContent": self._left_tray_content(),
                "centerTrayContent": self._center_tray_content(),
                "rightTrayContent": self._right_tray_content(),
            }
            if self._name == "toolbar"
            else {
                "leftTrayContent": self._left_tray_content(),
                "rightTrayContent": self._right_tray_content(),
            }
        )

    # Add-on API
    ######################################################################

    def _left_tray_content(self) -> List[str]:
        left_tray_content: list[str] = []
        getattr(gui_hooks, f"{self._name}_will_set_left_tray_content")(
            left_tray_content, self
        )
        return left_tray_content

    def _center_tray_content(self) -> List[str]:
        center_tray_content: list[str] = []
        getattr(gui_hooks, f"{self._name}_will_set_center_tray_content")(
            center_tray_content, self
        )
        return center_tray_content

    def _right_tray_content(self) -> List[str]:
        right_tray_content: list[str] = []
        getattr(gui_hooks, f"{self._name}_will_set_right_tray_content")(
            right_tray_content, self
        )
        return right_tray_content

    # We create our links in Svelte, but some add-on authors probably want a Python method.
    def create_link(
        self,
        cmd: str,
        label: str,
        func: Callable,
        tip: str | None = None,
        id: str | None = None,
    ) -> str:
        """Registers link handler and returns HTML link element (<a>)

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
            str -- HTML <a> element with provided label
        """

        self.mw.addon_link_handler[cmd] = func

        title_attr = f'title="{tip}"' if tip else ""
        id_attr = f'id="{id}"' if id else ""

        return (
            f"""<a class="hitem" tabindex="-1" aria-label="{label}" """
            f"""{title_attr} {id_attr} href="#" onclick="return pycmd('{cmd}')">"""
            f"""{label}</a>"""
        )


class Toolbar(Bar):
    def __init__(self, mw: aqt.AnkiQtNext) -> None:
        super().__init__(mw, "toolbar")
        # legacy aliases for add-ons
        self.link_handlers = mw.addon_link_handler
        self.web = mw.web

    @deprecated(info="use mw.mainPage.updateWeb instead")
    def draw(self) -> None:
        pass

    def redraw(self) -> None:
        self.set_sync_active(self.mw.media_syncer.is_syncing())
        self.update_sync_status()
        gui_hooks.toolbar_did_redraw(self)

    # Sync
    ######################################################################

    def set_sync_active(self, active: bool) -> None:
        self.mw.web.eval("")  # f"anki.setSyncActive({json.dumps(active)}); ")

    def set_sync_status(self, status: SyncStatus) -> None:
        self.mw.web.eval("")  # f"anki.setSyncStatus({status.required}); ")

    def update_sync_status(self) -> None:
        get_sync_status(self.mw, self.mw.toolbar.set_sync_status)


class StatusBar(Bar):
    def __init__(self, mw: aqt.AnkiQtNext) -> None:
        super().__init__(mw, "status_bar")

    # Profile
    ######################################################################

    def switch_profile(self, active: bool) -> None:
        self.mw.web.eval("")  # f"anki.setSyncActive({json.dumps(active)}); ")
