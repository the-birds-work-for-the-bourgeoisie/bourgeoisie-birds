import arcade
from arcade import Texture
from PIL import Image, ImageDraw, ImageFont

from constants import ANSWER_SCALING


class Answer(arcade.Sprite):
    """ Bird player animated sprite """

    def __init__(self, scale: float = ANSWER_SCALING):
        super().__init__(scale=scale)
        self.text = "0"
        self.texture = self._get_texture()

    def set_number(self, num: float):
        self.text = str(num)
        self.texture = self._get_texture()

    def _get_texture(self) -> Texture:
        img = Image.new('RGBA', (150, 150), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 70)
        d.text((10, 10), self.text, fill=(0, 0, 0, 255), font=fnt)
        return Texture(name="Answer{%s}" % self.text, image=img)
