import pygame

def getStringOfAscii(input):
    if input > 32 and input < 127:
        return chr(input).upper()
    else:
        return "a"

def checkKeyDown(event, key):
    return event.type == pygame.KEYDOWN and event.key == key

def removeSpaces(textHotKey):
    return textHotKey.replace(" ", "")