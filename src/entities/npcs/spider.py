from entities.npcs.floating_npc import FloatingEntity
from utils.constants import SCALE_FACTOR


class Spider(FloatingEntity):
    """
    Represents a spider NPC in the game. The spider moves vertically within a defined range
    and plays an animation.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the spider NPC.

        :param x: The initial x-coordinate of the spider.
        :param y: The initial y-coordinate of the spider.
        """
        super().__init__(
            x=x,
            y=y,
            sprite_sheet_path="spider_spritesheet.png",
            frame_width=32,
            frame_height=32,
            frame_count=4,
            move_distance=100,
            speed=0.5,
            initial_direction=1,
            scale=SCALE_FACTOR,
            move_axis="vertical",
            flip_on_reverse=True,
            draw_light=False,
            light_radius=10 * SCALE_FACTOR,
        )
        # Calls the parent class constructor to initialize the spider's properties.
