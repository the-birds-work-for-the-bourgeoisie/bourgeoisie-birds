"""
The level select screen.
"""
# Import the needed modules

import arcade
import arcade.gui
from arcade.gui import UIManager

from buttons.my_flat_button import MyFlatButton
from my_game_view import MyGame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class LevelSelect(arcade.View):
    def __init__(self, game_view=None):
        super().__init__()
        self.ui_manager = UIManager()
        self.awesome = 2
        self.game_view = game_view

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
            center_x=750,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.BLACK,
            bg_color=(169, 169, 169),
            bg_color_hover=(255, 0, 0),
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(lambda: self.level(3))
        self.ui_manager.add_ui_element(button)

        # Button for level 2
        button = MyFlatButton(
            app=self,
            text='Level 2',
            center_x=500,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.BLACK,
            bg_color=(169, 169, 169),
            bg_color_hover=(255, 255, 0),
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(lambda: self.level(2))
        self.ui_manager.add_ui_element(button)
        
        # Button for level 1S
        button = MyFlatButton(
            text='Level 1',
            center_x=250,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.BLACK,
            font_color_press=arcade.color.BLACK,
            bg_color=(169, 169, 169),
            bg_color_hover=(0, 255, 0),
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.BLACK,
            border_color_hover=arcade.color.BLACK,
            border_color_press=arcade.color.WHITE
        )
        button.add_event_listener(lambda: self.level(1))
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Level Select Screen", 305, 475, arcade.color.PURPLE_MOUNTAIN_MAJESTY, font_size=40)

    def level(self, l: int):
        if self.game_view:
            self.game_view.setup()
            self.game_view.level = l
            self.window.show_view(self.game_view)

        else:
            new_view = MyGame(l)
            self.window.show_view(new_view)
