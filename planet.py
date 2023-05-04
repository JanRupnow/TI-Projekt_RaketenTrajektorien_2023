import math
import pygame
from konstanten import *

class Planet:
    def __init__(self, x, y, radius, color, mass,name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.name = name
    def drawlineonly(self, window,move_x, move_y, draw_line,scale, width, height):
        x = self.x * scale + width / 2
        y = self.y * scale + height / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * scale + width / 2
                y = y * scale + height / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1) 
    def draw(self, window, show, move_x, move_y, draw_line,scale, width, height):
        x = self.x * scale + width / 2
        y = self.y * scale + height / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * scale + width / 2
                y = y * scale + height / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)   
        
        if self.radius * scale> 2:
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius * scale)
        else:
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), 2)
        #pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius
        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(self.name+ ": "+str(round(self.distance_to_rocket * 1.057 * 10 ** -16, 8))+ "light years", True,
                                          (255,255,255))
        if show:
            window.blit(distance_text, (x - distance_text.get_width() / 2 + move_x,
                                            y - distance_text.get_height() / 2 - 20 + move_y))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets, rocket):
        self.distance_to_rocket = math.sqrt((self.x-rocket.r_x[rocket.aktuellerschritt])**2+(self.y-rocket.r_z[rocket.aktuellerschritt])**2)
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        self.radius *= scale