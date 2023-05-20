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


def resetCurrentRocketConfig():
    currentJsonFile = open("./variables/rocket_config/current_rocket_config.json", "w")
    standardJsonFile = open("./variables/rocket_config/standard_rocket_config.json", "r")

    json.dump(json.load(standardJsonFile), currentJsonFile, indent=4, ensure_ascii=False)

    currentJsonFile.close()
    standardJsonFile.close()

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


def initializeStartUI(selectedNumber=0):
    createUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05, manager)
    createUiButton("Start the Game", WIDTH*0.465, HEIGHT*0.8, manager)
    createUiButton("Configure the Rocket", WIDTH*0.45, HEIGHT*0.7, manager, WIDTH*0.1)
    createRocketImage(selectedNumber, manager)

def initializeRocketConfigurationUI():
    createUiLabel("Rocket Configuration", WIDTH*0.7, HEIGHT*0.2, manager)
    createUiButton("Reset Controls", WIDTH*0.8, HEIGHT*0.8, manager)
    createUiButton("Previous", WIDTH*0.38, HEIGHT*0.7, manager)
    createUiButton("Next", WIDTH*0.55, HEIGHT*0.7, manager)
    configPairs = getTextsAndValuesForConfigUI()
    for i in range(len(configPairs)):
        createUiTextBoxAndTextEntry(configPairs[i][1], configPairs[i][0], WIDTH*0.7, HEIGHT*0.25 + HEIGHT*0.05*i, manager)

# removes all ui elements => no used object_ids
def clearStartUI():
    manager.clear_and_reset() 

def resetAndShowUI(selectedNumber):
    clearStartUI()
    initializeStartUI(selectedNumber)
    initializeRocketConfigurationUI()

def resetUI(selectedNumber,manager): 
    for element in manager.root_container.elements:
        if "rocket_image" in element.object_ids:
            remove_element = element
            element.kill()
    manager.clear_and_reset()
    manager.root_container.kill()
    manager.root_container.remove_element(remove_element)
    manager.root_container.remove_element_from_focus_set(remove_element)
    manager.root_container.update(1)
    initializeStartUI(selectedNumber)
    initializeRocketConfigurationUI()

def showStartUI():
    showGUI = True
    showConfiguration = False
    selectedNumber = 3
    if len(manager.get_sprite_group())<4:
        initializeStartUI(selectedNumber)
    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "StarttheGame_button":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ConfiguretheRocket_button" and not showConfiguration:
                initializeRocketConfigurationUI()
                showConfiguration = True
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_button":
                resetCurrentRocketConfig()
                resetAndShowUI(selectedNumber)
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Previous_button" and selectedNumber > 0:
                selectedNumber-= 1
                resetUI(selectedNumber,manager)
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Next_button" and selectedNumber < 3:
                selectedNumber+= 1
                resetUI(selectedNumber, manager)
            if checkKeyDown(event, keys.H_closeWindow[0]):
                pygame.quit()
                sys.exit()
                
            if event.type == pg.UI_TEXT_ENTRY_FINISHED:
                updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()
    
    clearStartUI()