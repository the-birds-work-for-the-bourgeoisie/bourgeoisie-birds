import math

import arcade
import random

# Constants used to scale our sprites from their original size
from arcade import SpriteList, Sprite

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites.answer import Answer
from sprites.bird import Bird
from equationGenerator import Equation

from background_handler import Background
from sprites.sky_scraper import SkyScraper

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH - LEFT_VIEWPORT_MARGIN
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


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

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # keeps track of the player sprite's location from previous frame
        self.player_last_x = 0


        # Initialize equation generator
        self.current_equation = Equation(self.level)
        self.current_answer_set = set()
        self.current_equation.setIncorrectAnswers(self.current_answer_set)
        # self.current_answer_set.add(self.current_equation.answer)

        for i in range(10000):
            self.next_equation = Equation(self.level)
            self.next_answer_set = set()
            self.next_equation.setIncorrectAnswers(self.next_answer_set)
            print(len(self.next_answer_set), self.next_answer_set)
            assert len(self.next_answer_set) == 3

        # Initialize the next equation generator
        self.next_equation = Equation(self.level)
        self.next_answer_set = set()
        self.next_equation.setIncorrectAnswers(self.next_answer_set)

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

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
        self.player_sprite.center_y = 150
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Load in map
        map_name = "firstMap.tmx"
        platforms_layer_name = "Tile Layer 1"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=1,
                                                      use_spatial_hash=True)
        new_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=1,
                                                      use_spatial_hash=True)
        for i in new_list:
            i.center_x += 1250
            self.wall_list.append(i)

        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)


        ys = [150, 350, 550]
        values = list(self.current_answer_set)
        for i in range(3):
            answer = Answer(COIN_SCALING)
            answer.center_x = 1000
            answer.center_y = ys[i]
            answer.set_number(values[i])
            self.answer_sprites.append(answer)

        # create the sky scrapers
        center_x = 920 - 1250 * 2
        center_y = SCREEN_HEIGHT // 2
        for i in range(3):
            sky_scraper = SkyScraper()
            sky_scraper.center_x = center_x
            sky_scraper.center_y = center_y
            center_x = sky_scraper.move_forward()
            self.sky_scraper_sprites.append(sky_scraper)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             0)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.bg_list.draw()
        self.sky_scraper_sprites.draw()
        self.wall_list.draw()
        self.answer_sprites.draw()
        self.player_sprite.draw()
        self.draw_stats()
        arcade.draw_text(self.current_equation.equationUnsolved(), 500 + self.view_left, 600 + self.view_bottom, arcade.csscolor.WHITE, 18)

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
                wall.center_x += 2500

        closest_sprite: Sprite = arcade.get_closest_sprite(self.player_sprite, self.answer_sprites)[0]
        if type(closest_sprite) == Answer and self.player_sprite.left > closest_sprite.left:
            answer: Answer = closest_sprite

            # player hit the correct answer
            if answer.is_correct:
                self.score += 1
                # Reset the equation and answers
                self.get_new_equation()
            else:
                self.kill_bird()

            # move answers
            print(self.current_answer_set)
            values = list(self.current_answer_set)
            print("debug", values, self.current_equation.answer, self.current_equation.equationUnsolved())
            for i in range(len(self.answer_sprites)):
                a: Answer = self.answer_sprites[i]
                a.center_x += 1250
                print(values)
                value = values[i]
                a.set_number(value)
                a.is_correct = self.current_equation.answer == value

            sprite: SkyScraper = self.sky_scraper_sprites.pop(0)
            sprite.move_forward(how_many=2)
            self.sky_scraper_sprites.append(sprite)

        # bird death detection
        if player_speed == 0:
            self.kill_bird()

    def kill_bird(self):
        # TODO: Show end screen
        self.dead = True
        print("DEAD BIRD")

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
        # Set current equation to next equation
        self.current_equation = self.next_equation
        self.current_answer_set = self.next_answer_set
        print(len(self.current_answer_set), self.current_answer_set)
        assert len(self.current_answer_set) == 3
        # Reset the next equation
        self.next_equation = Equation(self.level)
        self.next_answer_set = set()
        self.next_equation.setIncorrectAnswers(self.next_answer_set)
        print(len(self.next_answer_set), self.next_answer_set)
        assert len(self.next_answer_set) == 3
