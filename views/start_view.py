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

def getSelectedRocket():
    return json.load(open("./variables/rocket_config/current_rocket_config.json", "r+"))["Image"]["selectedNumber"]

def getStartplanetName():
    return json.load(open("./variables/rocket_config/current_rocket_config.json", "r+"))["Start"]["Startplanet"]["value"]

def updateSelectedRocket(selectedRocket):
    jsonfile = open("./variables/rocket_config/current_rocket_config.json", "r+")
    
    config = json.load(jsonfile)
    config["Image"]["selectedNumber"] = selectedRocket

    jsonfile.seek(0)
    jsonfile.truncate()
    json.dump(config, jsonfile, indent=4, ensure_ascii=False)
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
    createUiButton("Reset Configuration", WIDTH*0.8, HEIGHT*0.8, manager, length_x= WIDTH*0.1)
    createUiButton("Previous", WIDTH*0.38, HEIGHT*0.7, manager)
    createUiButton("Next", WIDTH*0.55, HEIGHT*0.7, manager)
    configPairs = getTextsAndValuesForConfigUI()
    createUiTextBoxAndTextEntry(configPairs[0][1], configPairs[0][0], WIDTH*0.7, HEIGHT*0.3, manager)
    createUiTextBox(configPairs[1][1],WIDTH*0.7, HEIGHT*0.35, manager)
    createDropDown(planetNameArray,
                              planetNameArray.index(getStartplanetName()),
                              WIDTH*0.8, HEIGHT*0.35, manager)
    createUiTextBoxAndTextEntry(configPairs[2][1], configPairs[2][0], WIDTH*0.7, HEIGHT*0.4, manager)
    createUiTextBoxAndTextEntry(configPairs[3][1], configPairs[3][0], WIDTH*0.7, HEIGHT*0.45, manager)
    createUiTextBoxAndTextEntry(configPairs[4][1], configPairs[4][0], WIDTH*0.7, HEIGHT*0.5, manager,size_x=WIDTH*0.03)
    createUiTextBoxAndTextEntry(configPairs[5][1], configPairs[5][0], WIDTH*0.7, HEIGHT*0.55, manager)
    createUiTextBoxAndTextEntry(configPairs[6][1], configPairs[6][0], WIDTH*0.2, HEIGHT*0.3, manager)
    createUiTextBoxAndTextEntry(configPairs[7][1], configPairs[7][0], WIDTH*0.2, HEIGHT*0.35, manager)
    createUiTextBoxAndTextEntry(configPairs[8][1], configPairs[8][0], WIDTH*0.2, HEIGHT*0.4, manager)
# removes all ui elements => no used object_ids
def clearStartUI():
    manager.clear_and_reset() 

def resetAndShowUI(selectedNumber):
    clearStartUI()
    initializeStartUI(selectedNumber)
    initializeRocketConfigurationUI()


def showStartUI():
    showGUI = True
    showConfiguration = False
    selectedNumber = getSelectedRocket()
    if len(manager.get_sprite_group())<4:
        initializeStartUI(selectedNumber)
    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "StarttheGame_button":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ConfiguretheRocket_button" and not showConfiguration:
                initializeRocketConfigurationUI()
                showConfiguration = True
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetConfiguration_button":
                resetCurrentRocketConfig()
                resetAndShowUI(selectedNumber)
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Previous_button" and selectedNumber > 0:
                selectedNumber-= 1
                createRocketImage(selectedNumber, manager)
                updateSelectedRocket(selectedNumber)
                resetAndShowUI(selectedNumber)

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Next_button" and selectedNumber < 3:
                selectedNumber+= 1
                updateSelectedRocket(selectedNumber)
                createRocketImage(selectedNumber, manager)
                resetAndShowUI(selectedNumber)
            if event.type == pg.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id =="startplanet_dropdown":
                #dropdown.selected_option = "Moon"
                updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)
            if checkKeyDown(event, keys.H_closeWindow[0]):
                pygame.quit()
                sys.exit()
            if checkKeyDown(event, keys.H_leaveSimulation[0]):
                pygame.quit()
                sys.exit()  
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "angleonplanet_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) < 360 and int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startangle_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) <= 45 and int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startthrust_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) <= 10 and int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "massoftherocketstructure_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "massofthepropellant_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)
            
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "yearofrocketstart_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) <= 10000 and int(event.text) >= 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "monthofrocketstart_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) <= 12 and int(event.text) > 0:
                        updateRocketConfigs(event)
                resetAndShowUI(selectedNumber)
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "dayofrocketstart_input":
                if is_convertible_to_int(event.text):
                    if getMonth() in [1,3,5,7,8,10,12]:
                        if int(event.text) <= 31 and int(event.text) > 0:
                            updateRocketConfigs(event)
                    elif getMonth() in [4,6,9,11]:
                        if int(event.text) <= 30 and int(event.text) > 0:
                            updateRocketConfigs(event)
                    elif getYear() % 4 == 0:
                        if int(event.text) <= 28 and int(event.text) > 0:
                            updateRocketConfigs(event)
                        else: 
                            overWriteStandardDay()
                    else:
                        if int(event.text) <= 29 and int(event.text) > 0:
                            updateRocketConfigs(event)
                        else:
                            overWriteStandardDay()
                resetAndShowUI(selectedNumber)
            manager.process_events(event)
        
        WINDOW.fill((0, 0, 0))
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()
    
    clearStartUI()