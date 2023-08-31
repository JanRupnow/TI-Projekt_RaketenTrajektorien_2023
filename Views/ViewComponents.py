import pygame_gui
import pygame_gui as pg
import json

from Globals.Constants import *

from Methods.SupportMethods import *


def create_ui_label(text, position_x, position_y, manager, size_x=WIDTH * 0.15,
                    size_y=HEIGHT * 0.1) -> pg.elements.UILabel:
    return pg.elements.UILabel(relative_rect=pygame.Rect((position_x, position_y), (size_x, size_y)),
                               text=text,
                               manager=manager,
                               object_id=remove_spaces(text + "_label"))


def create_ui_text_box_and_text_entry_hotkey(hotkey, position_x, position_y, manager, mutable=True,
                                             entry_text=None) -> (pg.elements.UITextBox, pg.elements.UITextEntryLine):
    text_box = pg.elements.UITextBox(hotkey[1],
                                     relative_rect=pygame.Rect((position_x, position_y), (WIDTH * 0.1, HEIGHT * 0.05)),
                                     manager=manager,
                                     object_id=remove_spaces(hotkey[1] + "_text"))
    text_input = pg.elements.UITextEntryLine(relative_rect=pygame.Rect((position_x + WIDTH * 0.1, position_y),
                                                                       (WIDTH * 0.04, HEIGHT * 0.05)),
                                             manager=manager,
                                             object_id=remove_spaces(hotkey[1] + "_input"))
    text_input.length_limit = 1 if entry_text is None else len(entry_text)
    text_input.is_enabled = mutable
    text_input.set_text(get_string_of_ascii(hotkey[0]) if entry_text is None else entry_text)

    return text_box, text_input


def create_rocket_image(rocket_image_number: int, manager: pygame_gui.UIManager, position_x=WIDTH * 0.5,
                        position_y=HEIGHT * 0.5) -> pg.elements.UIImage:
    for element in manager.root_container.elements:
        if "rocket_image" in element.get_object_ids():
            element.kill()
    json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(json_file)
    img = pygame.image.load(config["Image"]["path"][rocket_image_number]).convert_alpha()
    img = pygame.transform.scale_by(img, 300 / img.get_height())
    image_rect = img.get_rect()
    image_rect.topleft = (position_x - img.get_width() / 2, position_y - img.get_height() / 2)
    image = pg.elements.UIImage(relative_rect=image_rect,
                                image_surface=img, manager=manager, object_id="rocket_image")
    return image


def create_ui_text_box_and_text_entry(text, value, position_x, position_y, manager, size_x=0, size_y=0, length=20) -> (
pg.elements.UITextBox, pg.elements.UITextEntryLine):
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
    # We only use numeric inputs
    text_input.set_allowed_characters("numbers")
    text_input.set_text_length_limit(length)
    return text_box, text_input


def create_drop_down(array, defaultnumber, position_x, position_y, manager, length = WIDTH * 0.1, height = HEIGHT * 0.05) -> pg.elements.UIDropDownMenu:
    drop_down = pg.elements.UIDropDownMenu(array, array[defaultnumber],
                                           relative_rect=pygame.Rect((position_x, position_y),
                                                                     (length, height)),
                                           manager=manager,
                                           object_id="startplanet_dropdown",
                                           )
    return drop_down


def create_bool_drop_down(array, defaultnumber, position_x, position_y, manager, length = WIDTH * 0.1, height = HEIGHT * 0.05) -> pg.elements.UIDropDownMenu:
    drop_down = pg.elements.UIDropDownMenu(array, array[defaultnumber],
                                           relative_rect=pygame.Rect((position_x, position_y),
                                                                     (length, height)),
                                           manager=manager,
                                           object_id="savedata_dropdown",
                                           )
    return drop_down


def create_ui_text_box(text, position_x, position_y, manager) -> pg.elements.UITextBox:
    text_box = pg.elements.UITextBox(text,
                                     relative_rect=pygame.Rect((position_x, position_y), (WIDTH * 0.1, HEIGHT * 0.05)),
                                     manager=manager,
                                     object_id=remove_spaces(text[1] + "_text"))
    return text_box


def create_ui_button(text, position_x, position_y, manager, length_x=WIDTH * 0.07,
                     length_y=HEIGHT * 0.07) -> pg.elements.UIButton:
    button = pg.elements.UIButton(relative_rect=pygame.Rect((position_x, position_y), (length_x, length_y)),
                                  text=text,
                                  manager=manager,
                                  object_id=remove_spaces(text + "_button"))
    return button
