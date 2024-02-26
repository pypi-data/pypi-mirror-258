#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Philip Zerull

# This file is part of "The Cursed Editor"

# "The Cursed Editor" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import logging

from typing import Optional, Tuple, Dict

from .mutable_string import MutableString


logger = logging.getLogger(__name__)


class LinearEditor:
    def __init__(
        self,
        content: str = "",
    ) -> None:
        self._mutable_string = MutableString(content)
        self._cursor = 0
        self._second_cursor = 0
        self._copied_text = ""
        self._bookmarks: Dict[str, int] = {}

    def _bound_value(self, value: int) -> int:
        value = max(value, 0)
        value = min(value, len(str(self)))
        return value

    @property
    def cursor(self) -> int:
        return self._cursor

    @cursor.setter
    def cursor(self, value: int) -> None:
        self._cursor = self._bound_value(value)

    @property
    def second_cursor(self) -> int:
        return self._second_cursor

    @second_cursor.setter
    def second_cursor(self, value: int) -> None:
        self._second_cursor = self._bound_value(value)

    def copy(
        self, *, start: Optional[int] = None, end: Optional[int] = None
    ) -> None:
        start, end = self._get_start_end(start=start, end=end)
        self._copied_text = self._mutable_string[start, end]

    def paste(self) -> None:
        self.insert(self._copied_text)

    def undo(self) -> None:
        result = self._mutable_string.undo()
        if result is not None:
            self.cursor = result

    def redo(self) -> None:
        result = self._mutable_string.redo()
        if result is not None:
            self.cursor = result

    def go_to_bookmark(self, name: str) -> None:
        if name in self._bookmarks:
            self.cursor = self._bookmarks[name]

    def set_bookmark(self, name: str, index: int) -> None:
        self._bookmarks[name] = index

    def handle_delete(self, length: int = 1) -> None:
        self._update_bookmarks_for_delete(
            start=self.cursor, end=self.cursor + length
        )
        self._mutable_string.delete(start=self.cursor, length=length)

    def delete_between(
        self, *, start: Optional[int] = None, end: Optional[int] = None
    ) -> None:
        start, end = self._get_start_end(start=start, end=end)
        self._update_bookmarks_for_delete(start=start, end=end)
        self._mutable_string.delete(start=start, end=end)
        self.cursor = start

    def _get_start_end(
        self, *, start: Optional[int] = None, end: Optional[int] = None
    ) -> Tuple[int, int]:
        if start is None:
            start = self.cursor
        if end is None:
            end = self.second_cursor
        start, end = sorted([start, end])
        return start, end

    def _update_bookmarks_for_delete(self, *, start: int, end: int) -> None:
        names_to_remove = []
        for name, index in self._bookmarks.items():
            if start <= index <= end:
                names_to_remove.append(name)
            elif index > end:
                self._bookmarks[name] = index - end + start
        for name in names_to_remove:
            del self._bookmarks[name]

    def handle_backspace(self) -> None:
        if self.cursor:
            self._mutable_string.delete(start=self.cursor - 1, length=1)
            self._update_bookmarks_for_delete(
                start=self.cursor - 1, end=self.cursor - 1
            )
            self.cursor = self.cursor - 1

    def insert(self, text: str) -> None:
        self._mutable_string.insert(index=self.cursor, text=text)
        self._update_bookmarks_for_insert(index=self.cursor, text=text)
        self.cursor = self.cursor + len(text)

    def _update_bookmarks_for_insert(self, *, index: int, text: str) -> None:
        for name, position in self._bookmarks.items():
            if position > index:
                self._bookmarks[name] = position + len(text)

    def incremental_search(
        self,
        needle: str,
        mode: str = "normal",
        case_sensitive: bool = True,
    ) -> None:
        positions = self._mutable_string.search(
            needle=needle, case_sensitive=case_sensitive
        )
        if mode == "reverse":
            positions.reverse()
        move_to = None
        for position in positions:
            if mode == "reverse" and position < self.cursor:
                move_to = position
                break
            if mode == "normal" and position > self.cursor:
                move_to = position
                break
            if mode == "same" and position >= self.cursor:
                move_to = position
                break
        if move_to is None and positions:
            move_to = positions[0]
        if move_to is not None:
            self.cursor = move_to

    def __str__(self) -> str:
        return str(self._mutable_string)
