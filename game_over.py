"""
The game over screen
"""
# Import the needed modules

import arcade
import arcade.gui
from arcade.gui import UIManager, UIInputBox
from buttons.my_flat_button import MyFlatButton
import level_select
from buttons.my_input_box import MyInputBox
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from highscore_api import put_high_score, HighScore


class GameOver(arcade.View):
    def __init__(self, game_view, score: int):
        super().__init__()
        self.initials_input_box: MyInputBox = None
        self.high_score_button: MyFlatButton = None
        self.submitted = False
        self.ui_manager = UIManager()
        self.game_view = game_view
        self.score = score

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

        # Button for high score
        self.high_score_button = MyFlatButton(
            app=self,
            text='Submit High Score',
            center_x=SCREEN_WIDTH // 2 + 200,
            center_y=SCREEN_HEIGHT - 150,
            width=250,
            height=50,
        )
        self.high_score_button.set_style_attrs(
            font_color=arcade.color.BLACK,
            bg_color=arcade.color.GREEN,
            bg_color_hover=arcade.color.GO_GREEN,
            bg_color_press=arcade.color.WHITE,
            border_color=arcade.color.WHITE,
        )
        self.high_score_button.add_event_listener(self.submit_high_score)
        self.ui_manager.add_ui_element(self.high_score_button)

        self.initials_input_box = MyInputBox(
            text='initials',
            center_x=SCREEN_WIDTH // 2 - 200,
            center_y=SCREEN_HEIGHT - 150,
            width=250,
            height=50,
        )
        self.initials_input_box.add_event_listener(self.submit_high_score)
        self.ui_manager.add_ui_element(self.initials_input_box)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 350, 350, arcade.color.RED_DEVIL, font_size=50)
        arcade.draw_text("Your Score: %i" % self.score, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, arcade.color.WHITE, font_size=20, anchor_x="center")
        if self.submitted:
            arcade.draw_text("You score has been submitted!", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, arcade.color.GO_GREEN, font_size=20, anchor_x="center", anchor_y="center")

    def restart(self):
        self.game_view.setup()
        self.window.show_view(self.game_view)

    def level_select(self):
        new_view = level_select.LevelSelect(self.game_view)
        self.window.show_view(new_view)

    def submit_high_score(self):
        if not self.submitted:
            if put_high_score(HighScore(self.initials_input_box.text, self.score)):
                self.submitted = True
                self.high_score_button.scale = 0
                self.initials_input_box.scale = 0
