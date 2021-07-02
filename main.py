import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from level_select import LevelSelect

def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = LevelSelect()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()