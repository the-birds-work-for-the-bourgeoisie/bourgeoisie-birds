"""
The game over screen
"""
# Import the needed modules

import arcade
import arcade.gui
from arcade.gui import UIManager
from buttons.my_flat_button import MyFlatButton
import level_select
import my_game_view
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOver(arcade.View):
    def __init__(self, ):
        super().__init__()
        self.ui_manager = UIManager()

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
        
        # Button for restarting level
        button = MyFlatButton(
            app=self,
            text='Restart Level',
            center_x=375,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=(169, 169, 169),
            bg_color_hover=arcade.color.ORANGE,
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.BLACK,
        )
        button.add_event_listener(self.restart)
        self.ui_manager.add_ui_element(button)

        # Button for level 2
        button = MyFlatButton(
            app=self,
            text='Main Menu',
            center_x=625,
            center_y=y_slot * 1,
            width=250,
            height=100
        )
        button.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=(169, 169, 169),
            bg_color_hover=arcade.color.BLUE,
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.BLACK,
        )
        button.add_event_listener(self.level_select)
        self.ui_manager.add_ui_element(button)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 350, 450, arcade.color.RED_DEVIL, font_size=50)

    def restart(self):
        new_view = my_game_view.MyGame()
        self.window.show_view(new_view)

    def level_select(self):
        new_view = level_select.LevelSelect()
        self.window.show_view(new_view)


