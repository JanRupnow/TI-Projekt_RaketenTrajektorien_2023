import pygame.mouse

import Globals.Hotkeys as Keys
from Globals.FlightData.FlightDataManager import DATA

from Views.ViewComponents import *

from Methods.JsonMethods import *
from Methods.ViewMethods import *

manager = pg.UIManager((WIDTH, HEIGHT))
UI_REFRESH_RATE = CLOCK.tick(60) / 1000
#https://getimg.ai/text-to-image
rocket_hall = pygame.image.load("Images/Rocket_Hall.png").convert_alpha()
rocket_hall = pygame.transform.scale(rocket_hall, (WIDTH, HEIGHT))


def show_start_ui():
    show_gui = True
    # Slider Box
    slider = None
    area_rect = pygame.Rect(WIDTH * 0.2, HEIGHT * 0.7, WIDTH * 0.15, 0.06 * HEIGHT)
    mouse_position = None
    show_configuration = False
    DATA.save_data = get_save_data()
    selected_number = get_selected_rocket()
    if len(manager.get_sprite_group()) < 4:
        initialize_start_ui(selected_number)
    while show_gui:
        WINDOW.blit(rocket_hall, (0, 0))
        if show_configuration:
            diplay_configuration_ui()
        display_basic_ui()
        for event in pygame.event.get():
            if event.type == pg.UI_HORIZONTAL_SLIDER_MOVED and event.ui_object_id == "crash_velocity_slider":
                mouse_position = pygame.mouse.get_pos()

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Start_button":
                show_gui = False
                if slider is not None:
                    change_crash_velocity(int(slider.get_current_value()))
                DATA.crash_velocity = get_crash_velocity()

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Configuration_button" \
                    and not show_configuration:
                slider = initialize_rocket_configuration_ui()
                show_configuration = True
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Reset_button":
                reset_current_rocket_config()
                slider = reset_and_show_ui(selected_number)
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Previous_button" and selected_number > 0:
                selected_number -= 1
                create_rocket_image(selected_number, manager)
                update_selected_rocket(selected_number)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "Next_button" and selected_number < 3:
                selected_number += 1
                update_selected_rocket(selected_number)
                create_rocket_image(selected_number, manager)
                slider = reset_and_show_ui(selected_number)
            if event.type == pg.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "startplanet_dropdown":
                update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)
            if event.type == pg.UI_DROP_DOWN_MENU_CHANGED and event.ui_object_id == "savedata_dropdown":
                update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)
                DATA.save_data = get_save_data()
            if check_key_down(event, Keys.h_close_window[0]):
                pygame.quit()
                sys.exit()
            if check_key_down(event, Keys.h_leave_simulation[0]):
                pygame.quit()
                sys.exit()
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startangle_input":
                if is_convertible_to_int(event.text):
                    if 360 > int(event.text) >= 0:
                        update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "flightangle_input":
                if is_convertible_to_int(event.text):
                    if 45 >= int(event.text) >= 0:
                        update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "startthrust_input":
                if is_convertible_to_int(event.text):
                    if 10 >= int(event.text) >= 0:
                        update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "rocketmass(t)_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) >= 0:
                        update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "fuelmass(t)_input":
                if is_convertible_to_int(event.text):
                    if int(event.text) >= 0:
                        update_rocket_configs(event)
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "year_input":
                if is_convertible_to_int(event.text):
                    if 3000 >= int(event.text) >= 0:
                        update_rocket_configs(event)
                        if check_date_is_legal(get_start_day(), get_start_month(), event.text):
                            update_rocket_configs(event)
                        else:
                            update_rocket_configs(event)
                            over_write_standard_day()
                slider = reset_and_show_ui(selected_number)
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "month_input":
                if is_convertible_to_int(event.text):
                    if 12 >= int(event.text) > 0:
                        if check_date_is_legal(get_start_day(), event.text, get_start_year()):
                            update_rocket_configs(event)
                        else:
                            update_rocket_configs(event)
                            over_write_standard_day()
                slider = reset_and_show_ui(selected_number)

            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "day_input":
                if is_convertible_to_int(event.text):
                    if get_start_month() in [1, 3, 5, 7, 8, 10, 12]:
                        if 31 >= int(event.text) > 0:
                            update_rocket_configs(event)
                    elif get_start_month() in [4, 6, 9, 11]:
                        if 30 >= int(event.text) > 0:
                            update_rocket_configs(event)
                    elif get_start_year() % 4 != 0:
                        if 28 >= int(event.text) > 0:
                            update_rocket_configs(event)
                    else:
                        if 29 >= int(event.text) > 0:
                            update_rocket_configs(event)
                reset_and_show_ui(selected_number)

            if mouse_position != None and not area_rect.collidepoint(pygame.mouse.get_pos()):
                change_crash_velocity(int(slider.get_current_value()))
                slider = reset_and_show_ui(selected_number)
                mouse_position = None

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()

    clear_start_ui()


def display_basic_ui():
    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.39, HEIGHT * 0.08, WIDTH * 0.22, HEIGHT * 0.075))
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.39 + 1, HEIGHT * 0.08 + 1, WIDTH * 0.22 - 2, HEIGHT * 0.075 - 2))

    title_text = TITLE_FONT_1.render("Spaceflight Simulator", True, (0, 150, 150))
    WINDOW.blit(title_text, (WIDTH * 0.405, HEIGHT * 0.1))

    # Background Image
    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.45, HEIGHT * 0.315, WIDTH * 0.1, HEIGHT * 0.37))
    pygame.draw.rect(WINDOW, (50, 50, 50),
                     (WIDTH * 0.45 + 1, HEIGHT * 0.315 + 1, WIDTH * 0.1 - 2, HEIGHT * 0.37 - 2))


def diplay_configuration_ui():
    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.18, HEIGHT * 0.24, WIDTH * 0.19, HEIGHT * 0.235))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.18 + 1, HEIGHT * 0.24 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.235 - 2))
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.18 + 1, HEIGHT * 0.24 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.05 - 2))

    title_text = TITLE_FONT_1.render("Simulation Time", True, (0, 150, 150))
    WINDOW.blit(title_text, (WIDTH * 0.2, HEIGHT * 0.25))

    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.18, HEIGHT * 0.54, WIDTH * 0.19, HEIGHT * 0.235))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.18 + 1, HEIGHT * 0.54 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.235 - 2))
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.18 + 1, HEIGHT * 0.54 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.05 - 2))

    title_text = TITLE_FONT_1.render("Generals", True, (0, 150, 150))
    WINDOW.blit(title_text, (WIDTH * 0.2, HEIGHT * 0.55))

    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.685, HEIGHT * 0.24, WIDTH * 0.25, HEIGHT * 0.39))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.685 + 1, HEIGHT * 0.24 + 1, WIDTH * 0.25 - 2, HEIGHT * 0.39 - 2))
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.685 + 1, HEIGHT * 0.24 + 1, WIDTH * 0.25 - 2, HEIGHT * 0.05 - 2))

    rocket_config_text = TITLE_FONT_1.render("Rocket Configuration", True, (0, 150, 150))
    WINDOW.blit(rocket_config_text, (WIDTH * 0.715, HEIGHT * 0.25))


def initialize_start_ui(selected_number: int = 0):
    create_ui_button("Start", WIDTH * 0.465, HEIGHT * 0.8, manager)
    create_ui_button("Configuration", WIDTH * 0.45, HEIGHT * 0.7, manager, WIDTH * 0.1)
    create_rocket_image(selected_number, manager)


def initialize_rocket_configuration_ui() -> pg.elements.UIHorizontalSlider:
    create_ui_button("Reset", WIDTH * 0.8, HEIGHT * 0.8, manager, length_x=WIDTH * 0.1)
    create_ui_button("Previous", WIDTH * 0.38, HEIGHT * 0.7, manager)
    create_ui_button("Next", WIDTH * 0.55, HEIGHT * 0.7, manager)
    config_pairs = get_texts_and_values_for_config_ui()

    create_ui_text_box_and_text_entry(config_pairs[7][1], config_pairs[7][0], WIDTH * 0.2, HEIGHT * 0.3, manager,
                                      length=4)
    create_ui_text_box_and_text_entry(config_pairs[8][1], config_pairs[8][0], WIDTH * 0.2, HEIGHT * 0.35, manager,
                                      length=2)
    create_ui_text_box_and_text_entry(config_pairs[9][1], config_pairs[9][0], WIDTH * 0.2, HEIGHT * 0.4, manager,
                                      length=2)

    create_ui_text_box(config_pairs[4][1], WIDTH * 0.2, HEIGHT * 0.6, manager)
    list_bools = ["True", "False"]
    create_bool_drop_down(list_bools,
                          list_bools.index(str(get_save_data())),
                          WIDTH * 0.3, HEIGHT * 0.6, manager, length=WIDTH * 0.06)
    create_ui_text_box("crash velocity: ", WIDTH * 0.2, HEIGHT * 0.65, manager)
    create_ui_text_box(f"{get_crash_velocity()} m/s", WIDTH * 0.3, HEIGHT * 0.65, manager, length=0.06 * WIDTH)

    slider = create_ui_slider(WIDTH * 0.2, HEIGHT * 0.7, manager, length_x=WIDTH * 0.15,
                              length_y=0.06 * HEIGHT)

    create_ui_text_box_and_text_entry(config_pairs[0][1], config_pairs[0][0], WIDTH * 0.7, HEIGHT * 0.3, manager,
                                      length=3)
    create_ui_text_box(config_pairs[1][1], WIDTH * 0.7, HEIGHT * 0.35, manager)
    create_drop_down(planetNameArray,
                     planetNameArray.index(get_startplanet_name()),
                     WIDTH * 0.8, HEIGHT * 0.35, manager)
    create_ui_text_box_and_text_entry(config_pairs[2][1], config_pairs[2][0], WIDTH * 0.7, HEIGHT * 0.4, manager,
                                      length=3)
    create_ui_text_box_and_text_entry(config_pairs[3][1], config_pairs[3][0], WIDTH * 0.7, HEIGHT * 0.45, manager,
                                      length=2)
    create_ui_text_box_and_text_entry(config_pairs[6][1], config_pairs[6][0], WIDTH * 0.7, HEIGHT * 0.5, manager,
                                      length=10, length_entry=WIDTH * 0.07)
    create_ui_text_box_and_text_entry(config_pairs[5][1], config_pairs[5][0], WIDTH * 0.7, HEIGHT * 0.55, manager,
                                      length=10, length_entry=WIDTH * 0.07)
    return slider

# removes all ui elements => no used object_ids
def clear_start_ui():
    manager.clear_and_reset()


def reset_and_show_ui(selected_number) -> pg.elements.UIHorizontalSlider:
    clear_start_ui()
    initialize_start_ui(selected_number)
    slider = initialize_rocket_configuration_ui()
    return slider


def reset_current_rocket_config():
    current_json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json", "w")
    standard_json_file = open("./Globals/RocketConfig/StandardRocketConfig.json", "r")

    json.dump(json.load(standard_json_file), current_json_file, indent=4, ensure_ascii=False)

    current_json_file.close()
    standard_json_file.close()


def update_rocket_configs(event):
    json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")
    new_json = Keys.update_key_in_json_rocket(json.load(json_file), event.ui_object_id, event.text)

    json_file.seek(0)
    json_file.truncate()
    json.dump(new_json, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def get_selected_rocket():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Image"]["selectedNumber"]


def get_startplanet_name():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Start"]["Startplanet"]["value"]


def get_save_data():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Start"]["SaveData"]["value"]


def get_crash_velocity():
    return json.load(open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+"))["Start"]["CrashVelocity"]


def change_crash_velocity(value: int):
    json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")

    config = json.load(json_file)
    config["Start"]["CrashVelocity"] = value

    json_file.seek(0)
    json_file.truncate()
    json.dump(config, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def update_selected_rocket(selected_rocket):
    json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")

    config = json.load(json_file)
    config["Image"]["selectedNumber"] = selected_rocket

    json_file.seek(0)
    json_file.truncate()
    json.dump(config, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def get_texts_and_values_for_config_ui():
    json_file = open("./Globals/RocketConfig/CurrentRocketConfig.json", "r")
    config = json.load(json_file)

    config_pairs = []

    for category in config.keys():
        try:
            for key in config[category].keys():
                config_pairs.append((config[category][key]["value"], config[category][key]["text"]))
        except:
            pass

    json_file.close()
    return config_pairs


def create_ui_slider(position_x, position_y, manager, length_x=WIDTH * 0.07,
                     length_y=HEIGHT * 0.07) -> pg.elements.UIHorizontalSlider:
    slider = pg.elements.UIHorizontalSlider(relative_rect=pygame.Rect((position_x, position_y), (length_x, length_y)),
                                            start_value=get_crash_velocity(),
                                            value_range=(100, 1000),
                                            manager=manager,
                                            object_id="crash_velocity_slider")
    return slider
