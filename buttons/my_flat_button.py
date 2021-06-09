from typing import List, Callable

import arcade.gui


class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    callables: List[Callable] = None

    def on_click(self):
        """ Called when user lets off button """
        for c in self.callables:
            c()

    def add_event_listener(self, event_handler: Callable):
        if self.callables is None:
            self.callables = []
        self.callables.append(event_handler)