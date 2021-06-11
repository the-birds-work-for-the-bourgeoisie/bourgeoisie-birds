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

from buttons.my_flat_button import MyFlatButton
from level_select2 import LevelSelect2
from main import MyGame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "BIRDS OF THE BORDUASIE"

class LevelSelect(arcade.View):
    def __init__(self, ):
        super().__init__()
        self.ui_manager = UIManager()
        self.awesome = 2

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_show_view(self):
        """ Called once when view is activated. """
        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4
        print("Setup")
        self.ui_manager.purge_ui_elements()
        
        # Button for level 3
        button = MyFlatButton(
            app=self,
            text='Level 3',
            center_x=right_column_x + 75,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.WHITE,
            bg_color=(169, 169, 169),
            bg_color_hover=(255, 0, 0),
            bg_color_press=(122, 21, 24),
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(self.level3)
        self.ui_manager.add_ui_element(button)

        # Button for level 2
        button = MyFlatButton(
            app=self,
            text='Level 2',
            center_x=right_column_x - 200,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.WHITE,
            bg_color=(169, 169, 169),
            bg_color_hover=(255, 255, 0),
            bg_color_press=(122, 21, 24),
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(self.level2)
        self.ui_manager.add_ui_element(button)
        
        # Button for level 1
        button = MyFlatButton(
            text='Level 1',
            center_x=right_column_x - 475,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.WHITE,
            bg_color=(169, 169, 169),
            bg_color_hover=(0, 255, 0),
            bg_color_press=(122, 21, 24),
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(self.level1)
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Level Select Screen", SCREEN_WIDTH - 600, SCREEN_HEIGHT - 150, arcade.color.PURPLE_MOUNTAIN_MAJESTY, font_size=40)

    def level1(self):
        new_view = LevelSelect2()
        self.window.show_view(new_view)

    def level2(self):
        new_view = LevelSelect2()
        self.window.show_view(new_view)

    def level3(self):
        new_view = LevelSelect2()
        self.window.show_view(new_view)

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
start_view = LevelSelect()
window.show_view(start_view)
arcade.run()
