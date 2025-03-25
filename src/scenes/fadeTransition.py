import pygame

class FadeTransition:
    def __init__(self, screen, duration=1.0, on_complete=None):
        self.screen = screen
        self.duration = duration
        self.on_complete = on_complete
        self.active = False
        self.timer = 0
        self.overlay = pygame.Surface(screen.get_size()).convert()
        self.overlay.fill((0, 0, 0))
        self.alpha = 0

    def start(self):
        self.active = True
        self.timer = 0

    def update(self, dt):
        raise NotImplementedError("Implement this in FadeIn or FadeOut")

    def draw(self):
        if self.active:
            self.overlay.set_alpha(self.alpha)
            self.screen.blit(self.overlay, (0, 0))



class FadeOut(FadeTransition):
    def __init__(self, screen, duration=2.5, on_complete=None):
        super().__init__(screen, duration, on_complete)
        self.alpha = 0

    def update(self, dt):
        if not self.active:
            return

        self.timer += dt
        progress = min(self.timer / self.duration, 1.0)
        self.alpha = int(progress * 255)

        if progress >= 1.0:
            self.active = False
            if self.on_complete:
                self.on_complete()

class FadeIn(FadeTransition):
    def __init__(self, screen, duration=1.0, on_complete=None):
        super().__init__(screen, duration, on_complete)
        self.alpha = 255 

    def update(self, dt):
        if not self.active:
            return

        self.timer += dt
        progress = min(self.timer / self.duration, 1.0)
        self.alpha = int((1 - progress) * 255)

        if progress >= 1.0:
            self.active = False
            if self.on_complete:
                self.on_complete()