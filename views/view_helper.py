from variables.konstanten import *
from methods.support_methods import *
import pygame_gui as pg
import json


def createUiLabel(text, position_x, position_y, manager):
    return pg.elements.UILabel(relative_rect=pygame.Rect((position_x,position_y), (WIDTH*0.1,HEIGHT*0.05)),
                               text=text,
                               manager=manager,
                               object_id=removeSpaces(text+"_label"))

def createUiTextBoxAndTextEntryHotkey(hotkey,position_x, position_y, manager):
    TEXT_BOX = pg.elements.UITextBox(hotkey[1],
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=removeSpaces(hotkey[1]+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1,position_y), (WIDTH*0.03,HEIGHT*0.05)), 
                                             manager = manager, 
                                             object_id = removeSpaces(hotkey[1]+"_input"))
    TEXT_INPUT.length_limit = 1
    TEXT_INPUT.set_text(getStringOfAscii(hotkey[0]))
    
    return TEXT_BOX, TEXT_INPUT

def createRocketImage(rocketImageNumber,manager, position_x = WIDTH*0.5, position_y = HEIGHT*0.5):
    jsonfile = open("./variables/rocket_config/current_rocket_config.json")
    config = json.load(jsonfile)
    img = pygame.image.load(config["Image"]["path"][rocketImageNumber])
    img = pygame.transform.scale_by(img, 300/img.get_height())
    image_rect = img.get_rect()
    image_rect.topleft = (position_x -  img.get_width()/2, position_y - img.get_height()/2)
    pg.elements.UIImage(relative_rect=image_rect, image_surface=img, manager=manager, object_id = "rocket_image")

def createUiTextBoxAndTextEntry(text, value, position_x, position_y, manager):
    TEXT_BOX = pg.elements.UITextBox(text,
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=removeSpaces(text[1]+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1,position_y), (WIDTH*0.03,HEIGHT*0.05)), 
                                             manager = manager, 
                                             object_id = removeSpaces(text+"_input"))
    
    TEXT_INPUT.set_text(str(value))

    return TEXT_BOX, TEXT_INPUT


def createUiSettingsTopicLabel(text, position_x, position_y, manager):
    label = createUiLabel(text, position_x, position_y, manager)
    label.text_horiz_alignment = "left"
    label.text_colour = "red"
    label.rebuild()
    return label

def createUiGameTitleLabel(text, position_x, position_y, manager):
    label = createUiLabel(text, position_x, position_y, manager)
    label.text_horiz_alignment = "center"
    label.text_colour = "green"
    label.set_text_scale(15)
    label.rebuild()
    return label

def createUiButton(text, position_x,position_y, manager, length_x = WIDTH*0.07, length_y= HEIGHT*0.07):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x,position_y), (length_x,length_y)),
                                text=text,
                                manager=manager,
                                object_id=removeSpaces(text+"_button"))
