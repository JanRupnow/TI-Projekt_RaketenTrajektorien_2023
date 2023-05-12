import math
import pygame
from konstanten import *

class Planet:
    def __init__(self, x, y, radius, color, mass,name):
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.x_vel = 0
        self.y_vel = 0
        self.name = name
        self.timestep = TIMESTEP

        self.r_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.r_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.aktuellerschritt = 0
        self.aktuellerrechenschritt = 0

        self.r_x[0] = x
        self.r_z[0] = y
    """"
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
    """
    def drawlineonly(self, window,move_x, move_y, draw_line,scale, width, height, pause):
        if draw_line:
            pygame.draw.lines(window, self.color, False, np.array((self.r_x[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_y+ height/2)).T, 1)
        
        if not pause:
            self.aktuellerschritt += 1 #fixen
    """
    def draw(self, window, show, move_x, move_y, draw_line, scale, width, height):
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
        
        pygame.draw.circle(window, self.color, (x + move_x, y + move_y), max(self.radius * scale, 2))

        #pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius
        if show:
            distance_to_rocket = np.sqrt(self.r_x[self.aktuellerschritt]**2 + self.r_z[self.aktuellerschritt]**2)
            distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(self.name+ ": "+str(round(distance_to_rocket * 1.057 * 10 ** -16, 8))+ "light years", True,
                                          (255,255,255))
            window.blit(distance_text, (x - distance_text.get_width() / 2 + move_x,
                                            y - distance_text.get_height() / 2 - 20 + move_y))
    """
    def draw(self, window, show, move_x, move_y, draw_line, scale, width, height, pause):
        self.drawlineonly(window, move_x, move_y, draw_line, scale, width, height, True)
        pygame.draw.circle(window, self.color, (self.r_x[self.aktuellerschritt], self.r_z[self.aktuellerschritt]), max(self.radius * scale, 2))

        if show:
            distance_to_rocket = np.sqrt(self.r_x[self.aktuellerschritt]**2 + self.r_z[self.aktuellerschritt]**2)
            distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(self.name+ ": "+str(round(distance_to_rocket * 1.057 * 10 ** -16, 8))+ "light years", True,
                                          (255,255,255))
            window.blit(distance_text, (self.r_x[self.aktuellerschritt] - distance_text.get_width() / 2 + move_x,
                                        self.r_z[self.aktuellerschritt] - distance_text.get_height() / 2 - 20 + move_y))
        
        if not pause:
            self.aktuellerschritt += 1 #fixen

    def attraction(self, other, i):
        other_x, other_y = other.r_x[i], other.r_z[i]
        distance_x = other_x - self.r_x[i]
        distance_y = other_y - self.r_z[i]
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    """"
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
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
        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep
        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep
        self.orbit.append((self.x, self.y))
    """
    def resetArray(self):
        self.r_x[1:NUM_OF_PREDICTIONS+1] = self.r_x[NUM_OF_PREDICTIONS:]
        self.r_z[1:NUM_OF_PREDICTIONS+1] = self.r_z[NUM_OF_PREDICTIONS:]
        self.v_x[1:NUM_OF_PREDICTIONS+1] = self.v_x[NUM_OF_PREDICTIONS:]
        self.v_z[1:NUM_OF_PREDICTIONS+1] = self.v_z[NUM_OF_PREDICTIONS:]
        self.aktuellerschritt = 1
        self.aktuellerrechenschritt = NUM_OF_PREDICTIONS

    def update_scale(self, scale):
        self.radius *= scale

    def predictNext(self, i, planets):
        self.aktuellerrechenschritt = i

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet, i)
            total_fx += fx
            total_fy += fy
        self.v_x[i+1] = self.v_x[i] + total_fx / self.mass * self.timestep
        self.v_z[i+1] = self.v_z[i] + total_fy / self.mass * self.timestep
        self.r_x[i+1] = self.r_x[i] + self.v_x[i+1] * self.timestep
        self.r_z[i+1] = self.r_z[i] + self.v_z[i+1] * self.timestep

        self.aktuellerrechenschritt += 1