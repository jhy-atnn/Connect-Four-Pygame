import pygame
import random
import time


class ConfettiParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(3, 7)
        self.color = [random.randint(0, 255) for _ in range(3)]
        self.speed_y = random.uniform(2, 6)
        self.speed_x = random.uniform(-2, 2)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def handle_win(screen, bg):
    """Display confetti animation on the screen."""
    show_confetti(screen, bg, duration=2)


def show_confetti(screen, bg, duration=2):
    screen_width, screen_height = screen.get_size()
    particles = [ConfettiParticle(random.randint(0, screen_width), random.randint(-100, 0)) for _ in range(120)]
    start_time = time.time()
    clock = pygame.time.Clock()
    while time.time() - start_time < duration:
        screen.blit(bg, (0, 0))
        for p in particles:
            p.update()
            p.draw(screen)
        pygame.display.update()
        clock.tick(100)
