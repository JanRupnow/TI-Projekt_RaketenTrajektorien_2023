import pygame
import pygame_gui as pg
import sys
import variables.hotkeys as keys
from variables.konstanten import *
from methods.support_methods import *
from methods.json_methods import *
import json

manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = clock.tick(60)/1000

def createUiButton(text, position_x,position_y):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x,position_y), (WIDTH*0.07,HEIGHT*0.07)),
                         text=text,
                         manager=manager,
                         object_id=removeSpaces(text+"_label"))

def initialiseStartScreen():
    createUiButton("Start the Game", WIDTH*0.5, HEIGHT*0.9)
    
showGUI = True
def show_startScreen():
    while showGUI:
        for event in pygame.event.get():
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()