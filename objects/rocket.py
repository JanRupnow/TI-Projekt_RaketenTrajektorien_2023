import numpy as np
from variables.konstanten import *
import pygame
import math
import datetime



class Rocket:
    def __init__(self, startwinkel,treibstoffmasse, koerpermasse, startplanet, radius, color, sun, img0):
        self.aktuellerschritt = AktuellerSchritt
        self.aktuellerrechenschritt = AktuellerRechenschritt
        self.timestep = timestep
        self.timestepChanged = False
        self.KoerperMasse = koerpermasse
        self.TreibstoffMasse = treibstoffmasse
        self.startwinkel = startwinkel
        self.r_x= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # x-Position [m]
        self.r_z= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # z-Position [m]
        self.v_x=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # x-Geschwindigkeit [m/s]
        self.v_z=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # z-Geschwindigkeit [m/s]               
        self.c = Luftwiederstand/self.KoerperMasse
        self.radius = radius
        self.thrust = 0                     # aktuell nicht genutzt     
        self.angle = 0  
        self.landed = False
        self.powerchanged = False
        self.rocketstarted = False 
        self.landed = False  
        self.color = color
        self.startplanet = startplanet
        self.predictions = []
        self.v_x[0] = self.startplanet.v_x[0]
        self.v_z[0] = self.startplanet.v_z[0]
        ## Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.r_x[0]= startplanet.r_x[self.aktuellerschritt] + startplanet.radius * np.cos(self.startwinkel * np.pi / 180)  
        self.r_z[0]= startplanet.r_z[self.aktuellerschritt] + startplanet.radius * np.sin(self.startwinkel * np.pi / 180)
        self.img = img0
        self.img0 = img0
        self.notRotatedImg = pygame.transform.scale_by(img0, min(0.1*self.radius, 1))
        self.zoomOnRocket = False
        self.sun = sun
        self.entryAngle = 0
        self.nextPlanet = self.startplanet
        self.planetNearEnough = True
        self.nearestPlanet = self.startplanet
        #self.imgage = img0
    # Methode für die x-Komponente
    def f2(self, v, i:int):
        x = 0
        if self.planetNearEnough:
            r0 = np.sqrt( (self.r_x[i] - self.nearestPlanet.r_x[i])**2 + (self.r_z[i] - self.nearestPlanet.r_z[i])**2)
            x = ( -(G*self.nearestPlanet.mass/r0**2) - (Luftwiederstand*self.getRelativeVelocity(i)**2*np.sign(self.v_x[i]) * p_0 * np.exp(-abs((r0-self.nearestPlanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_x[i] - self.nearestPlanet.r_x[i])/r0) #Extrakraft x einbauen

        distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        x -= (G*self.sun.mass/distanceToSun**2)* ((self.r_x[i] - self.sun.r_x[i])/distanceToSun)
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
        if self.thrust != 0:
            x += math.cos(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust*10
        return x
    # Methode für die z-Komponente
    def f1(self, v,i:int):
        z = 0       
        if self.planetNearEnough:
            r0 = np.sqrt( (self.r_x[i] - self.nearestPlanet.r_x[i])**2 + (self.r_z[i] - self.nearestPlanet.r_z[i])**2)
            z = ( -(G*self.nearestPlanet.mass/r0**2) - (Luftwiederstand*self.getRelativeVelocity(i)**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r0-self.nearestPlanet.radius)) / h_s))/(2 * self.KoerperMasse) ) * ((self.r_z[i] - self.nearestPlanet.r_z[i])/r0)

        distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        z -= (G*self.sun.mass/distanceToSun**2)* ((self.r_z[i] - self.sun.r_z[i])/distanceToSun)
        # TODO muss die Geschwindigkeit relativ zum Planet sein? Eigentlich ja oder? (Luftwiderstand) (wie kann man das besser machen? planetenabhängig?)

        if self.thrust != 0:
            z += math.sin(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust*10
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

        self.updateNextPlanet(planets)

    def updateNextPlanet(self, planets):
        if self.planetNearEnough and not self.isPlanetNearEnough(self.nearestPlanet):
            self.planetNearEnough = False
        elif self.planetNearEnough == False:
            for planet in planets:
                if self.isPlanetNearEnough(planet):
                    self.planetNearEnough = True
                    self.nearestPlanet = planet

        print(f"nearest planet: {self.nearestPlanet.name}")
                    
        
    def isPlanetNearEnough(self, planet):
        return np.sqrt((self.r_x[self.aktuellerrechenschritt] - planet.r_x[self.aktuellerrechenschritt])**2 + 
                       (self.r_z[self.aktuellerrechenschritt] - planet.r_z[self.aktuellerrechenschritt])**2) < planet.radius * 100

    def update_scale(self,scale):
        self.radius *= scale
        if self.radius > MIN_ROCKET_RADIUS and self.radius < 0.1:
            self.notRotatedImg = pygame.transform.scale_by(self.img0, max(min(0.1*self.radius, 1), 0.1))
    def draw(self, window, move_x, move_y, planets, paused, scale, width, height):
        print(self.entryAngle)
        if not self.rocketstarted or self.landed:
            #self.drawAndValueBeforeStarting(window, scale, width, height, move_x, move_y)
            self.drawIfNotStarted(paused, planets, window, scale, width, height, move_x, move_y)
            return
        """"
        if self.landed:
            self.landing(window, scale, width, height, move_x, move_y)
            if paused:
                return
            if planets[0].aktuellerschritt == 0 or self.timestepChanged:
                print("Bedingung erreicht")
                for planet in planets:
                    planet.aktuellerrechenschritt = planet.aktuellerschritt
                for i in range(NUM_OF_PREDICTIONS):
                    for planet in planets:
                        planet.predictNext(planets, paused)

                if self.timestepChanged:
                    self.timestepChanged = False

                else:
                    for planet in planets:
                        planet.predictNext(planets, paused)

                for planet in planets:
                    planet.aktuellerschritt += 1

                if planets[0].aktuellerschritt >= NUM_OF_PREDICTIONS:
                    for planet in planets:
                        planet.resetArray()
            return
        """
        if not paused:
            if self.powerchanged or self.aktuellerschritt==0 or self.timestepChanged:
                firstTime = self.aktuellerrechenschritt == 0
                if firstTime:
                    for planet in planets:
                        planet.resetPlanetsArrayToSyncWithRocket()
                self.aktuellerrechenschritt = self.aktuellerschritt
                self.calculateNewCalculationOfPredictions(firstTime, planets, paused)
                if not (firstTime or self.timestepChanged):
                    for planet in planets:
                        planet.predictStep(self.aktuellerrechenschritt-1, planets, paused, self)

                self.powerchanged = False
                self.timestepChanged = False

            else:
                self.calculateOnePrediction(planets, paused)
        # move_x and move_y verschieben je nach bewegung des Bildschirm
        if self.aktuellerrechenschritt > 2:
            pygame.draw.lines(window, self.color, False, np.array((self.r_x[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt:self.aktuellerrechenschritt]*scale+move_y+ height/2)).T, 1)
            
            self.drawRocket(window, width, height, move_x, move_y, scale)
        if paused:
            return
        self.aktuellerschritt += 1
        for planet in planets:
            planet.aktuellerschritt += 1

        if self.aktuellerschritt >= (NUM_OF_PREDICTIONS):
            self.resetArray()
            for planet in planets:
                planet.resetArray()

            
                
    def getCurrentDistanceToNextPlanet(self):
        if self.planetNearEnough == False:
            return -1
        return np.sqrt((self.r_x[self.aktuellerrechenschritt] - self.nearestPlanet.r_x[self.aktuellerrechenschritt])**2 + 
                           (self.r_z[self.aktuellerrechenschritt] - self.nearestPlanet.r_z[self.aktuellerrechenschritt])**2)


    def drawRocket(self, window, width, height, move_x, move_y, scale):
        if self.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(window, self.color, (self.r_x[self.aktuellerschritt]*scale+move_x+width/2, self.r_z[self.aktuellerschritt]*scale+move_y+height/2), MIN_ROCKET_RADIUS)
            return
        self.img = pygame.transform.rotate(self.notRotatedImg, math.atan2(self.v_z[self.aktuellerschritt], self.v_x[self.aktuellerschritt]) * (-180) /np.pi - 90)
        #img = pygame.transform.rotozoom(img0, math.atan2(self.v_z[self.aktuellerschritt], self.v_x[self.aktuellerschritt]), max(0.05, self.radius))
        window.blit(self.img, (self.r_x[self.aktuellerschritt]*scale+move_x+width/2 -self.img.get_width()/2 , self.r_z[self.aktuellerschritt]*scale+move_y+height/2 - self.img.get_height()/2))

    def getRelativeVelocity(self, i):
        if not self.rocketstarted:
            return 0
        return np.sqrt( (self.v_x[i] - self.nearestPlanet.v_x[i])**2 
                        + (self.v_z[i] - self.nearestPlanet.v_z[i])**2)
        
    def getCurrentRelativeVelocity(self):
        if not self.rocketstarted:
            return 0
        return np.sqrt( (self.v_x[self.aktuellerschritt] - self.nearestPlanet.v_x[self.aktuellerschritt])**2 
                        + (self.v_z[self.aktuellerschritt] - self.nearestPlanet.v_z[self.aktuellerschritt])**2)


    # in m/s
    def getAbsoluteVelocity(self):
        if not self.rocketstarted:
            return 0
        return np.sqrt(self.v_x[self.aktuellerschritt]**2 + self.v_z[self.aktuellerschritt]**2)
    def resetArray(self):
        self.r_x[1:NUM_OF_PREDICTIONS+1] = self.r_x[NUM_OF_PREDICTIONS:]
        self.r_z[1:NUM_OF_PREDICTIONS+1] = self.r_z[NUM_OF_PREDICTIONS:]
        self.v_x[1:NUM_OF_PREDICTIONS+1] = self.v_x[NUM_OF_PREDICTIONS:]
        self.v_z[1:NUM_OF_PREDICTIONS+1] = self.v_z[NUM_OF_PREDICTIONS:]
        self.aktuellerschritt = 1
        self.aktuellerrechenschritt = NUM_OF_PREDICTIONS

    def drawAndValueBeforeStarting(self,window, scale, width, height, move_x, move_y):
        
        angle = self.entryAngle if self.landed else self.startwinkel
        self.r_x[0] = self.startplanet.r_x[self.startplanet.aktuellerschritt] + self.startplanet.radius * np.cos(angle * np.pi / 180)  
        self.r_z[0] = self.startplanet.r_z[self.startplanet.aktuellerschritt] + self.startplanet.radius * np.sin(angle * np.pi / 180)
        self.v_x[0] = self.startplanet.v_x[self.startplanet.aktuellerschritt]
        self.v_z[0] = self.startplanet.v_z[self.startplanet.aktuellerschritt]

        self.drawRocket(window, width, height, move_x, move_y, scale)

    def calculateEntryAngle(self):
        self.entryAngle =  math.atan2(self.r_z[self.aktuellerschritt] - self.nearestPlanet.r_z[self.nearestPlanet.aktuellerschritt],
                          self.r_x[self.aktuellerschritt] - self.nearestPlanet.r_x[self.nearestPlanet.aktuellerschritt]) * (180 / np.pi)
        print(self.entryAngle)

        
    def calculateNewCalculationOfPredictions(self, firstTime, planets, paused):
        for i in range(NUM_OF_PREDICTIONS):
            if firstTime or self.timestepChanged:
                for planet in planets:
                    planet.predictStep(self.aktuellerrechenschritt, planets, paused, self)
            self.berechneNaechstenSchritt(self.aktuellerrechenschritt, planets)
            self.aktuellerrechenschritt += 1

    def calculateOnePrediction(self, planets, paused):
        for planet in planets:
            planet.predictStep(self.aktuellerrechenschritt, planets, paused, self)
        self.berechneNaechstenSchritt(self.aktuellerrechenschritt, planets)
        self.aktuellerrechenschritt += 1
        
    def clearArray(self):
        self.r_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.r_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)

        self.aktuellerschritt = 0
        self.aktuellerrechenschritt = 0

        self.r_x[0] = self.nearestPlanet.r_x[self.nearestPlanet.aktuellerschritt] + self.nearestPlanet.radius * np.cos(self.entryAngle * np.pi / 180)  
        self.r_z[0] = self.nearestPlanet.r_z[self.nearestPlanet.aktuellerschritt] + self.nearestPlanet.radius * np.sin(self.entryAngle * np.pi / 180)
        self.v_x[0] = self.nearestPlanet.v_x[self.nearestPlanet.aktuellerschritt]
        self.v_z[0] = self.nearestPlanet.v_z[self.nearestPlanet.aktuellerschritt]


    def drawIfNotStarted(self, paused, planets, window, scale, width, height, move_x, move_y):
        self.drawAndValueBeforeStarting(window, scale, width, height, move_x, move_y)
            
        if not paused:
            if planets[0].aktuellerschritt == 0 or self.timestepChanged:
                for planet in planets:
                    planet.aktuellerrechenschritt = planet.aktuellerschritt
                for i in range(NUM_OF_PREDICTIONS):
                    for planet in planets:
                        planet.predictNext(planets, paused)

                if self.timestepChanged:
                    self.timestepChanged = False

            else:
                for planet in planets:
                    planet.predictNext(planets, paused)

            for planet in planets:
                planet.aktuellerschritt += 1

            if planets[0].aktuellerschritt >= NUM_OF_PREDICTIONS:
                for planet in planets:
                    planet.resetArray()