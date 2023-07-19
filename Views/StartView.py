import pygame
import pygame_gui as pg
import json
import sys

import Globals.Hotkeys as keys
from Globals.Constants import *

from Views.ViewElements import *

from Methods.SupportMethods import *
from Methods.JsonMethods import *
from Methods.ViewMethods import *

manager = pg.UIManager((WIDTH,HEIGHT))
UI_REFRESH_RATE = Clock.tick(60)/1000

def ShowStartUI():
    showGUI = True
    showConfiguration = False
    selectedNumber = GetSelectedRocket()
    if len(manager.get_sprite_group())<4:
        InitializeStartUI(selectedNumber)
    while showGUI:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "StarttheGame_button":
                showGUI = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ConfiguretheRocket_button" and not showConfiguration:
                InitializeRocketConfigurationUI()
                showConfiguration = True
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetConfiguration_button":
                ResetCurrentRocketConfig()
                ResetAndShowUI(selectedNumber)
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Previous_button" and selectedNumber > 0:
                selectedNumber-= 1
                CreateRocketImage(selectedNumber, manager)
                UpdateSelectedRocket(selectedNumber)
                ResetAndShowUI(selectedNumber)

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Next_button" and selectedNumber < 3:
                selectedNumber+= 1
                UpdateSelectedRocket(selectedNumber)
                CreateRocketImage(selectedNumber, manager)
                ResetAndShowUI(selectedNumber)
            if event.type == pg.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id =="startplanet_dropdown":
                #dropdown.selected_option = "Moon"
                UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)
            if CheckKeyDown(event, keys.H_closeWindow[0]):
                pygame.quit()
                sys.exit()
            if CheckKeyDown(event, keys.H_leaveSimulation[0]):
                pygame.quit()
                sys.exit()  
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "angleonplanet_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) < 360 and int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startangle_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) <= 45 and int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startthrust_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) <= 10 and int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "massoftherocketstructure_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "massofthepropellant_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)
            
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "yearofrocketstart_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) <= 10000 and int(event.text) >= 0:
                        UpdateRocketConfigs(event)
                        if CheckDateIsLegal(GetStartMonth(), GetStartDay()):
                            UpdateRocketConfigs(event)
                        else:
                            UpdateRocketConfigs(event)
                            OverWriteStandardDay()
                ResetAndShowUI(selectedNumber)
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "monthofrocketstart_input":
                if IsConvertibleToInt(event.text):
                    if int(event.text) <= 12 and int(event.text) > 0:
                        if CheckDateIsLegal(event.text, GetStartDay()):
                            UpdateRocketConfigs(event)
                        else:
                            UpdateRocketConfigs(event)
                            OverWriteStandardDay()
                ResetAndShowUI(selectedNumber)
            
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "dayofrocketstart_input":
                if IsConvertibleToInt(event.text):
                    if GetStartMonth() in [1,3,5,7,8,10,12]:
                        if int(event.text) <= 31 and int(event.text) > 0:
                            UpdateRocketConfigs(event)
                    elif GetStartMonth() in [4,6,9,11]:
                        if int(event.text) <= 30 and int(event.text) > 0:
                            UpdateRocketConfigs(event)
                    elif getStartYear() % 4 != 0:
                        if int(event.text) <= 28 and int(event.text) > 0:
                            UpdateRocketConfigs(event)
                    else:
                        if int(event.text) <= 29 and int(event.text) > 0:
                            UpdateRocketConfigs(event)
                ResetAndShowUI(selectedNumber)
            manager.process_events(event)
        
        WINDOW.fill((0, 0, 0))
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()
    
    ClearStartUI()



def InitializeStartUI(selectedNumber=0):
    CreateUiGameTitleLabel("Spaceflight Simulator", WIDTH*0.45, HEIGHT*0.05, manager)
    CreateUiButton("Start the Game", WIDTH*0.465, HEIGHT*0.8, manager)
    CreateUiButton("Configure the Rocket", WIDTH*0.45, HEIGHT*0.7, manager, WIDTH*0.1)
    CreateRocketImage(selectedNumber, manager)

def InitializeRocketConfigurationUI():
    CreateUiLabel("Rocket Configuration", WIDTH*0.7, HEIGHT*0.2, manager)
    CreateUiButton("Reset Configuration", WIDTH*0.8, HEIGHT*0.8, manager, length_x= WIDTH*0.1)
    CreateUiButton("Previous", WIDTH*0.38, HEIGHT*0.7, manager)
    CreateUiButton("Next", WIDTH*0.55, HEIGHT*0.7, manager)
    configPairs = GetTextsAndValuesForConfigUI()
    CreateUiTextBoxAndTextEntry(configPairs[0][1], configPairs[0][0], WIDTH*0.7, HEIGHT*0.3, manager)
    CreateUiTextBox(configPairs[1][1],WIDTH*0.7, HEIGHT*0.35, manager)
    CreateDropDown(planetNameArray,
                              planetNameArray.index(GetStartplanetName()),
                              WIDTH*0.8, HEIGHT*0.35, manager)
    CreateUiTextBoxAndTextEntry(configPairs[2][1], configPairs[2][0], WIDTH*0.7, HEIGHT*0.4, manager)
    CreateUiTextBoxAndTextEntry(configPairs[3][1], configPairs[3][0], WIDTH*0.7, HEIGHT*0.45, manager)
    CreateUiTextBoxAndTextEntry(configPairs[4][1], configPairs[4][0], WIDTH*0.7, HEIGHT*0.5, manager,size_x=WIDTH*0.03)
    CreateUiTextBoxAndTextEntry(configPairs[5][1], configPairs[5][0], WIDTH*0.7, HEIGHT*0.55, manager)
    CreateUiTextBoxAndTextEntry(configPairs[6][1], configPairs[6][0], WIDTH*0.2, HEIGHT*0.3, manager)
    CreateUiTextBoxAndTextEntry(configPairs[7][1], configPairs[7][0], WIDTH*0.2, HEIGHT*0.35, manager)
    CreateUiTextBoxAndTextEntry(configPairs[8][1], configPairs[8][0], WIDTH*0.2, HEIGHT*0.4, manager)
# removes all ui elements => no used object_ids
def ClearStartUI():
    manager.clear_and_reset() 

def ResetAndShowUI(selectedNumber):
    ClearStartUI()
    InitializeStartUI(selectedNumber)
    InitializeRocketConfigurationUI()
    
def ResetCurrentRocketConfig():
    currentJsonFile = open("./Globals/RocketConfig/CurrentRocketConfig.json", "w")
    standardJsonFile = open("./Globals/RocketConfig/StandardRocketConfig.json", "r")

    json.dump(json.load(standardJsonFile), currentJsonFile, indent=4, ensure_ascii=False)

    currentJsonFile.close()
    standardJsonFile.close()

def UpdateRocketConfigs(event):
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")
    newJson = keys.UpdateKeyInJsonRocket(json.load(jsonfile), event.ui_object_id, event.text)

    jsonfile.seek(0)
    jsonfile.truncate()
    json.dump(newJson, jsonfile, indent=4, ensure_ascii=False)
    jsonfile.close()

def GetSelectedRocket():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Image"]["selectedNumber"]

def GetStartplanetName():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Start"]["Startplanet"]["value"]

def UpdateSelectedRocket(selectedRocket):
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")
    
    config = json.load(jsonfile)
    config["Image"]["selectedNumber"] = selectedRocket

    jsonfile.seek(0)
    jsonfile.truncate()
    json.dump(config, jsonfile, indent=4, ensure_ascii=False)
    jsonfile.close()

def GetTextsAndValuesForConfigUI():
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r")
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



