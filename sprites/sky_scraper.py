import os
from typing import List

import arcade

from birds_game_wall.wall_generator import WallGeneratorWorker
from constants import SKY_SCRAPER_SCALING


class SkyScraper(arcade.Sprite):
    """ SkyScraper dynamic sprite """

    def __init__(self, numbers: List[int], scale: float = SKY_SCRAPER_SCALING, id: int = 0):
        self.id: int = id
        self.thread: WallGeneratorWorker = None
        self.loaded = False
        self.filename = "current-wall%i.png" % self.id
        super().__init__(scale=scale)
        self.start_loading_image(numbers)

    def start_loading_image(self, numbers: List[int]):
        self.loaded = False
        print("reload_image", numbers)
        self.texture = arcade.load_texture("birds_game_wall/current_wall.png")
        self.thread = WallGeneratorWorker(
            self.id,
            "Thread-%i" % self.id,
            numbers=numbers,
            filename=self.filename
        )
        self.thread.start()

    def load_image(self):
        print("on_done", self.filename)
        filepath = "birds_game_wall/" + self.filename
        try:
            print(filepath)
            self.texture = arcade.load_texture(filepath)
        except:
            print("error")
        self.loaded = True
        print("completed")
        os.remove(filepath)

    def move_forward(self, how_many: int = 1) -> float:
        self.center_x += 1250 * how_many
        self.scale = SKY_SCRAPER_SCALING
        return self.center_x
