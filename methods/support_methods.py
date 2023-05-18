import pygame
def getStringOfAscii(input):
    return chr(input)

def checkKeyDown(event, key):
    return event.type == pygame.KEYDOWN and event.key == key