import os

import arcade
from arcade import Texture
from PIL import Image, ImageDraw, ImageFont

from constants import ANSWER_SCALING


class Answer(arcade.Sprite):
    """ Answer dynamic sprite """

    def __init__(self, scale: float = ANSWER_SCALING):
        super().__init__(scale=scale)
        # is_correct is used to detect if it is the right answer
        self._value = 0
        self._text = "0"
        self.texture = self._get_texture()

    def set_number(self, num: float):
        """
        Sets the displayed number as float
        """
        self._value = num
        self._text = str(num)
        self.texture = self._get_texture()

    def get_number(self) -> float:
        """
        Gets the displayed number as float
        """
        return self._value

    def _get_texture(self) -> Texture:
        img = Image.new('RGBA', (150, 150), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("arial.ttf" if os.name == 'nt' else "Arial.ttf", 70)
        d.text((10, 10), self._text, fill=(0, 0, 0, 255), font=fnt)
        return Texture(name="Answer{%s}" % self._text, image=img)
