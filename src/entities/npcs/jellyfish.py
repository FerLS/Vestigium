from entities.npcs.floating_npc import FloatingEntity
from utils.constants import SCALE_FACTOR


class Jellyfish(FloatingEntity):
    """
    Represents a jellyfish NPC in the game. The jellyfish moves along a specified axis,
    emits light, and plays an animation.
    """

    def __init__(self, x: int, y: int, move_axis: str, initial_direction: int) -> None:
        """
        Initializes the jellyfish NPC.

        :param x: The initial x-coordinate of the jellyfish.
        :param y: The initial y-coordinate of the jellyfish.
        :param move_axis: The axis of movement ('vertical' or 'horizontal').
        :param initial_direction: The initial direction of movement (1 for forward, -1 for backward).
        """
        super().__init__(
            x=x,
            y=y,
            sprite_sheet_path="jellyfish_spritesheet.png",
            frame_width=64,
            frame_height=64,
            frame_count=8,
            move_distance=180 * SCALE_FACTOR,
            speed=2,
            initial_direction=initial_direction,
            scale=SCALE_FACTOR // 1.5,
            move_axis=move_axis,
            flip_on_reverse=False,
            draw_light=True,
            light_radius=25 * SCALE_FACTOR,
        )
        # Calls the parent class constructor to initialize the jellyfish's properties.
