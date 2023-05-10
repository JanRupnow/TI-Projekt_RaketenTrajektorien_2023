import numpy as np
from konstanten import *
import pygame
import math
class Rocket:
    def __init__(self, startwinkel, abwurfwinkel,treibstoffmasse, koerpermasse, startplanet, radius, color):
        self.aktuellerschritt = AktuellerSchritt
        self.aktuellerrechenschritt = AktuellerRechenschritt
        self.timestep = TIMESTEP
        self.timestepChanged = False
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
        self.thrust = 0                     # aktuell nicht genutzt     
        self.angle = 0  
        self.powerchanged = False   
        self.color = color
        self.startplanet = startplanet
        self.predictions = []
        self.v_x[0] = 10e3
        self.v_z[0] = 10e3
        self.r_x[0]= self.StartKoordinatenX   
        self.r_z[0]= self.StartKoordiantenZ
        self.rocketstarted = False
    # Methode für die x-Komponente
    def f2(self, x, i:int):
        ## TO DO Gravitation für alle Planeten einbauen
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.x)**2 + (self.r_z[i] - self.startplanet.y)**2)
        x=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*x**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_x[i] - self.startplanet.x)/r0) #Extrakraft x einbauen
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
        #if self.aktuellerschritt == self.aktuellerrechenschritt:
            #if self.x_schub!=0:
        if self.thrust != 0:
            x += FallBeschleunigung*math.cos(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust
        return x
    # Methode für die z-Komponente
    def f1(self, x,i:int):
        ## TO DO Gravitation für alle Planeten einbauen
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.x)**2 + (self.r_z[i] - self.startplanet.y)**2)
        z=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*x**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_z[i] - self.startplanet.y)/r0) #Extrakraft z einbauen
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_z - c*x**2*np.sign(x)

        if self.thrust != 0:
            z += FallBeschleunigung*math.sin(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust
        return z
    # Berechnung nach Runge-Kutta Verfahren
    def berechneNaechstenSchritt(self, i: int):
        # z-Komponente
        k1 = self.f1(self.v_z[i],i)
        k2 = self.f1(self.v_z[i] + k1*self.timestep/2,i)
        k3 = self.f1(self.v_z[i] + k2*self.timestep/2,i)
        k4 = self.f1(self.v_z[i] + k3*self.timestep/2,i)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_z[i+1] = self.v_z[i] + k*self.timestep
        self.r_z[i+1] = self.r_z[i] + self.v_z[i]*self.timestep

        # x-Komponente
        k1 = self.f2(self.v_x[i],i)
        k2 = self.f2(self.v_x[i] + k1*self.timestep/2,i)
        k3 = self.f2(self.v_x[i] + k2*self.timestep/2,i)
        k4 = self.f2(self.v_x[i] + k3*self.timestep/2,i)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_x[i+1] = self.v_x[i] + k*self.timestep
        self.r_x[i+1] = self.r_x[i] + self.v_x[i]*self.timestep
    def update_scale(self,scale):
        self.radius *= scale
    def draw(self, window, move_x, move_y, planets, paused, scale, width, height):
        if self.rocketstarted:
            if not paused:
                if self.powerchanged or self.aktuellerschritt==0 or self.timestepChanged:
                    self.aktuellerrechenschritt = self.aktuellerschritt
                    for i in range(1000):
                        self.berechneNaechstenSchritt(self.aktuellerrechenschritt)
                        self.aktuellerrechenschritt += 1
                    self.powerchanged = False
                    self.timestepChanged = False
                else:
                    self.berechneNaechstenSchritt(self.aktuellerrechenschritt)
                    self.aktuellerrechenschritt += 1
            # move_x and move_y verschieben je nach bewegung des Bildschirm
            if self.aktuellerrechenschritt > 2:
                pygame.draw.lines(window, self.color, False, np.array((self.r_x[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_y+ height/2)).T, 1)
                pygame.draw.circle(window,self.color,(self.r_x[self.aktuellerschritt]*scale+move_x+width/2 , self.r_z[self.aktuellerschritt]*scale+move_y+height/2),self.radius)
            if not paused:
                self.aktuellerschritt+= 1
        else:
            startplanet = next(filter(lambda x: x.name == self.startplanet.name, planets),None)
            pygame.draw.circle(window,self.color,(startplanet.x + startplanet.radius * np.sin(self.startwinkel * np.pi / 180) *scale+move_x+width/2 , startplanet.y + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)*scale+move_y+height/2),self.radius)
            self.StartKoordinatenX = startplanet.x + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
            self.StartKoordiantenZ = startplanet.y + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)
            self.r_x[0]= self.StartKoordinatenX   
            self.r_z[0]= self.StartKoordiantenZ
            
    # in m/s
    def getAbsoluteVelocity(self):
        if self.rocketstarted:
            return np.sqrt(self.v_x[self.aktuellerschritt]**2 + self.v_z[self.aktuellerschritt]**2)
        else:
            return 0
