import pygame
import math
import numpy as np

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
pygame.display.set_caption("Solar System Simulation")
### Solarsystem Variablen 
AU = 149.6e6 * 1000  # Astronomical unit
G = 6.67428e-11  # Gravitational constant
SCALE = 200 / AU
### Generelle Variablen
Luftwiederstand = 0.0162        # Luftwiderstandsbeiwert                     #  - Verwendung zur Einstellung des Schubs
FallBeschleunigung = 9.81       # [m/s^2]
p_0 = 1.225 # Luftdichte auf Meereshöhe [kg/m^3]
h_s = 8400  # Skalenhöhe [m]

### Zeit-Variablen
Startzeit = 0                   # [s]                # [s]
Rechenschritte = 100000
Endzeit = Rechenschritte*5
t=np.linspace(Startzeit, Endzeit, Rechenschritte)
dt=(Endzeit-Startzeit)/Rechenschritte
TIMESTEP = 60*60*24*2
AktuellerSchritt = 0
AktuellerRechenschritt = 0

class Rocket:
    def __init__(self, startwinkel, abwurfwinkel,treibstoffmasse, koerpermasse, startplanet, radius, color):
        self.aktuellerschritt = AktuellerSchritt
        self.aktuellerrechenschritt = AktuellerRechenschritt
        self.dt = dt
        self.AbwurfWinkel = abwurfwinkel # Winkel des Starts auf der Erde [°C]
        self.KoerperMasse = koerpermasse
        self.TreibstoffMasse = treibstoffmasse
        self.startwinkel = startwinkel
        ## Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.StartKoordinatenX = startplanet.x + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
        self.StartKoordiantenZ = startplanet.y + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)
        self.r_x= np.zeros(Rechenschritte)   # x-Position [m]
        self.r_z= np.zeros(Rechenschritte)   # z-Position [m]
        self.v_x=np.zeros(Rechenschritte)    # x-Geschwindigkeit [m/s]
        self.v_z=np.zeros(Rechenschritte)    # z-Geschwindigkeit [m/s]               
        self.c = Luftwiederstand/self.KoerperMasse
        self.radius = radius
        self.z_schub = 0                     # aktuell nicht genutzt     
        self.x_schub = 0  
        self.powerchanged = False   
        self.color = color
        self.startplanet = startplanet
        self.predictions = []
        self.v_x[0] = 10e6
        self.v_z[0] = 10e6
        self.r_x[0]= self.StartKoordinatenX   
        self.r_z[0]= self.StartKoordiantenZ
        self.rocketstarted = False
    # Methode für die x-Komponente
    def f2(self, x, i:int):
        ## TO DO Gravitation für alle Planeten einbauen
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.x)**2 + (self.r_z[i] - self.startplanet.y)**2)
        x=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*x**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_x[i] - self.startplanet.x)/r0) #Extrakraft x einbauen
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
        if self.aktuellerschritt == self.aktuellerrechenschritt:
            if self.x_schub!=0:
                x += FallBeschleunigung*self.x_schub
        return x
    # Methode für die z-Komponente
    def f1(self, x,i:int):
        ## TO DO Gravitation für alle Planeten einbauen
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.x)**2 + (self.r_z[i] - self.startplanet.y)**2)
        z=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*x**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_z[i] - self.startplanet.y)/r0) #Extrakraft z einbauen
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_z - c*x**2*np.sign(x)
        if self.aktuellerschritt == self.aktuellerrechenschritt:
            if self.z_schub!=0:
                z += FallBeschleunigung*self.z_schub
        return z
    # Berechnung nach Runge-Kutta Verfahren
    def berechneNaechstenSchritt(self, i: int):
        # z-Komponente
        k1 = self.f1(self.v_z[i],i)
        k2 = self.f1(self.v_z[i] + k1*self.dt/2,i)
        k3 = self.f1(self.v_z[i] + k2*self.dt/2,i)
        k4 = self.f1(self.v_z[i] + k3*self.dt/2,i)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_z[i+1] = self.v_z[i] + k*self.dt
        self.r_z[i+1] = self.r_z[i] + self.v_z[i]*self.dt

        # x-Komponente
        k1 = self.f2(self.v_x[i],i)
        k2 = self.f2(self.v_x[i] + k1*self.dt/2,i)
        k3 = self.f2(self.v_x[i] + k2*self.dt/2,i)
        k4 = self.f2(self.v_x[i] + k3*self.dt/2,i)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_x[i+1] = self.v_x[i] + k*self.dt
        self.r_x[i+1] = self.r_x[i] + self.v_x[i]*self.dt
    def update_scale(self,scale):
        self.radius *= scale
    def draw(self, window, move_x, move_y, planets, paused):
        if self.rocketstarted:
            if not paused:
                if self.powerchanged or self.aktuellerschritt==0:
                    self.aktuellerrechenschritt = self.aktuellerschritt
                    for i in range(1000):
                        self.berechneNaechstenSchritt(self.aktuellerrechenschritt)
                        self.aktuellerrechenschritt += 1
                    self.powerchanged = False
                else:
                    self.berechneNaechstenSchritt(self.aktuellerrechenschritt)
                    self.aktuellerrechenschritt += 1
            # move_x and move_y verschieben je nach bewegung des Bildschirm
            pygame.draw.lines(window, self.color, False, np.array((self.r_x[self.aktuellerschritt:self.aktuellerrechenschritt]*SCALE+move_x+WIDTH/2, self.r_z[self.aktuellerschritt:self.aktuellerrechenschritt]*SCALE+move_y+ HEIGHT/2)).T, 1)
            pygame.draw.circle(window,self.color,(self.r_x[self.aktuellerschritt]*SCALE+move_x+WIDTH/2 , self.r_z[self.aktuellerschritt]*SCALE+move_y+HEIGHT/2),self.radius)
            if not paused:
                self.aktuellerschritt+= 1
        else:
            startplanet = next(filter(lambda x: x.name == self.startplanet.name, planets),None)
            pygame.draw.circle(window,self.color,(startplanet.x + startplanet.radius * np.sin(self.startwinkel * np.pi / 180) *SCALE+move_x+WIDTH/2 , startplanet.y + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)*SCALE+move_y+HEIGHT/2),self.radius)
            self.StartKoordinatenX = startplanet.x + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
            self.StartKoordiantenZ = startplanet.y + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)
            self.r_x[0]= self.StartKoordinatenX   
            self.r_z[0]= self.StartKoordiantenZ
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
    def drawlineonly(self, window,move_x, move_y, draw_line):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1) 
    def draw(self, window, show, move_x, move_y, draw_line):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)   
        
        if self.radius * SCALE> 2:
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius * SCALE)
        else:
            pygame.draw.circle(window, self.color, (x + move_x, y + move_y), 2)
        #pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius
        distance_text = FONT_2.render(self.name+ ": "+str(round(self.distance_to_rocket * 1.057 * 10 ** -16, 8))+ "light years", True,
                                          COLOR_WHITE)
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


def main():
    global SCALE
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    move_x = 0
    move_y = 0
    draw_line = True

    # Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30,"Sonne")
    sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23,"Merkur")
    mercury.y_vel = 47.4 * 1000

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24,"Venus")
    venus.y_vel = 35.02 * 1000

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24,"Erde")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 3394  * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23,"Mars")
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27,"Jupiter")
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.573 * AU, 0, 60268  * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26,"Saturn")
    saturn.y_vel = 9.68 * 1000

    uranus = Planet(-19.165 * AU, 0, 25559  * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25,"Uranus")
    uranus.y_vel = 6.80 * 1000

    neptune = Planet(-30.178 * AU, 0, 24764  * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26,"Neptun")
    neptune.y_vel = 5.43 * 1000


    planets = [neptune, uranus, saturn, jupiter, mars, earth, venus, mercury, sun]
    

    rocket = Rocket(45,0,0,10000,earth,5,(255,255,255))
    while run:
        clock.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            # Raketenboost Oben
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and rocket.z_schub<10:
                rocket.z_schub += 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Links   
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and rocket.x_schub>-10:
                rocket.x_schub -= 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Unten
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and rocket.z_schub>-10:
                rocket.z_schub -= 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Rechts
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and rocket.x_schub<10:
                rocket.x_schub += 1
                rocket.powerchanged = True
                rocket.rocketstarted = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                show_distance = not show_distance
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                move_x, move_y = -sun.x * SCALE, -sun.y * SCALE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                move_x, move_y = -rocket.r_x[rocket.aktuellerschritt] * SCALE, -rocket.r_z[rocket.aktuellerschritt] * SCALE    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                mouseX, mouseY = pygame.mouse.get_pos()
                move_x-=(mouse_x-WIDTH/2)/2
                move_y-=(mouse_y-HEIGHT/2)/2
                SCALE *= 0.75
                rocket.update_scale(0.75)
                for planet in planets:
                    planet.update_scale(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                mouseX, mouseY = pygame.mouse.get_pos()
                move_x-=(mouse_x-WIDTH/2)/2
                move_y-=(mouse_y-HEIGHT/2)/2
                SCALE *= 1.25
                rocket.update_scale(1.25)
                for planet in planets:
                    planet.update_scale(1.25)

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 10
        if keys[pygame.K_LEFT] or mouse_x == 0:
            move_x += distance
        if keys[pygame.K_RIGHT] or mouse_x == window_w - 1:
            move_x -= distance
        if keys[pygame.K_UP] or mouse_y == 0:
            move_y += distance
        if keys[pygame.K_DOWN] or mouse_y == window_h - 1:
            move_y -= distance
        
        ### Rocket           
        for planet in planets:
            if not pause:
                planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen
            if not (planet.y*SCALE+planet.radius*SCALE < -move_y-HEIGHT/2 or planet.y*SCALE-planet.radius*SCALE > -move_y+HEIGHT/2 or planet.x*SCALE+planet.radius*SCALE < -move_x-WIDTH/2 or planet.x*SCALE-planet.radius*SCALE > -move_x+WIDTH/2):
                if show_distance :
                    planet.draw(WINDOW, 1, move_x, move_y, draw_line)
                else:
                    planet.draw(WINDOW, 0, move_x, move_y, draw_line)
            else: 
                planet.drawlineonly(WINDOW, move_x, move_y, draw_line)
        rocket.draw(WINDOW,move_x,move_y, planets, pause)
        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (15, 15))
        text_surface = FONT_1.render("Press X or ESC to exit", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 45))
        text_surface = FONT_1.render("Press P to turn on/off distance", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 75))
        text_surface = FONT_1.render("Press U to turn on/off drawing orbit lines", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 105))
        text_surface = FONT_1.render("Use mouse or arrow keys to move around", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 135))
        text_surface = FONT_1.render("Press C to center to the Sun or B to Center to the rocket", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 165))
        text_surface = FONT_1.render("Press Space to pause/unpause", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 195))
        text_surface = FONT_1.render("Use scroll-wheel to zoom", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 225))
        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 285))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 315))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 345))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 375))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 405))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 435))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 465))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 495))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 525))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()