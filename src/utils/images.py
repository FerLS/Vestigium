import pygame 

def extract_frames(sheet, start_x, start_y, frame_width, frame_height, num_frames, scale_factor=1, lying=None):
    """
    Extracts animation frames from a sprite sheet.

    Parameters:
    - sheet (pygame.Surface): The sprite sheet image.
    - start_x (int): X-coordinate of the starting frame in the sprite sheet.
    - start_y (int): Y-coordinate of the starting frame in the sprite sheet.
    - frame_width (int): Width of each frame.
    - frame_height (int): Height of each frame.
    - num_frames (int): Total number of frames in the animation.
    - scale_factor (float, optional): Factor to scale the frames. Default is 1.
    - lying (float, optional): Angle to rotate the frames. Default is None.

    Returns:
    - List[pygame.Surface]: A list containing the extracted animation frames.
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
