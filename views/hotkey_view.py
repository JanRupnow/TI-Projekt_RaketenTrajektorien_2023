import pygame
import pygame_gui as pg
import sys
import variables.hotkeys as keys
from variables.konstanten import *
from methods.support_methods import *
from methods.json_methods import *
import json
from views.view_helper import *

manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = clock.tick(60)/1000


def changeHotKeyFromInput(event,hotkey):
    if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == removeSpaces(hotkey[1]):
        jsonfile = open("./variables/hotkeys/current_hotkeys.json", "r+")
        hotkey[0] = ord(event.text)
        newJson = keys.updateKeyInJson(json.load(jsonfile),hotkey)

        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(newJson, jsonfile, indent=4, ensure_ascii=False)
    return hotkey[0]

def changeAllHotKeysFromInput(event,hotkeys):
    for hotkey in hotkeys:
        hotkey[0] = changeHotKeyFromInput(event, hotkey)

def createUiCloseButton():
    label = createUiButton("Close Settings", 0,0, manager)
    return label

def createUiSettingsTitleLabel():
    title_label = createUiLabel("Settings", WIDTH*0.45, 0.15*HEIGHT, manager)
    title_label.text_horiz_alignment = "center"
    title_label.rebuild()
    return title_label




# removes all ui elements => no used object_ids
def clearSettingsUI():
    manager.clear_and_reset() 

def initializeSettingsUI():
    createUiSettingsTitleLabel()
    createUiCloseButton()
    createUiButton("Reset Controls", WIDTH*0.8, HEIGHT*0.1, manager)
    createUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05, manager)

    createUiTextBoxAndTextEntry(keys.H_displayHotKeys, WIDTH*0.1, HEIGHT*0.2, manager)
    createUiTextBoxAndTextEntry(keys.H_leaveSimulation, WIDTH*0.1, HEIGHT*0.25, manager)
    createUiTextBoxAndTextEntry(keys.H_openSettings, WIDTH*0.1, HEIGHT*0.3, manager)
    createUiTextBoxAndTextEntry(keys.H_closeWindow, WIDTH*0.1, HEIGHT*0.35, manager)
    createUiSettingsTopicLabel("Rocket Controls", WIDTH*0.1, HEIGHT*0.4, manager)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostForward, WIDTH*0.1, HEIGHT*0.45, manager)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostLeft, WIDTH*0.1, HEIGHT*0.5, manager)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostRight, WIDTH*0.1, HEIGHT*0.55, manager)
    createUiTextBoxAndTextEntry(keys.H_lowerRocketBoost, WIDTH*0.1, HEIGHT*0.6, manager)
    createUiSettingsTopicLabel("Zoom Controls", WIDTH*0.1, HEIGHT*0.65, manager)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketStart, WIDTH*0.1, HEIGHT*0.7, manager)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketPlanet, WIDTH*0.1, HEIGHT*0.75, manager)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketPlanetSystem, WIDTH*0.1, HEIGHT*0.8, manager)
    createUiTextBoxAndTextEntry(keys.H_zoomAutoOnRocket, WIDTH*0.1, HEIGHT*0.85, manager)

def showSettingsUI():

    if len(manager.get_sprite_group())<4:
        initializeSettingsUI()

    showGUI = True

    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "CloseSettings_label":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_label":
                keys.resetOverwriteCurrent()
                manager.clear_and_reset()     
                initializeSettingsUI()
            if checkKeyDown(event, keys.H_closeWindow[0]):
                showGUI = False
            changeAllHotKeysFromInput(event, keys.listHotKeys)
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()
