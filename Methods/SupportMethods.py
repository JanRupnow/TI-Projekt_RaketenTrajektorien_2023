import pygame

def GetStringOfAscii(input):
    if input > 32 and input < 127:
        return chr(input).upper()
    else:
        return "a"

def CheckKeyDown(event, key):
    return event.type == pygame.KEYDOWN and event.key == key

def RemoveSpaces(textHotKey):
    return textHotKey.replace(" ", "")

def IsConvertibleToInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False