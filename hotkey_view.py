import pygame
import pygame_gui
import sys
from variables.hotkeys import *
from variables.konstanten import *
from methods.support_methods import *

def showHotKeySettings():
    global H_centerOnRocket
    MANAGER = pygame_gui.UIManager((WIDTH,HEIGHT))
    TEXT_FUEL = pygame_gui.elements.UITextBox("Treibstoffmasse eingeben:",relative_rect= pygame.Rect((350,275),(250,50)),manager = MANAGER, object_id="fuel_text")
    TEXT_INPUT_FUEL = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((600,275),(100,50)), manager = MANAGER, object_id = "user_input_fuel")
    TEXT_MASS  = pygame_gui.elements.UITextBox("Gesamtmasse eingeben:",relative_rect= pygame.Rect((350,350),(250,50)),manager = MANAGER, object_id="mass_text")
    TEXT_INPUT_MASS = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 350), (100, 50)),
                                                          manager=MANAGER, object_id="user_input_mass")
    TEXT_INPUT_MASS.length_limit = 1
    UI_REFRESH_RATE = clock.tick(60)/1000
    showGUI = True
    while showGUI:
        for event in pygame.event.get():
            if checkKeyDown(event, H_closeWindow):
                showGUI = False
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "user_input_mass":
                H_centerOnRocket = ord(event.text)
            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(WINDOW)
        pygame.display.update()
showHotKeySettings()
