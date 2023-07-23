import sys

import Globals.Hotkeys as Keys

from Views.ViewComponents import *

from Methods.JsonMethods import *
from Methods.ViewMethods import *

manager = pg.UIManager((WIDTH, HEIGHT))
UI_REFRESH_RATE = CLOCK.tick(60) / 1000


def change_hot_key_from_input(event, hotkey):
    if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == remove_spaces(hotkey[1] + "_input") \
            and event.text != "":
        jsonfile = open("./variables/hotkeys_config/current_hotkeys.json", "r+")
        hotkey[0] = ord(event.text)
        new_json = Keys.update_key_in_json(json.load(jsonfile), hotkey)

        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(new_json, jsonfile, indent=4, ensure_ascii=False)
    return hotkey[0]


def change_all_hot_keys_from_input(event, hotkeys):
    for hotkey in hotkeys:
        hotkey[0] = change_hot_key_from_input(event, hotkey)


def create_ui_close_button():
    label = create_ui_button("Close Settings", 0, 0, manager)
    return label


def create_ui_settings_title_label():
    title_label = create_ui_label("Settings", WIDTH * 0.45, 0.15 * HEIGHT, manager)
    title_label.text_horiz_alignment = "center"
    title_label.rebuild()
    return title_label


def clear_settings_ui():
    manager.clear_and_reset()


def initialize_settings_ui():
    create_ui_settings_title_label()
    create_ui_close_button()
    create_ui_button("Reset Controls", WIDTH * 0.9, HEIGHT * 0.9, manager)
    create_ui_game_title_label("Spaceflight Simulator", WIDTH * 0.45, HEIGHT * 0.05, manager)
    create_ui_settings_topic_label("General Controls (not mutable)", WIDTH * 0.1, HEIGHT * 0.15, manager, WIDTH * 0.12)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_display_hot_keys, WIDTH * 0.1, HEIGHT * 0.2, manager, False, "6")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_leave_simulation, WIDTH * 0.1, HEIGHT * 0.25, manager, False, "X")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_open_settings, WIDTH * 0.1, HEIGHT * 0.3, manager, False, "F1")
    create_ui_settings_topic_label("Rocket Controls", WIDTH * 0.1, HEIGHT * 0.35, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_forward, WIDTH * 0.1, HEIGHT * 0.4, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_left, WIDTH * 0.1, HEIGHT * 0.45, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_right, WIDTH * 0.1, HEIGHT * 0.5, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_lower_rocket_boost, WIDTH * 0.1, HEIGHT * 0.55, manager)
    create_ui_settings_topic_label("Zoom Controls", WIDTH * 0.1, HEIGHT * 0.6, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.H_zoomAutoOnReferencePlanet, WIDTH * 0.1, HEIGHT * 0.65, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_start, WIDTH * 0.1, HEIGHT * 0.7, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_planet, WIDTH * 0.1, HEIGHT * 0.75, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_planet_system, WIDTH * 0.1, HEIGHT * 0.8, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_auto_on_rocket, WIDTH * 0.1, HEIGHT * 0.85, manager)
    create_ui_settings_topic_label("Navigation Controls (not mutable)", WIDTH * 0.7, HEIGHT * 0.15, manager, WIDTH * 0.15)
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenUp, WIDTH * 0.7, HEIGHT * 0.2, manager, False, "UP")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenLeft, WIDTH * 0.7, HEIGHT * 0.25, manager, False, "LEFT")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenRight, WIDTH * 0.7, HEIGHT * 0.3, manager, False, "RIGHT")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenDown, WIDTH * 0.7, HEIGHT * 0.35, manager, False, "DOWN")
    create_ui_settings_topic_label("Display Controls", WIDTH * 0.7, HEIGHT * 0.4, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_pause_simulation, WIDTH * 0.7, HEIGHT * 0.45, manager, False, "SPACE")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_draw_line, WIDTH * 0.7, HEIGHT * 0.5, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_show_distance, WIDTH * 0.7, HEIGHT * 0.55, manager)
    create_ui_settings_topic_label("Time Controls", WIDTH * 0.7, HEIGHT * 0.6, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_shift_time_step_up, WIDTH * 0.7, HEIGHT * 0.65, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_shift_time_step_down, WIDTH * 0.7, HEIGHT * 0.7, manager)
    create_ui_settings_topic_label("Center Controls", WIDTH * 0.7, HEIGHT * 0.75, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_center_on_rocket, WIDTH * 0.7, HEIGHT * 0.8, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_center_on_sun, WIDTH * 0.7, HEIGHT * 0.85, manager)


def show_settings_ui():
    if len(manager.get_sprite_group()) < 4:
        initialize_settings_ui()

    show_gui = True

    while show_gui:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "CloseSettings_button":
                show_gui = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_button":
                Keys.reset_overwrite_current()
                manager.clear_and_reset()
                initialize_settings_ui()
            if check_key_down(event, Keys.h_close_window[0]):
                show_gui = False
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id.endswith("_notMutable"):
                manager.clear_and_reset()
                initialize_settings_ui()
            if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id.endswith("_input"):
                if event.text != "":
                    if 32 < ord(event.text) < 127:
                        change_all_hot_keys_from_input(event, Keys.list_hot_keys)
                manager.clear_and_reset()
                initialize_settings_ui()
            if check_key_down(event, Keys.h_leave_simulation[0]):
                pygame.quit()
                sys.exit()
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(WINDOW)
        pygame.display.update()

    clear_settings_ui()
