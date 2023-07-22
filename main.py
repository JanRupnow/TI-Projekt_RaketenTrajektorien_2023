import pygame
import datetime

from Globals.Constants import DATA

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.GameManager import GameManager

from Methods.PackageInstaller import InstallAllPackages
from Methods.ConfigurePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents
from Methods.RocketConfig import LoadRocket

def main():

    InstallAllPackages()
    ShowStartUI()

    now = datetime.datetime.now()
    global CLOCK
    
    ConfigureStartValues()
    planets = ConfigurePlanets()
    rocket = LoadRocket(planets)

    while DATA.getRun():
        CLOCK.tick(60)
        
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket = ProcessHotKeyEvents(event, rocket, planets)

        GameManager.CalculateNextIteration(rocket, planets)
        GameManager.DisplayIteration(rocket, planets)
        RenderFlightInterface(rocket, now)
        
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()