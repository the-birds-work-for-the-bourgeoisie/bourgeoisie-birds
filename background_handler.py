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
    def __init__(self, default_player_speed, level):
        # creates a new Sprite 
        super().__init__()

        # set up sprite lists for the backgrounds
        self.bg_sky_list = SpriteList()      # the two skies (back)
        self.bg_skyline_list = SpriteList()  # the two skylines (middle)
        self.bg_building_list = SpriteList() # the two buildings (front)
        self.bg_all_list = SpriteList()      # all six sprites

        # time of day chosen based on level selected by user 
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
        bg_sky_img = "assets-src/bg_{}_0.png"
        bg_sky_img = bg_sky_img.format(self.theme)
        bg_skyline_img = "assets-src/bg_{}_1.png"
        bg_skyline_img = bg_skyline_img.format(self.theme)
        bg_buildings_img = "assets-src/bg_{}_2.png"
        bg_buildings_img = bg_buildings_img.format(self.theme)

        # set up speeds for each background layer
        self.default_player_speed = default_player_speed
        bg_speed_0 = self.default_player_speed * 0.90 # 90% of player speed
        bg_speed_1 = self.default_player_speed * 0.80 # 80% of player speed
        bg_speed_2 = self.default_player_speed * 0.60 # 60% of player speed

        # set up first sky (back) image
        bg_sprite_0a = arcade.Sprite(bg_sky_img)
        bg_sprite_0a.center_x = 1000
        bg_sprite_0a.center_y = 325
        bg_sprite_0a.change_x = bg_speed_0
        self.bg_sky_list.append(bg_sprite_0a)

        # set up second sky (back) image
        bg_sprite_0b = arcade.Sprite(bg_sky_img)
        bg_sprite_0b.center_x = -1000
        bg_sprite_0b.center_y = 325
        bg_sprite_0b.change_x = bg_speed_0
        self.bg_sky_list.append(bg_sprite_0b)

        # set up first skyline (middle) image
        bg_sprite_1a = arcade.Sprite(bg_skyline_img)
        bg_sprite_1a.center_x = 1000
        bg_sprite_1a.center_y = 325
        bg_sprite_1a.change_x = bg_speed_1
        self.bg_skyline_list.append(bg_sprite_1a) 

        # set up second skyline (middle) image
        bg_sprite_1b = arcade.Sprite(bg_skyline_img)
        bg_sprite_1b.center_x = -1000
        bg_sprite_1b.center_y = 325
        bg_sprite_1b.change_x = bg_speed_1
        self.bg_skyline_list.append(bg_sprite_1b) 

        # set up first building (front) image 
        bg_sprite_2a = arcade.Sprite(bg_buildings_img)
        bg_sprite_2a.center_x = 1000
        bg_sprite_2a.center_y = 325
        bg_sprite_2a.change_x = bg_speed_2
        self.bg_building_list.append(bg_sprite_2a) 

        # set up second building (front) image 
        bg_sprite_2b = arcade.Sprite(bg_buildings_img)
        bg_sprite_2b.center_x = -1000
        bg_sprite_2b.center_y = 325
        bg_sprite_2b.change_x = bg_speed_2
        self.bg_building_list.append(bg_sprite_2b)

        # combine all backgrounds into one nice list for later 
        self.bg_all_list.extend(self.bg_sky_list)
        self.bg_all_list.extend(self.bg_skyline_list)
        self.bg_all_list.extend(self.bg_building_list)


    """ 
    Update - updates/animates the background sprites frame-by-frame
    """
    def update(self, player_speed, player_location):

        # if the player is moving, all backgrounds can move
        if player_speed == self.default_player_speed:
            for sprite in self.bg_all_list:
                sprite.center_x += sprite.change_x

        # if the player isn't moving (aka dead), only the sky should move
        elif player_speed == 0:
            for sprite in self.bg_sky_list:
                # speed is now -0.15 to simulate leisurely-moving clouds 
                # while the camera is not moving 
                sprite.center_x += -0.15

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