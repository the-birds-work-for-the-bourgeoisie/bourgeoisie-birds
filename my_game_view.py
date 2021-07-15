import math

import arcade
import random

# Constants used to scale our sprites from their original size
from arcade import SpriteList, Sprite

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites.answer import Answer
from sprites.bird import Bird

from background_handler import Background

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
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

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # keeps track of the player sprite's location from previous frame
        self.player_last_x = 0

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
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 150
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        map_name = "firstMap.tmx"
        platforms_layer_name = "Tile Layer 1"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=1,
                                                      use_spatial_hash=True)

        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        ys = [150, 350, 550]
        for i in range(3):
            answer = Answer(COIN_SCALING)
            answer.center_x = 1000
            answer.center_y = ys[i]
            answer.set_number(20)
            self.answer_sprites.append(answer)

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
        self.wall_list.draw()
        self.player_sprite.draw()
        self.answer_sprites.draw()
        self.draw_stats()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):

        # --- Manage Animations ---
        self.player_sprite.on_update(delta_time)

    def update(self, delta_time):
        """ Movement and game logic """
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

        greatest = 0

        for wall in self.wall_list:
            if wall.center_x > greatest:
                greatest = wall.center_x

        for wall in self.wall_list:
            if wall.center_x < self.player_sprite.center_x - 800:
                wall.center_x = greatest + (self.player_sprite._get_width() / 4)

        closest_sprite: Sprite = arcade.get_closest_sprite(self.player_sprite, self.answer_sprites)[0]
        if type(closest_sprite) == Answer and self.player_sprite.left > closest_sprite.left:
            print("hello")
            answer: Answer = closest_sprite
            is_correct = False
            if answer.is_correct:
                is_correct = True

            # player hit the correct answer
            if is_correct:
                self.score += 1

            # move and reset answers
            for answer in self.answer_sprites:
                if type(answer) == Answer:
                    a: Answer = answer
                    a.center_x += 1250
                    a.set_number(random.choice(list(range(-100, 100))))
                    a.is_correct = True

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
