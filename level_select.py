"""
The level select screen.
"""
# Import the needed modules
import arcade

# Define the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "BIRDS OF THE BORDUASIE"

class LevelSelect(arcade.View):

    def on_show(self):
        
        arcade.set_background_color(arcade.csscolor.AQUAMARINE)
        
        arcade.set_viewport(0, SCREEN_WIDTH -1, 0, SCREEN_HEIGHT -1 )

    def on_draw(self):

        arcade.start_render()
        arcade.draw_text("Level Select Screen", SCREEN_WIDTH - 460, SCREEN_HEIGHT - 150, arcade.color.ALLOY_ORANGE)


window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
start_view = LevelSelect()
window.show_view(start_view)
arcade.run()
