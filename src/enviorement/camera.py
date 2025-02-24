class Camera:
    def __init__(self, left_limit, right_limit):
        self.left_limit = left_limit   
        self.right_limit = right_limit
        self.scroll = 0              

    def update(self, player_rect):
        if player_rect.left < self.left_limit:
            self.scroll = player_rect.left - self.left_limit
        elif player_rect.right > self.right_limit:
            self.scroll = player_rect.right - self.right_limit
        else:
            self.scroll = 0

