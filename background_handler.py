"""
This handles all of the moving and recycling of background images.
"""

import arcade
from arcade.sprite_list import SpriteList

class Background(arcade.Sprite):

    def __init__(self, speed, level):
        super().__init__()

        self.bg_sky_list = SpriteList()      # the two skies 
        self.bg_skyline_list = SpriteList()  # the two skylines
        self.bg_building_list = SpriteList() # the two buildings
        self.theme = ""

        # allow level of difficulty to determine time of day
        if level == 1:
            self.theme = "day"
        elif level == 2:
            self.theme = "dusk"
        elif level == 3:
            self.theme = "night"

        bg_sky = "assets-src/bg_{}_0.png"
        bg_sky = bg_sky.format(self.theme)
        bg_skyline = "assets-src/bg_{}_1.png"
        bg_skyline = bg_skyline.format(self.theme)
        bg_buildings = "assets-src/bg_{}_2.png"
        bg_buildings = bg_buildings.format(self.theme)

        # Set up backgrounds
        bg_sprite = arcade.Sprite(bg_sky)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 0.5
        self.bg_sky_list.append(bg_sprite)
        # appended twice so we can loop it
        bg_sprite = arcade.Sprite(bg_sky)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 0.5
        self.bg_sky_list.append(bg_sprite)

        bg_sprite = arcade.Sprite(bg_skyline)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 1.5
        self.bg_skyline_list.append(bg_sprite) 
        # appended twice so we can loop it
        bg_sprite = arcade.Sprite(bg_skyline)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 1.5
        self.bg_skyline_list.append(bg_sprite) 

        bg_sprite = arcade.Sprite(bg_buildings)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 2
        self.bg_building_list.append(bg_sprite) 
        # appended twice so we can loop it
        bg_sprite = arcade.Sprite(bg_buildings)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 2
        self.bg_building_list.append(bg_sprite)

        self.bg_all_list = self.bg_sky_list
        self.bg_all_list.extend(self.bg_skyline_list)
        self.bg_all_list.extend(self.bg_building_list)

    def update(self, player_location):
        # allows backgrounds to move
        for sprite in self.bg_all_list:
            sprite.center_x += sprite.change_x

        """
        This next part needs a bit more explaining. If a player is past the 
        middle of an image (A), and there is another image (B) behind that
        one, then (B) will jump in front of (A), like leap frog!

        if the player (P) is past the middle of the image (A)...

        [  B  ][  A  ]
                  P
        
        ...then the other image (B) will go in front of (A)

               [  A  ][  B  ]
                  P

        and this pattern will continue as the player goes forward
        [  A  ][  B  ]
                  P

               [  B  ][  A  ]
                  P

        """

        # update sky
        if self.bg_sky_list[0].center_x < player_location and self.bg_sky_list[0].center_x > self.bg_sky_list[1].center_x:
            self.bg_sky_list[1].center_x += 4000
        if self.bg_sky_list[1].center_x < player_location and self.bg_sky_list[1].center_x > self.bg_sky_list[0].center_x:
            self.bg_sky_list[0].center_x += 4000

        # update skyline
        if self.bg_skyline_list[0].center_x < player_location and self.bg_skyline_list[0].center_x > self.bg_skyline_list[1].center_x:
            self.bg_skyline_list[1].center_x += 4000
        if self.bg_skyline_list[1].center_x < player_location and self.bg_skyline_list[1].center_x > self.bg_skyline_list[0].center_x:
            self.bg_skyline_list[0].center_x += 4000

        # update buildings 
        if self.bg_building_list[0].center_x < player_location and self.bg_building_list[0].center_x > self.bg_building_list[1].center_x:
            self.bg_building_list[1].center_x += 4000
        if self.bg_building_list[1].center_x < player_location and self.bg_building_list[1].center_x > self.bg_building_list[0].center_x:
            self.bg_building_list[0].center_x += 4000


    def draw(self):
        for sprite in self.bg_all_list:
            sprite.draw()