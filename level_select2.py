"""
The level select screen.
"""
# Import the needed modules
from typing import Optional, Callable, List
import random

import arcade
import arcade.gui
from arcade.gui import UIManager

# Define the constants
from arcade.gui.ui_style import UIStyle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "BIRDS OF THE BORDUASIE2"

class LevelSelect2(arcade.View):
    def __init__(self, ):
        super().__init__()
        self.ui_manager = UIManager()
        self.awesome = 2

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.AQUAMARINE)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_show_view(self):
        """ Called once when view is activated. """
        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4
        print("Setup")
        self.ui_manager.purge_ui_elements()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Level Select Screen2", SCREEN_WIDTH - 460, SCREEN_HEIGHT - 150, arcade.color.ALLOY_ORANGE)