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


from typing import List, Union, Tuple, Type

from ..editor import Editor

from . import actions, triggers
from .state import State


class Rule:
    def __init__(
        self,
        trigger: Union[str, triggers.BaseTrigger],
        action: Type[actions.BaseAction],
        always_continue: bool = False,
    ):
        if isinstance(trigger, str):
            trigger = triggers.SimpleTrigger(trigger)
        self.trigger = trigger
        self.action = action
        self.always_continue = always_continue

    def process(
        self, key: str, editor: Editor, state: State
    ) -> Tuple[State, bool]:
        continue_ = True
        if self.trigger.is_triggered(key):
            state = self.action.perform(key, editor, state)
            continue_ = self.always_continue
        return state, continue_


class BaseMode:
    name: str = "Unnamed Mode"
    rules: List[Rule] = []

    @classmethod
    def handle_key(cls, key: str, editor: Editor, state: State) -> State:
        for rule in cls.rules:  # pragma: no branch
            state, continue_ = rule.process(key, editor, state)
            if not continue_:
                break
        return state

    @classmethod
    def help_text(cls) -> str:
        curmax = 0
        curmax = max([curmax] + [len(str(x.trigger.name)) for x in cls.rules])
        lines: List[str] = []
        for rule in cls.rules:
            triggername = str(rule.trigger.name).ljust(curmax, " ")
            lines.append(f"  {triggername} : {rule.action.name}")
        string_lines = "\n\n" + "\n".join(lines)
        return f"{cls.name}:{string_lines}"


COMMON_RULES = [
    Rule(triggers.end_of_text, actions.Exit),
    Rule(triggers.control_s, actions.Save),
]


ARROW_KEY_MOVEMENT = [
    Rule(triggers.key_up, actions.MoveUp),
    Rule(triggers.key_down, actions.MoveDown),
    Rule(triggers.key_left, actions.MoveLeft),
    Rule(triggers.key_right, actions.MoveRight),
]

FULL_MOVEMENT = ARROW_KEY_MOVEMENT + [
    Rule(triggers.numeric, actions.AddKeyToMultiplier),
    Rule("g", actions.MoveToLine),
    Rule("k", actions.MoveUp),
    Rule("j", actions.MoveDown),
    Rule("h", actions.MoveLeft),
    Rule("l", actions.MoveRight),
    Rule(triggers.numeric, actions.AddKeyToMultiplier),
    Rule("g", actions.MoveToLine),
    Rule("k", actions.MoveUp),
    Rule("j", actions.MoveDown),
    Rule("h", actions.MoveLeft),
    Rule("l", actions.MoveRight),
]


class SetBookmarkMode(BaseMode):
    name = "Bookmark Set Mode"
    rules = (
        COMMON_RULES
        + ARROW_KEY_MOVEMENT
        + [Rule(triggers.alphanumeric, actions.SetBookmark)]
    )


class GoToBookmarkMode(BaseMode):
    name = "Goto Bookmark Mode"
    rules = COMMON_RULES + [Rule(triggers.alphanumeric, actions.GoToBookmark)]


class InsertMode(BaseMode):
    name = "Insert Mode"
    rules = (
        COMMON_RULES
        + ARROW_KEY_MOVEMENT
        + [
            Rule(triggers.delete, actions.Delete),
            Rule(triggers.backspace, actions.Backspace),
            Rule(triggers.escape, actions.SwitchToCommandMode),
            Rule(triggers.any_other, actions.InsertKey),
        ]
    )


class CommandMode(BaseMode):
    name = "Command Mode"
    rules = (
        COMMON_RULES
        + FULL_MOVEMENT
        + [
            Rule("n", actions.FindNext),
            Rule("N", actions.FindPrevious),
            Rule("i", actions.SwitchToInsertMode),
            Rule("a", actions.SwitchToInsertModeAfter),
            Rule("A", actions.SwitchToInsertModeAfterLine),
            Rule("I", actions.SwitchToInsertModeStartLine),
            Rule("J", actions.JoinLines),
            Rule("?", actions.SwitchToSearchMode),
            Rule("/", actions.SwitchToCaseInsensitiveSearchMode),
            Rule("u", actions.Undo),
            Rule("r", actions.Redo),
            Rule("v", actions.StartMultiSelection),
            Rule("V", actions.SwitchToVisualLineMode),
            Rule("y", actions.Copy),
            Rule("p", actions.Paste),
            Rule("d", actions.DeleteBetween),
            Rule("m", actions.SwitchToBookmarkMode),
            Rule("'", actions.SwitchToGoToBookmarkMode),
        ]
    )


class VisualLineMode(BaseMode):
    name = "Visual Line Mode"
    rules = (
        COMMON_RULES
        + FULL_MOVEMENT
        + [
            Rule("i", actions.SwitchToInsertMode),
            Rule("a", actions.SwitchToInsertModeAfter),
            Rule("A", actions.SwitchToInsertModeAfterLine),
            Rule("I", actions.SwitchToInsertModeStartLine),
            Rule(triggers.escape, actions.SwitchToCommandMode),
            Rule("y", actions.CopyLines),
            Rule("d", actions.DeleteLines),
        ]
    )


class SearchMode(BaseMode):
    name = "Search Mode"
    rules = COMMON_RULES + [
        Rule(triggers.escape, actions.SwitchToCommandMode),
        Rule(triggers.backspace, actions.SearchBackspace),
        Rule(triggers.enter, actions.SwitchToCommandMode),
        Rule(triggers.any_other, actions.SearchAddCharacter),
    ]


class KeyHandler:
    modes = {
        "command": CommandMode,
        "insert": InsertMode,
        "search": SearchMode,
        "visual_line": VisualLineMode,
        "set_bookmark": SetBookmarkMode,
        "goto_bookmark": GoToBookmarkMode,
    }

    def __init__(self, editor: Editor) -> None:
        self.state = State()
        self.editor = editor

    def handle_key(self, key: str) -> None:
        mode = self.modes[self.state.mode]
        self.state = mode.handle_key(key, self.editor, self.state)

    @classmethod
    def help_text(cls) -> str:
        return "\n\n".join(mode.help_text() for mode in cls.modes.values())
