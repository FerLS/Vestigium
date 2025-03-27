class Camera:
    def __init__(self, screen_width, screen_height):
        self.scroll_x = 0
        self.scroll_y = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.left_margin = screen_width // 4         
        self.right_margin = screen_width // 4  

        self.margin_y = screen_height // 4

    def update(self, target_rect):
        # Horizontal
        if target_rect.left < self.scroll_x + self.left_margin:
            self.scroll_x = target_rect.left - self.left_margin

        elif target_rect.right > self.scroll_x + self.screen_width - self.right_margin:
            self.scroll_x = target_rect.right - (self.screen_width - self.right_margin)

        # Vertical (igual que antes)
        if target_rect.top < self.scroll_y + self.margin_y:
            self.scroll_y = target_rect.top - self.margin_y

        elif target_rect.bottom > self.scroll_y + self.screen_height - self.margin_y:
            self.scroll_y = target_rect.bottom - (self.screen_height - self.margin_y)

    def get_offset(self):
        return int(self.scroll_x), int(self.scroll_y)
    
    def get_horizontal_bounds(self):
        """Returns the left and right bounds of the camera"""
        return self.scroll_x, self.scroll_x + self.screen_width
    
    def update_x_margin(self, new_left_margin, new_right_margin):
        self.left_margin = new_left_margin
        self.right_margin = new_right_margin
