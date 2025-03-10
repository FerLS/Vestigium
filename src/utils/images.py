import pygame 
def extract_frames(sheet, start_x, start_y, frame_width, frame_height, num_frames, scale_factor):
    """
    Extracts animation frames from a sprite sheet.

    Parameters:
    - sheet (pygame.Surface): The sprite sheet image.
    - start_x (int): X-coordinate of the starting frame in the sprite sheet.
    - start_y (int): Y-coordinate of the starting frame in the sprite sheet.
    - frame_width (int): Width of each frame.
    - frame_height (int): Height of each frame.
    - num_frames (int): Total number of frames in the animation.
    - scale_factor (float): Factor to scale the frames.


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

        frames.append(frame)
    return frames

"""import pygame
import time

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300  # Adjust as needed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frame Debugger")

# Load the sprite sheet
sprite_sheet = pygame.image.load("assets\\images\\player_spritesheet.png").convert_alpha()

# Extract frames using your function
walk_frames = extract_frames(
    sheet=sprite_sheet,  
    start_x=0,           
    start_y=96,         
    frame_width=32,      
    frame_height=32,     
    num_frames=8,
    scale_factor=2       
)

# Show each frame for debugging
running = True
frame_index = 0
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(walk_frames[frame_index], (100, 100))  # Draw frame at position (100,100)
    
    # Draw the rect of the current frame
    frame_rect = walk_frames[frame_index].get_rect(topleft=(100, 100))
    pygame.draw.rect(screen, (255, 0, 0), frame_rect, 2)  # Red rectangle with 2px border
    
    pygame.display.flip()  # Update screen
    
    print(f"Displaying frame {frame_index}")  # Debugging: print frame index
    print(f"Frame rect: {frame_rect}")  # Print the rect of the current frame

    time.sleep(0.5)  # Wait 0.5 seconds to see the frame change
    frame_index = (frame_index + 1) % len(walk_frames)  # Cycle through frames

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()"""
