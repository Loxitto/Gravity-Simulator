import pygame
import sys
import random
import math
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
pygame.display.set_caption('Gravity Simulator')

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

class Planet:
    def __init__(self, x, y, radius, mass, vx=0, vy=0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.vx = vx
        self.vy = vy

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius)

    def update(self, planets, dt, screen_width, screen_height):
        fx = fy = 0
        for planet in planets:
            if planet != self:
                dx = planet.x - self.x
                dy = planet.y - self.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if self.collide(planet):
                    if planet.mass > self.mass:
                        self, planet = planet, self
                    self.mass += planet.mass
                    self.radius = (self.radius ** 3 + planet.radius ** 3) ** (1/3)
                    planets.remove(planet)
                else:
                    force = 6.674e-11 * self.mass * planet.mass / dist ** 2
                    fx += force * dx / dist
                    fy += force * dy / dist

        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x > screen_width:
            self.x -= screen_width

        if self.x < 0:
            self.x += screen_width

        if self.y > screen_height:
            self.y -= screen_height

        if self.y < 0:
            self.y += screen_height

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        return dist < self.radius + other.radius

planets = []
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                radius = random.randint(5, 15)
                mass = radius ** 13
                vx = random.uniform(-30, 30)
                vy = random.uniform(-30, 30)
                planet = Planet(x, y, radius, mass, vx, vy)
                planets.append(planet)
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                for planet in planets:
                    planet_rect = pygame.Rect(planet.x - planet.radius, planet.y - planet.radius, planet.radius * 2, planet.radius * 2)
                    if planet_rect.collidepoint(mouse_pos):
                        planets.remove(planet)
                        break
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            for planet in planets:
                planet_rect = pygame.Rect(planet.x - planet.radius, planet.y - planet.radius, planet.radius * 2, planet.radius * 2)
                if planet_rect.collidepoint(mouse_pos):
                    if event.y > 0:
                        planet.radius = planet.radius + 1 if planet.radius <= 150 else planet.radius
                        planet.mass += planet.mass // 13
                    elif event.y < 0:
                        planet.radius = planet.radius - 1 if planet.radius >= 5 else planet.radius
                        planet.mass -= planet.mass // 13
                    break
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                planets.clear()

    screen.fill(WHITE)
    dt = clock.tick(60) / 1000.0

    for planet in planets:
        planet.update(planets, dt, screen_width, screen_height)

    for planet in planets:
        planet.draw(screen)

    pygame.display.update()