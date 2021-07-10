"""
Background Handler
Author: Grant Williams

This class implements the background sprites. They have their own class due to
their odd update() requirements allowing them to loop continuously, which is 
futher explained in said function.
"""

import arcade
from arcade.sprite_list import SpriteList

class Background(arcade.Sprite):

    """ 
    __init__ - sets up our background sprites
    """
    def __init__(self, speed, level):
        # creates a new Sprite 
        super().__init__()

        # set up sprite lists for the backgrounds
        self.bg_sky_list = SpriteList()      # the two skies (back)
        self.bg_skyline_list = SpriteList()  # the two skylines (middle)
        self.bg_building_list = SpriteList() # the two buildings (front)
        self.bg_all_list = SpriteList()      # all six sprites

        # allow level of difficulty to determine time of day
        self.theme = ""
        if level == 1:
            self.theme = "day"
        elif level == 2:
            self.theme = "dusk"
        elif level == 3:
            self.theme = "night"
        else:
            self.theme = "dawn"

        # set up file sources as dictated by previous if-else block 
        bg_sky = "assets-src/bg_{}_0.png"
        bg_sky = bg_sky.format(self.theme)
        bg_skyline = "assets-src/bg_{}_1.png"
        bg_skyline = bg_skyline.format(self.theme)
        bg_buildings = "assets-src/bg_{}_2.png"
        bg_buildings = bg_buildings.format(self.theme)

        # set up two sky (back) images
        bg_sprite = arcade.Sprite(bg_sky)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 0.5
        self.bg_sky_list.append(bg_sprite)
        # needs to be repeated to ensure second copy is made
        bg_sprite = arcade.Sprite(bg_sky)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 0.5
        self.bg_sky_list.append(bg_sprite)

        # set up two skyline (middle) images
        bg_sprite = arcade.Sprite(bg_skyline)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 1.5
        self.bg_skyline_list.append(bg_sprite) 
        # needs to be repeated to ensure second copy is made
        bg_sprite = arcade.Sprite(bg_skyline)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 1.5
        self.bg_skyline_list.append(bg_sprite) 

        # set up two building (front) images 
        bg_sprite = arcade.Sprite(bg_buildings)
        bg_sprite.center_x = 1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 2
        self.bg_building_list.append(bg_sprite) 
        # needs to be repeated to ensure second copy is made
        bg_sprite = arcade.Sprite(bg_buildings)
        bg_sprite.center_x = -1000
        bg_sprite.center_y = 325
        bg_sprite.change_x = speed - 2
        self.bg_building_list.append(bg_sprite)

        # combine all backgrounds into one nice list for later 
        self.bg_all_list.extend(self.bg_sky_list)
        self.bg_all_list.extend(self.bg_skyline_list)
        self.bg_all_list.extend(self.bg_building_list)


    """ 
    Update - updates/animates the background sprites frame-by-frame
    """
    def update(self, player_speed, player_location):

        # if the player is moving, all backgrounds can move
        if player_speed == 5:
            for sprite in self.bg_all_list:
                sprite.center_x += sprite.change_x

        # if the player isn't moving (aka dead), only the sky should move
        elif player_speed == 0:
            for sprite in self.bg_sky_list:
                # speed is now -0.5 (instead of 4.5) to match its apparent 
                # speed from the player's perspective 
                sprite.center_x += sprite.change_x - 5

        """
        A visual for the background images' unique updating.

        If the player (P) is past the middle of the image (A)...

        [  B  ][  A  ]
                  P
        
        ...then the other image (B) will "hop" in front of (A)...

               [  A  ][  B  ]
                  P

        ...and this pattern will continue on forever. It even works backwards,
        such as when the sky moves backwards once the player is dead.
        """

        # substitues for sky images's positions that are less unwieldy 
        sky_0_x = self.bg_sky_list[0].center_x
        sky_1_x = self.bg_sky_list[1].center_x

        # if the player is in the middle of an image, and the other image is
        # behind, then the other "hops" in front by 4000 pixels 
        if sky_0_x < player_location and sky_0_x > sky_1_x:
            self.bg_sky_list[1].center_x += 4000
        if sky_1_x < player_location and sky_1_x > sky_0_x:
            self.bg_sky_list[0].center_x += 4000

        # substitues for skyline images' positions that are less unwieldy
        skyline_0_x = self.bg_skyline_list[0].center_x
        skyline_1_x = self.bg_skyline_list[1].center_x

        # if the player is in the middle of an image, and the other image is
        # behind, then the other "hops" in front by 4000 pixels
        if skyline_0_x < player_location and skyline_0_x > skyline_1_x:
            self.bg_skyline_list[1].center_x += 4000
        if skyline_1_x < player_location and skyline_1_x > skyline_0_x:
            self.bg_skyline_list[0].center_x += 4000

        # substitues for buildings images' positions that are less unwieldy
        buildings_0_x = self.bg_building_list[0].center_x
        buildings_1_x = self.bg_building_list[1].center_x

        # if the player is in the middle of an image, and the other image is
        # behind, then the other "hops" in front by 4000 pixels
        if buildings_0_x < player_location and buildings_0_x > buildings_1_x:
            self.bg_building_list[1].center_x += 4000
        if buildings_1_x < player_location and buildings_1_x > buildings_0_x:
            self.bg_building_list[0].center_x += 4000


    """ 
    Draw - allows all six sprites to be drawn in the arcade view. 
    """
    def draw(self):
        # use the list of all sprites to draw them, nice and easy!
        for sprite in self.bg_all_list:
            sprite.draw()