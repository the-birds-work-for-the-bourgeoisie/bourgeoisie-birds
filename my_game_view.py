import math
import time
from typing import List

import arcade
# Constants used to scale our sprites from their original size
from arcade import SpriteList, Sprite
from arcade.gui import UIManager

import game_over
from background_handler import Background
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from equationGenerator import Equation
from sprites.answer import Answer
from sprites.bird import Bird
from sprites.sky_scraper import SkyScraper

CHARACTER_SCALING = 1
TILE_SCALING = 0.4
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 6

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH - LEFT_VIEWPORT_MARGIN
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100
STARTING_X_OFFSET = 500


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self, level: int = 1):
        super().__init__()
        self.score: int = 0
        self.level = level
        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None

        self.bg_list = None
        self.answer_sprites = SpriteList()
        self.sky_scraper_sprites = SpriteList()
        self.dead: bool = False

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.ui_manager = UIManager()

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.is_dead = False
        self.won = False
        self.sound = arcade.Sound("sound_files/dying2.mp3", True)
        # keeps track of the player sprite's location from previous frame
        self.player_last_x = 0

        # Initialize equations
        self.equations: List[Equation] = []  # First is current
        for i in range(3):
            self.equations.append(Equation(self.level))

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.courage_sound = arcade.load_sound("sound_files/courage screech.mp3")
        self.dying_sound_1 = arcade.load_sound("sound_files/dying1.mp3")
        self.dying_sound_2 = arcade.load_sound("sound_files/dying2.mp3")
        self.music1 = arcade.load_sound("sound_files/music1.mp3")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.setup()

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Create the Sprite lists
        self.wall_list = arcade.SpriteList()
        self.bg_list = Background(PLAYER_MOVEMENT_SPEED, self.level)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "assets-target/pixelbird2/"
        self.player_sprite = Bird(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 250
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Load in walls (invisible)
        self.wall_list = SpriteList()
        wall_offset = STARTING_X_OFFSET + 830
        create_wall_list = lambda x_offset = 0: [
            Sprite("stoneMid.png",
                   scale=TILE_SCALING,
                   center_x=wall_offset + x_offset,
                   center_y=SCREEN_HEIGHT // 2 - 100),
            Sprite("stoneMid.png",
                   scale=TILE_SCALING,
                   center_x=wall_offset + x_offset,
                   center_y=SCREEN_HEIGHT // 2 + 100),
        ]
        self.wall_list.extend(create_wall_list())
        self.wall_list.extend(create_wall_list(1250))

        ys = [
            116,
            316,
            516
        ]
        values = self.equations[0].answers
        for i in range(3):
            answer = Answer(COIN_SCALING)
            answer.center_x = 920 + STARTING_X_OFFSET
            answer.center_y = ys[i]
            answer.set_number(values[i])
            self.answer_sprites.append(answer)

        # create the sky scrapers
        center_x = STARTING_X_OFFSET + 920 - 1250 * 2
        center_y = SCREEN_HEIGHT // 2
        print([e.answers for e in self.equations])
        for i in range(3):
            values = self.equations[(i - 1) % len(self.equations)].answers
            sky_scraper = SkyScraper(values, id=i)
            sky_scraper.center_x = center_x
            sky_scraper.center_y = center_y
            center_x = sky_scraper.move_forward()
            self.sky_scraper_sprites.append(sky_scraper)
            if i == 0:
                # make the first invisible temporarily so it doesn't get in the way
                sky_scraper.scale = 0

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             0)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()  # invisible
        self.bg_list.draw()
        self.sky_scraper_sprites.draw()
        self.player_sprite.draw()
        self.draw_stats()
        self.answer_sprites.draw()  # invisible
        arcade.draw_text(self.equations[0].equationUnsolved(), 500 + self.view_left, 600 + self.view_bottom, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        # elif key == arcade.key.LEFT:
        #     self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        # elif key == arcade.key.RIGHT:
        #     self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        # elif key == arcade.key.LEFT:
        #     self.player_sprite.change_x = 0
        # elif key == arcade.key.RIGHT:
        #     self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):

        # --- Manage Animations ---
        self.player_sprite.on_update(delta_time)

    def update(self, delta_time):
        """ Movement and game logic """
        # Stop the player from leaving the screen
        if self.player_sprite.center_y > 600:
            self.player_sprite.change_y = 0
            self.player_sprite.center_y = 599
        elif self.player_sprite.center_y < 25:
            self.player_sprite.change_y = 0
            self.player_sprite.center_y = 26

        # record the player's last location to get their true speed
        self.player_last_x = self.player_sprite.center_x

        # Move the player with the physics engine
        self.physics_engine.update()

        # get player's speed and update backgrounds
        player_speed = self.player_sprite.center_x - self.player_last_x
        self.bg_list.update(player_speed, self.player_sprite.center_x)

        # --- Manage Scrolling ---

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        
        for wall in self.wall_list:
            if wall.center_x < self.player_sprite.center_x - 500:
                wall.center_x += 1250

        # if self.won:
        #     arcade.play_sound(self.courage_sound)
        #     time.sleep(1)
        #     new_view = game_won.GameWon()
        #     self.window.show_view(new_view)
        #     if wall.center_x < self.player_sprite.center_x - 500:
        #         wall.center_x += 2500

        # manage threads
        for i in range(len(self.sky_scraper_sprites)):
            ss: SkyScraper = self.sky_scraper_sprites[i]
            if not ss.thread.is_alive() and not ss.loaded:
                ss.load_image()
        current_equation = self.equations[0]
        closest_sprite: Sprite = arcade.get_closest_sprite(self.player_sprite, self.answer_sprites)[0]
        if type(closest_sprite) == Answer and self.player_sprite.left > closest_sprite.left:
            answer: Answer = closest_sprite

            # player hit the correct answer
            if answer.get_number() == current_equation.answer:
                self.score += 1
                # Reset the equation and answers
                self.get_new_equation()
                current_equation = self.equations[0]
            else:
                self.kill_bird()

            # move answers
            values = current_equation.answers
            for i in range(len(self.answer_sprites)):
                a: Answer = self.answer_sprites[i]
                a.center_x += 1250
                value = values[i]
                a.set_number(value)
                a.is_correct = current_equation.answer == value

            sprite: SkyScraper = self.sky_scraper_sprites.pop(0)
            center = (sprite.center_x, sprite.center_y)
            print("reloading", [e.answers for e in self.equations])
            new_sprite = SkyScraper(self.equations[1].answers, id=sprite.id)
            new_sprite.center_x = center[0]
            new_sprite.center_y = center[1]
            new_sprite.move_forward(how_many=3)
            self.sky_scraper_sprites.append(new_sprite)

        # bird death detection
        if player_speed == 0:
            print("Bird hit the wall")
            self.kill_bird()

    def kill_bird(self):
        self.dead = True
        print("Bird died")
        arcade.play_sound(self.dying_sound_2)
        time.sleep(1)
        new_view = game_over.GameOver(self)
        self.window.show_view(new_view)

    def draw_stats(self):
        start_x = SCREEN_WIDTH + self.view_left
        start_y = SCREEN_HEIGHT
        font_size = 20
        if self.score > 0:
            number_width = math.floor(math.log10(self.score) + 1) * font_size
        else:
            number_width = 1 * font_size
        arcade.draw_xywh_rectangle_filled(start_x - number_width, start_y - 100, width=100, height=100, color=arcade.color.BLACK)
        arcade.draw_text(str(self.score), start_x, start_y, arcade.color.WHITE, font_size,
                         anchor_x="right", anchor_y="top")

    def get_new_equation(self):
        self.equations.pop(0)
        self.equations.append(Equation(self.level))
        print("get_new_equation", [e.answers for e in self.equations])
