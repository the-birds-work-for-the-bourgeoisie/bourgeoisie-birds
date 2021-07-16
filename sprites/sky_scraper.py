import arcade
from constants import SKY_SCRAPER_SCALING


class SkyScraper(arcade.Sprite):
    """ SkyScraper dynamic sprite """

    def __init__(self, scale: float = SKY_SCRAPER_SCALING):
        super().__init__(scale=scale)
        self.reload_image()

    def reload_image(self):
        self.texture = arcade.load_texture("birds_game_wall/current_wall.png")

    def move_forward(self) -> float:
        self.center_x += 1250
        return self.center_x
