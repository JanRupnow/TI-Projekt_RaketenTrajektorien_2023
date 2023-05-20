import pygame
import pygame_gui as pg
import sys
import variables.hotkeys as keys
from variables.konstanten import *
from methods.support_methods import *
from methods.json_methods import *
from views.view_helper import *
import json

manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = clock.tick(60)/1000


def updateRocketConfigs(event):
    jsonfile = open("./variables/rocket_config/current_rocket_config.json", "r+")
    newJson = keys.updateKeyInJsonRocket(json.load(jsonfile), event.ui_object_id, event.text)

    jsonfile.seek(0)
    jsonfile.truncate()
    json.dump(newJson, jsonfile, indent=4, ensure_ascii=False)
    jsonfile.close()

def getTextsAndValuesForConfigUI():
    jsonfile = open("./variables/rocket_config/current_rocket_config.json", "r")
    config = json.load(jsonfile)

    configPairs = []

    for category in config.keys():
        try:
            for key in config[category].keys():
                configPairs.append((config[category][key]["value"], config[category][key]["text"]))
        except:
            pass

    jsonfile.close()
    return configPairs


def initializeStartUI():
    createUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05, manager)
    createUiButton("Start the Game", WIDTH*0.465, HEIGHT*0.8, manager)
    createUiButton("Configure the Rocket", WIDTH*0.45, HEIGHT*0.7, manager, WIDTH*0.1)

def initializeRocketConfigurationUI():
    createUiLabel("Rocket Configuration", WIDTH*0.7, HEIGHT*0.2, manager)

    configPairs = getTextsAndValuesForConfigUI()
    for i in range(len(configPairs)):
        createUiTextBoxAndTextEntry(configPairs[i][1], configPairs[i][0], WIDTH*0.7, HEIGHT*0.25 + HEIGHT*0.05*i, manager)

# removes all ui elements => no used object_ids
def clearStartUI():
    manager.clear_and_reset() 

def showStartUI():
    showGUI = True
    showConfiguration = False

    if len(manager.get_sprite_group())<4:
        initializeStartUI()

    while showGUI:
        for event in pygame.event.get():

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "StarttheGame_button":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ConfiguretheRocket_button" and not showConfiguration:
                initializeRocketConfigurationUI()
                showConfiguration = True
            if checkKeyDown(event, keys.H_closeWindow[0]):
                pygame.quit()
                sys.exit()
            if event.type == pg.UI_TEXT_ENTRY_FINISHED:
                updateRocketConfigs(event)
                clearStartUI()
                initializeStartUI()
                initializeRocketConfigurationUI()
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()
    
    clearStartUI()