import numpy as np
from variables.konstanten import *
import pygame
import math
import sys
import os



class Rocket:
    def __init__(self, startwinkel, abwurfwinkel,treibstoffmasse, koerpermasse, startplanet, radius, color, sun, img0):
        self.aktuellerschritt = AktuellerSchritt
        self.aktuellerrechenschritt = AktuellerRechenschritt
        self.timestep = timestep
        self.timestepChanged = False
        self.AbwurfWinkel = abwurfwinkel # Winkel des Starts auf der Erde [°C]
        self.KoerperMasse = koerpermasse
        self.TreibstoffMasse = treibstoffmasse
        self.startwinkel = startwinkel
        ## Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.StartKoordinatenX = startplanet.r_x[self.aktuellerschritt] + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
        self.StartKoordiantenZ = startplanet.r_z[self.aktuellerschritt] + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)
        self.r_x= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # x-Position [m]
        self.r_z= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # z-Position [m]
        self.v_x=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # x-Geschwindigkeit [m/s]
        self.v_z=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # z-Geschwindigkeit [m/s]               
        self.c = Luftwiederstand/self.KoerperMasse
        self.radius = radius
        self.thrust = 0                     # aktuell nicht genutzt     
        self.angle = 0  
        self.powerchanged = False   
        self.color = color
        self.startplanet = startplanet
        self.predictions = []
        self.v_x[0] = self.startplanet.v_x[0]
        self.v_z[0] = self.startplanet.v_z[0]
        self.r_x[0]= self.StartKoordinatenX   
        self.r_z[0]= self.StartKoordiantenZ
        self.rocketstarted = False
        self.img = img0
        self.img0 = img0
        self.notRotatedImg = pygame.transform.scale_by(img0, min(0.1*self.radius, 1))
        self.zoomOnRocket = False
        self.sun = sun
        #self.imgage = img0
    # Methode für die x-Komponente
    def f2(self, x, i:int):

        #for planet in planets:
         #   if planet.distance_to_rocket < 100*plaen
        ## TO DO Gravitation für alle Planeten einbauen
        distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.r_x[i])**2 + (self.r_z[i] - self.startplanet.r_z[i])**2)
        x=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*self.getRelativeVelocity(i)**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_x[i] - self.startplanet.r_x[i])/r0) #Extrakraft x einbauen
        x -= (G*self.sun.mass/distanceToSun**2)* ((self.r_x[i] - self.sun.r_x[i])/distanceToSun)
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
        #if self.aktuellerschritt == self.aktuellerrechenschritt:
            #if self.x_schub!=0:
        if self.thrust != 0:
            x += math.cos(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust
        return x
    # Methode für die z-Komponente
    def f1(self, x,i:int):
        ## TO DO Gravitation für alle Planeten einbauen
        distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        r0 = np.sqrt( (self.r_x[i] - self.startplanet.r_x[i])**2 + (self.r_z[i] - self.startplanet.r_z[i])**2)
        z=( -(G*self.startplanet.mass/r0**2) - (Luftwiederstand*self.getRelativeVelocity(i)**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.startplanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_z[i] - self.startplanet.r_z[i])/r0) #Extrakraft z einbauen
        z -= (G*self.sun.mass/distanceToSun**2)* ((self.r_z[i] - self.sun.r_z[i])/distanceToSun)
        # TODO muss die Geschwindigkeit relativ zum Planet sein? Eigentlich ja oder?

        if self.thrust != 0:
            z += math.sin(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust
        return z
    # Berechnung nach Runge-Kutta Verfahren
    def berechneNaechstenSchritt(self, i: int, planets):
        
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
        if self.radius > MIN_ROCKET_RADIUS:
            self.notRotatedImg = pygame.transform.scale_by(self.img0, max(min(0.1*self.radius, 1), 0.1))
    def draw(self, window, move_x, move_y, planets, paused, scale, width, height):
        global img0
        if self.rocketstarted:
            if not paused:
                if self.powerchanged or self.aktuellerschritt==0 or self.timestepChanged:
                    firstTime = self.aktuellerrechenschritt == 0
                    self.aktuellerrechenschritt = self.aktuellerschritt
                    self.calculateNewCalculationOfPredictions(firstTime, planets, paused)
                    if not (firstTime or self.timestepChanged):
                        for planet in planets:
                            planet.predictNext(self.aktuellerrechenschritt-1, planets, paused)

                    self.powerchanged = False
                    self.timestepChanged = False

                else:
                    self.calculateOnePrediction(planets, paused)
            # move_x and move_y verschieben je nach bewegung des Bildschirm
            if self.aktuellerrechenschritt > 2:
                pygame.draw.lines(window, self.color, False, np.array((self.r_x[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_y+ height/2)).T, 1)
                #pygame.draw.circle(window,self.color,(self.r_x[self.aktuellerschritt]*scale+move_x+width/2 , self.r_z[self.aktuellerschritt]*scale+move_y+height/2),self.radius)
                
                if self.radius >= MIN_ROCKET_RADIUS:
                    self.img = pygame.transform.rotate(self.notRotatedImg, math.atan2(self.v_z[self.aktuellerschritt], self.v_x[self.aktuellerschritt]) * (-180) /np.pi - 90)
                    #img = pygame.transform.rotozoom(img0, math.atan2(self.v_z[self.aktuellerschritt], self.v_x[self.aktuellerschritt]), max(0.05, self.radius))
                    window.blit(self.img, (self.r_x[self.aktuellerschritt]*scale+move_x+width/2 -self.img.get_width()/2 , self.r_z[self.aktuellerschritt]*scale+move_y+height/2 - self.img.get_height()/2))
                else:
                    pygame.draw.circle(window, self.color, (self.r_x[self.aktuellerschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt]*scale+move_y+height/2), MIN_ROCKET_RADIUS)
            if not paused:
                self.aktuellerschritt += 1
                for planet in planets:
                    planet.aktuellerschritt += 1

                if self.aktuellerschritt >= (NUM_OF_PREDICTIONS):
                    self.resetArray()
                    for planet in planets:
                        planet.resetArray()
        else:
            startplanet = next(filter(lambda x: x.name == self.startplanet.name, planets),None)
            self.drawAndValueBeforeStarting(startplanet, window, scale, width, height, move_x, move_y)
            
    def getRelativeVelocity(self, i):
        if self.rocketstarted:
            return np.sqrt( (self.v_x[i] - self.startplanet.v_x[i])**2 
                            + (self.v_z[i] - self.startplanet.v_z[i])**2)
        else:
            return 0
        
    def getCurrentRelativeVelocity(self):
        if self.rocketstarted:
            return np.sqrt( (self.v_x[self.aktuellerschritt] - self.startplanet.v_x[self.aktuellerschritt])**2 
                            + (self.v_z[self.aktuellerschritt] - self.startplanet.v_z[self.aktuellerschritt])**2)
        else:
            return 0

    # in m/s
    def getAbsoluteVelocity(self):
        if self.rocketstarted:
            return np.sqrt(self.v_x[self.aktuellerschritt]**2 + self.v_z[self.aktuellerschritt]**2)
        else:
            return 0
    def resetArray(self):
        self.r_x[1:NUM_OF_PREDICTIONS+1] = self.r_x[NUM_OF_PREDICTIONS:]
        self.r_z[1:NUM_OF_PREDICTIONS+1] = self.r_z[NUM_OF_PREDICTIONS:]
        self.v_x[1:NUM_OF_PREDICTIONS+1] = self.v_x[NUM_OF_PREDICTIONS:]
        self.v_z[1:NUM_OF_PREDICTIONS+1] = self.v_z[NUM_OF_PREDICTIONS:]
        self.aktuellerschritt = 1
        self.aktuellerrechenschritt = NUM_OF_PREDICTIONS

    def drawAndValueBeforeStarting(self, startplanet,window, scale, width, height, move_x, move_y):
            pygame.draw.circle(window,self.color,(startplanet.r_x[self.aktuellerschritt] + startplanet.radius * np.sin(self.startwinkel * np.pi / 180) *scale+move_x+width/2 , startplanet.r_z[self.aktuellerschritt] + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)*scale+move_y+height/2),self.radius)
            self.StartKoordinatenX = startplanet.r_x[self.aktuellerschritt] + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
            self.StartKoordiantenZ = startplanet.r_z[self.aktuellerschritt] + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)
            self.r_x[0] = self.StartKoordinatenX   
            self.r_z[0] = self.StartKoordiantenZ
            self.v_x[0] = startplanet.v_x[startplanet.aktuellerschritt]
            self.v_z[0] = startplanet.v_z[startplanet.aktuellerschritt]
    def calculateNewCalculationOfPredictions(self, firstTime, planets, paused):
        for i in range(NUM_OF_PREDICTIONS):
            if firstTime or self.timestepChanged:
                for planet in planets:
                    planet.predictNext(self.aktuellerrechenschritt, planets, paused)
            self.berechneNaechstenSchritt(self.aktuellerrechenschritt, planets)
            self.aktuellerrechenschritt += 1
    def calculateOnePrediction(self, planets, paused):
        for planet in planets:
            planet.predictNext(self.aktuellerrechenschritt, planets, paused)
        self.berechneNaechstenSchritt(self.aktuellerrechenschritt, planets)
        self.aktuellerrechenschritt += 1
