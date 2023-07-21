import pygame_gui as pg
import json

from Globals.Constants import *

from Methods.SupportMethods import *


def CreateUiLabel(text, position_x, position_y, manager, size_x = WIDTH*0.1):
    return pg.elements.UILabel(relative_rect=pygame.Rect((position_x,position_y), (size_x,HEIGHT*0.05)),
                               text=text,
                               manager=manager,
                               object_id=RemoveSpaces(text+"_label"))

def CreateUiTextBoxAndTextEntryHotkey(hotkey,position_x, position_y, manager, mutable= True, entryText = None):
    TEXT_BOX = pg.elements.UITextBox(hotkey[1],
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=RemoveSpaces(hotkey[1]+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1,position_y), (WIDTH*0.03,HEIGHT*0.05)), 
                                             manager = manager, 
                                             object_id = RemoveSpaces(hotkey[1] + "_text") if mutable else RemoveSpaces(hotkey[1] + "_notMutable"))
    TEXT_INPUT.length_limit = 1 if entryText == None else len(entryText)
    TEXT_INPUT.set_text(GetStringOfAscii(hotkey[0])if entryText == None else entryText)
    
    return TEXT_BOX, TEXT_INPUT

def GetRocketImgage(rocketImageNumber):
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    img = pygame.image.load(config["Image"]["path"][rocketImageNumber])
    return pygame.transform.scale_by(img, 300/img.get_height())

def CreateRocketImage(rocketImageNumber,manager, position_x = WIDTH*0.5, position_y = HEIGHT*0.5) -> pg.elements.UIImage:
    for element in manager.root_container.elements:
                    if "rocket_image" in element.get_object_ids():
                        element.kill()
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    img = pygame.image.load(config["Image"]["path"][rocketImageNumber])
    img = pygame.transform.scale_by(img, 300/img.get_height())
    image_rect = img.get_rect()
    image_rect.topleft = (position_x -  img.get_width()/2, position_y - img.get_height()/2)
    return pg.elements.UIImage(relative_rect=image_rect, image_surface=img, manager=manager, object_id = "rocket_image")

def CreateUiTextBoxAndTextEntry(text, value, position_x, position_y, manager, size_x=0, size_y=0):
    TEXT_BOX = pg.elements.UITextBox(text,
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1+size_x,size_y+HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=RemoveSpaces(text+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1+size_x,position_y), (WIDTH*0.03+size_x,HEIGHT*0.05+size_y)), 
                                             manager = manager, 
                                             object_id = RemoveSpaces(text+"_input"))
    
    TEXT_INPUT.set_text(str(value))

    return TEXT_BOX, TEXT_INPUT

def CreateDropDown(array,defaultnumber,position_x,position_y,manager):
    DROP_DOWN = pg.elements.UIDropDownMenu(array,array[defaultnumber],relative_rect=pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id="startplanet_dropdown",
                                     )
    return DROP_DOWN
def CreateUiTextBox(text, position_x, position_y, manager):
    TEXT_BOX = pg.elements.UITextBox(text,
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=RemoveSpaces(text[1]+"_text"))
    return TEXT_BOX

def CreateUiSettingsTopicLabel(text, position_x, position_y, manager, size_x = WIDTH*0.1):
    label = CreateUiLabel(text, position_x, position_y, manager, size_x)
    label.text_horiz_alignment = "left"
    label.text_colour = "red"
    label.rebuild()
    return label

def CreateUiGameTitleLabel(text, position_x, position_y, manager):
    label = CreateUiLabel(text, position_x, position_y, manager)
    label.text_horiz_alignment = "center"
    label.text_colour = "green"
    label.set_text_scale(15)
    label.rebuild()
    return label

def CreateUiButton(text, position_x,position_y, manager, length_x = WIDTH*0.07, length_y= HEIGHT*0.07):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x,position_y), (length_x,length_y)),
                                text=text,
                                manager=manager,
                                object_id=RemoveSpaces(text+"_button"))
    
