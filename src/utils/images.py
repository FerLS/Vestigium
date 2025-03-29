import pygame 

def extract_frames(
        sheet: pygame.Surface,
        start_x: int, start_y: int, 
        frame_width: int, frame_height: int, 
        num_frames: int, 
        scale_factor: int=1, 
        lying: float=None) -> list[pygame.Surface]:
    """
    Extracts animation frames from a sprite sheet.

    :param sheet: The sprite sheet surface.
    :param start_x: The starting x-coordinate of the first frame.
    :param start_y: The starting y-coordinate of the first frame.
    :param frame_width: The width of each frame.
    :param frame_height: The height of each frame.
    :param num_frames: The number of frames to extract.
    :param scale_factor: The factor by which to scale the frames (default is 1, no scaling).
    :param lying: The angle to rotate the frames (default is None, no rotation).
    :return: A list of extracted frames as pygame surfaces.
    """
    frames = []
    for i in range(num_frames):
        # Extract the frame
        frame = sheet.subsurface((start_x + i * frame_width, start_y, frame_width, frame_height))
        
        # Scale the frame if needed
        if scale_factor != 1:
            frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))

        # Rotate the frame if lying is True
        if lying is not None:
            frame = pygame.transform.rotate(frame, lying) 
    
        frames.append(frame)
    return frames
