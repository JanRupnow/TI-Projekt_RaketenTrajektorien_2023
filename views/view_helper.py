from variables.konstanten import *
from methods.support_methods import *
import pygame_gui as pg


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
                                             object_id = removeSpaces(hotkey[1]))
    TEXT_INPUT.length_limit = 1
    TEXT_INPUT.set_text(getStringOfAscii(hotkey[0]))
    
    return TEXT_BOX, TEXT_INPUT

def createUiTextBoxAndTextEntry(text, value, position_x, position_y, manager):
    TEXT_BOX = pg.elements.UITextBox(text,
                                     relative_rect= pygame.Rect((position_x,position_y),(WIDTH*0.1,HEIGHT*0.05)),
                                     manager = manager, 
                                     object_id=removeSpaces(text[1]+"_text"))
    
    TEXT_INPUT = pg.elements.UITextEntryLine(relative_rect= pygame.Rect((position_x+WIDTH*0.1,position_y), (WIDTH*0.03,HEIGHT*0.05)), 
                                             manager = manager, 
                                             object_id = removeSpaces(text))
    
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

def createUiButton(text, position_x,position_y, manager):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x,position_y), (WIDTH*0.07,HEIGHT*0.07)),
                                text=text,
                                manager=manager,
                                object_id=removeSpaces(text+"_button"))