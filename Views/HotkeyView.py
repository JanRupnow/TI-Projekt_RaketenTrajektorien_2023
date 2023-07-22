import pygame
import pygame_gui as pg
import sys
import json

import Globals.Hotkeys as keys
from Globals.Constants import *

from Views.ViewComponents import *

from Methods.SupportMethods import *
from Methods.JsonMethods import *
from Methods.ViewMethods import *


manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = CLOCK.tick(60)/1000


def ChangeHotKeyFromInput(event,hotkey):
    if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == RemoveSpaces(hotkey[1]+"_input") and event.text != "":
        jsonfile = open("./variables/hotkeys_config/current_hotkeys.json", "r+")
        hotkey[0] = ord(event.text)
        newJson = keys.UpdateKeyInJson(json.load(jsonfile),hotkey)

        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(newJson, jsonfile, indent=4, ensure_ascii=False)
    return hotkey[0]

def ChangeAllHotKeysFromInput(event,hotkeys):
    for hotkey in hotkeys:
        hotkey[0] = ChangeHotKeyFromInput(event, hotkey)

def CreateUiCloseButton():
    label = CreateUiButton("Close Settings", 0,0, manager)
    return label

def CreateUiSettingsTitleLabel():
    title_label = CreateUiLabel("Settings", WIDTH*0.45, 0.15*HEIGHT, manager)
    title_label.text_horiz_alignment = "center"
    title_label.rebuild()
    return title_label




# removes all ui elements => no used object_ids
def ClearSettingsUI():
    manager.clear_and_reset() 

def InitializeSettingsUI():
    CreateUiSettingsTitleLabel()
    CreateUiCloseButton()
    CreateUiButton("Reset Controls", WIDTH*0.9, HEIGHT*0.9, manager)
    CreateUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05, manager)
    CreateUiSettingsTopicLabel("General Controls (not mutable)", WIDTH*0.1, HEIGHT*0.15, manager, WIDTH*0.12)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_displayHotKeys, WIDTH*0.1, HEIGHT*0.2, manager, False, "6")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_leaveSimulation, WIDTH*0.1, HEIGHT*0.25, manager, False, "X")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_openSettings, WIDTH*0.1, HEIGHT*0.3, manager, False, "F1")
    CreateUiSettingsTopicLabel("Rocket Controls", WIDTH*0.1, HEIGHT*0.35, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_rocketBoostForward, WIDTH*0.1, HEIGHT*0.4, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_rocketBoostLeft, WIDTH*0.1, HEIGHT*0.45, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_rocketBoostRight, WIDTH*0.1, HEIGHT*0.5, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_lowerRocketBoost, WIDTH*0.1, HEIGHT*0.55, manager)
    CreateUiSettingsTopicLabel("Zoom Controls", WIDTH*0.1, HEIGHT*0.6, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_zoomAutoOnReferencePlanet, WIDTH*0.1, HEIGHT*0.65, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_zoomRocketStart, WIDTH*0.1, HEIGHT*0.7, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_zoomRocketPlanet, WIDTH*0.1, HEIGHT*0.75, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_zoomRocketPlanetSystem, WIDTH*0.1, HEIGHT*0.8, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_zoomAutoOnRocket, WIDTH*0.1, HEIGHT*0.85, manager)
    CreateUiSettingsTopicLabel("Navigation Controls (not mutable)", WIDTH*0.7, HEIGHT*0.15, manager, WIDTH*0.15)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_moveScreenUp, WIDTH*0.7, HEIGHT*0.2, manager, False, "UP")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_moveScreenLeft, WIDTH*0.7, HEIGHT*0.25, manager, False, "LEFT")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_moveScreenRight, WIDTH*0.7, HEIGHT*0.3, manager, False, "RIGHT")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_moveScreenDown, WIDTH*0.7, HEIGHT*0.35, manager, False, "DOWN")
    CreateUiSettingsTopicLabel("Display Controls", WIDTH*0.7, HEIGHT*0.4, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_pauseSimulation, WIDTH*0.7, HEIGHT*0.45, manager, False, "SPACE")
    CreateUiTextBoxAndTextEntryHotkey(keys.H_drawLine, WIDTH*0.7, HEIGHT*0.5, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_showDistance, WIDTH*0.7, HEIGHT*0.55, manager)
    CreateUiSettingsTopicLabel("Time Controls", WIDTH*0.7, HEIGHT*0.6, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_shiftTimeStepUp, WIDTH*0.7, HEIGHT*0.65, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_shiftTimeStepDown, WIDTH*0.7, HEIGHT*0.7, manager)
    CreateUiSettingsTopicLabel("Center Controls", WIDTH*0.7, HEIGHT*0.75, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_centerOnRocket, WIDTH*0.7, HEIGHT*0.8, manager)
    CreateUiTextBoxAndTextEntryHotkey(keys.H_centerOnSun, WIDTH*0.7, HEIGHT*0.85, manager)

def ShowSettingsUI():
    if len(manager.get_sprite_group())<4:
        InitializeSettingsUI()

    showGUI = True

    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "CloseSettings_button":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_button":
                keys.resetOverwriteCurrent()
                manager.clear_and_reset()     
                InitializeSettingsUI()
            if CheckKeyDown(event, keys.H_closeWindow[0]):
                showGUI = False
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id.endswith("_notMutable"):    
                manager.clear_and_reset()
                InitializeSettingsUI()
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id.endswith("_input"):
                if event.text != "":
                    if ord(event.text) > 32 and ord(event.text) < 127:
                        ChangeAllHotKeysFromInput(event, keys.listHotKeys)
                manager.clear_and_reset()
                InitializeSettingsUI()
            if CheckKeyDown(event, keys.H_leaveSimulation[0]):
                pygame.quit()
                sys.exit()
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()

    ClearSettingsUI()
