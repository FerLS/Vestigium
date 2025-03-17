class Camera:
    def __init__(self, screen_width, screen_height):
        self.scroll_x = 0
        self.scroll_y = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.margin_x = screen_width // 4
        self.margin_y = screen_height // 4

    def update(self, player_rect):
        # Horizontal
        if player_rect.left < self.scroll_x + self.margin_x:
            self.scroll_x = player_rect.left - self.margin_x

        elif player_rect.right > self.scroll_x + self.screen_width - self.margin_x:
            self.scroll_x = player_rect.right - (self.screen_width - self.margin_x)

        # Vertical
        if player_rect.top < self.scroll_y + self.margin_y:
            self.scroll_y = player_rect.top - self.margin_y

        elif player_rect.bottom > self.scroll_y + self.screen_height - self.margin_y:
            self.scroll_y = player_rect.bottom - (self.screen_height - self.margin_y)

    def get_offset(self):
        return int(self.scroll_x), int(self.scroll_y)
