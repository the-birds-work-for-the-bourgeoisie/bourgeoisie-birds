import arcade
from pathlib import Path

from constants import BIRD_SCALING, BIRD_ANIMATION_FPS
from utils import file_utils


class Bird(arcade.Sprite):
    """ Bird player animated sprite """

    def __init__(self, folder_name: str, scale: float = BIRD_SCALING):
        super().__init__(scale=scale)

        # settings
        self.scale = BIRD_SCALING
        self.animation_fps = BIRD_ANIMATION_FPS
        self.textures = []
        path_list = file_utils.get_files_in_folder_by_file_extension(folder_name, "png")
        for path in path_list:
            self.textures.append(arcade.load_texture(folder_name + path.name))
        self.texture = self.textures[0]
        self.time = 0

    def on_update(self, delta_time: float = 1/60):
        """ Animate the player. The physics engine does the movement """
        self.time += delta_time
        texture_index = int(self.time * self.animation_fps) % len(self.textures)
        self.texture = self.textures[texture_index]

