from typing import List, Callable

import arcade.gui
from arcade.gui import UIEvent


class MyInputBox(arcade.gui.UIInputBox):
    """
    To capture a button click, subclass the button and override on_click.
    """
    callables: List[Callable] = None

    def on_ui_event(self, event: UIEvent):
        """ Called when the something happens with the mouse or keyboard """
        super().on_ui_event(event)
        if event.type == arcade.gui.TEXT_INPUT:
            if len(self.text) > 3:
                self.text = self.text[:3]
            new_char = event.data['text']
            if not new_char.isalpha():
                self.text = self.text.replace(new_char, "")
            self.text = self.text.upper()
        elif event.type == arcade.gui.UIInputBox.ENTER:
            for c in self.callables:
                c()

    def add_event_listener(self, event_handler: Callable):
        if self.callables is None:
            self.callables = []
        self.callables.append(event_handler)