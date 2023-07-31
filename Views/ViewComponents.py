
import pygame_gui as pg

from Globals.Constants import *

from Methods.SupportMethods import *


def create_ui_label(text, position_x, position_y, manager, size_x=WIDTH * 0.15, size_y=HEIGHT*0.1):
    return pg.elements.UILabel(relative_rect=pygame.Rect((position_x, position_y), (size_x, size_y)),
                               text=text,
                               manager=manager,
                               object_id=remove_spaces(text + "_label"))


def create_ui_text_box_and_text_entry_hotkey(hotkey, position_x, position_y, manager, mutable=True, entry_text=None):
    text_box = pg.elements.UITextBox(hotkey[1],
                                     relative_rect=pygame.Rect((position_x, position_y), (WIDTH * 0.1, HEIGHT * 0.05)),
                                     manager=manager,
                                     object_id=remove_spaces(hotkey[1] + "_text"))

    text_input = pg.elements.UITextEntryLine(relative_rect=pygame.Rect((position_x + WIDTH * 0.1, position_y),
                                                                       (WIDTH * 0.04, HEIGHT * 0.05)),
                                             manager=manager,
                                             object_id=remove_spaces(hotkey[1] + "_text") if mutable else remove_spaces(
                                                 hotkey[1] + "_notMutable"))
    text_input.length_limit = 1 if entry_text is None else len(entry_text)
    text_input.set_text(get_string_of_ascii(hotkey[0]) if entry_text is None else entry_text)

    return text_box, text_input


def get_rocket_imgage(rocket_image_number):
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    img = pygame.image.load(config["Image"]["path"][rocket_image_number]).convert_alpha()
    return pygame.transform.scale_by(img, 300 / img.get_height())


def create_rocket_image(rocket_image_number, manager, position_x=WIDTH * 0.5,
                        position_y=HEIGHT * 0.5) -> pg.elements.UIImage:
    for element in manager.root_container.elements:
        if "rocket_image" in element.get_object_ids():
            element.kill()
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    img = pygame.image.load(config["Image"]["path"][rocket_image_number]).convert_alpha()
    img = pygame.transform.scale_by(img, 300 / img.get_height())
    image_rect = img.get_rect()
    image_rect.topleft = (position_x - img.get_width() / 2, position_y - img.get_height() / 2)
    return pg.elements.UIImage(relative_rect=image_rect, image_surface=img, manager=manager, object_id="rocket_image")


def create_ui_text_box_and_text_entry(text, value, position_x, position_y, manager, size_x=0, size_y=0):
    text_box = pg.elements.UITextBox(text,
                                     relative_rect=pygame.Rect((position_x, position_y),
                                                               (WIDTH * 0.1 + size_x, size_y + HEIGHT * 0.05)),
                                     manager=manager,
                                     object_id=remove_spaces(text + "_text"))

    text_input = pg.elements.UITextEntryLine(relative_rect=pygame.Rect((position_x + WIDTH * 0.1 + size_x, position_y),
                                                                       (WIDTH * 0.04 + size_x, HEIGHT * 0.05 + size_y)),
                                             manager=manager,
                                             object_id=remove_spaces(text + "_input"))

    text_input.set_text(str(value))

    return text_box, text_input


def create_drop_down(array, defaultnumber, position_x, position_y, manager):
    drop_down = pg.elements.UIDropDownMenu(array, array[defaultnumber],
                                           relative_rect=pygame.Rect((position_x, position_y),
                                                                     (WIDTH * 0.1, HEIGHT * 0.05)),
                                           manager=manager,
                                           object_id="startplanet_dropdown",
                                           )
    return drop_down


def create_ui_text_box(text, position_x, position_y, manager):
    text_box = pg.elements.UITextBox(text,
                                     relative_rect=pygame.Rect((position_x, position_y), (WIDTH * 0.1, HEIGHT * 0.05)),
                                     manager=manager,
                                     object_id=remove_spaces(text[1] + "_text"))
    return text_box


def create_ui_settings_topic_label(text, position_x, position_y, manager, size_x=WIDTH * 0.1):
    label = create_ui_label(text, position_x, position_y, manager, size_x)
    label.text_horiz_alignment = "left"
    label.text_colour = "red"
    label.rebuild()
    return label


def create_ui_game_title_label(text, position_x, position_y, manager, color="green"):
    label = create_ui_label(text, position_x, position_y, manager)
    label.text_horiz_alignment = "center"
    label.text_colour = color
    label.set_text_scale(15)
    label.rebuild()
    return label


def create_ui_button(text, position_x, position_y, manager, length_x=WIDTH * 0.07, length_y=HEIGHT * 0.07):
    return pg.elements.UIButton(relative_rect=pygame.Rect((position_x, position_y), (length_x, length_y)),
                                text=text,
                                manager=manager,
                                object_id=remove_spaces(text + "_button"))
