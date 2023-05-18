import pygame
import pygame_gui as pg
import sys
import variables.hotkeys as keys
from variables.konstanten import *
from methods.support_methods import *
from methods.jsonHotkeys import *
import json

manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = clock.tick(60)/1000

def changeHotKeyFromInput(event,hotkey):
    if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == removeSpaces(hotkey[1]):
        jsonfile = open("./variables/hotkeys/current_hotkeys.json")
        hotkey[0] = ord(event.text)
        newJson = keys.updateKeyInJson(jsonfile,hotkey)
        #parsed = json.loads(newJson)
        #print(json.dumps(parsed, indent=4))
        json.dump(newJson, jsonfile, indent=4, ensure_ascii=False)
    return hotkey[0]

def changeAllHotKeysFromInput(event,hotkeys):
    for hotkey in hotkeys:
        hotkey[0] = changeHotKeyFromInput(event, hotkey)
                                         
def createUiTextBoxAndTextEntry(hotkey,position_x, position_y):
    TEXT_BOX = pg.elements.UITextBox(hotkey[1],
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=removeSpaces(hotkey[1]+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1,position_y), (WIDTH*0.03,HEIGHT*0.05)), 
                                             manager = manager, 
                                             object_id = removeSpaces(hotkey[1]))
    TEXT_INPUT.length_limit = 1
    TEXT_INPUT.set_text(getStringOfAscii(hotkey[0]))

def createUiCloseButton():
    label = createUiButton("Close Settings", 0,0)
    return label
def createUiButton(text, position_x,position_y):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x,position_y), (WIDTH*0.07,HEIGHT*0.07)),
                         text=text,
                         manager=manager,
                         object_id=removeSpaces(text+"_label"))

def createUiSettingsTitleLabel():
    title_label = createUiLabel("Settings", WIDTH*0.45, 0.15*HEIGHT)
    title_label.text_horiz_alignment = "center"
    title_label.rebuild()
    return title_label
    

def createUiLabel(text, position_x, position_y):
    return pg.elements.UILabel(relative_rect=pygame.Rect((position_x,position_y), (WIDTH*0.1,HEIGHT*0.05)),
                               text=text,
                               manager=manager,
                               object_id=removeSpaces(text+"_label"))

    
def createUiSettingsTopicLabel(text, position_x, position_y):
    label = createUiLabel(text, position_x, position_y)
    label.text_horiz_alignment = "left"
    label.text_colour = "red"
    label.rebuild()
    return label

def createUiGameTitleLabel(text, position_x, position_y):
    label = createUiLabel(text, position_x, position_y)
    label.text_horiz_alignment = "center"
    label.text_colour = "green"
    label.set_text_scale(15)
    label.rebuild()
    return label
def InitializeSettingsUI():
    createUiSettingsTitleLabel()
    createUiCloseButton()
    createUiButton("Reset Controls", WIDTH*0.8, HEIGHT*0.1)
    createUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05)

    createUiTextBoxAndTextEntry(keys.H_displayHotKeys, WIDTH*0.1, HEIGHT*0.2)
    createUiTextBoxAndTextEntry(keys.H_leaveSimulation, WIDTH*0.1, HEIGHT*0.25)
    createUiTextBoxAndTextEntry(keys.H_openSettings, WIDTH*0.1, HEIGHT*0.3)
    createUiTextBoxAndTextEntry(keys.H_closeWindow, WIDTH*0.1, HEIGHT*0.35)
    createUiSettingsTopicLabel("Rocket Controls", WIDTH*0.1, HEIGHT*0.4)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostForward, WIDTH*0.1, HEIGHT*0.45)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostLeft, WIDTH*0.1, HEIGHT*0.5)
    createUiTextBoxAndTextEntry(keys.H_rocketBoostRight, WIDTH*0.1, HEIGHT*0.55)
    createUiTextBoxAndTextEntry(keys.H_lowerRocketBoost, WIDTH*0.1, HEIGHT*0.6)
    createUiSettingsTopicLabel("Zoom Controls", WIDTH*0.1, HEIGHT*0.65)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketStart, WIDTH*0.1, HEIGHT*0.7)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketPlanet, WIDTH*0.1, HEIGHT*0.75)
    createUiTextBoxAndTextEntry(keys.H_zoomRocketPlanetSystem, WIDTH*0.1, HEIGHT*0.8)
    createUiTextBoxAndTextEntry(keys.H_zoomAutoOnRocket, WIDTH*0.1, HEIGHT*0.85)

def showHotKeySettings():

    if len(manager.get_sprite_group())<4:
        InitializeSettingsUI()

    showGUI = True

    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "CloseSettings_label":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_label":
                keys.resetOverwriteCurrent()
            if checkKeyDown(event, keys.H_closeWindow[0]):
                showGUI = False
            changeAllHotKeysFromInput(event, keys.listHotKeys)
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()


