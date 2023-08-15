import Globals.Hotkeys as Keys

from Views.ViewComponents import *

from Methods.JsonMethods import *
from Methods.ViewMethods import *

manager = pg.UIManager((WIDTH, HEIGHT))
UI_REFRESH_RATE = CLOCK.tick(60) / 1000

settings_font_title = pygame.font.SysFont("Trebuchet MS", 22)
settings_font_header = pygame.font.SysFont("Trebuchet MS", 16)
rocket_background_img = pygame.image.load("Images/Rocket_Background_Image.png").convert_alpha()
rocket_background_img = pygame.transform.scale(rocket_background_img, (WIDTH, HEIGHT))


def change_hot_key_from_input(event: pygame.event, hotkey) -> str:
    if event.type == pg.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == remove_spaces(hotkey[1] + "_input") \
            and event.text != "":
        json_file = open("./variables/hotkeys_config/current_hotkeys.json", "r+")
        hotkey[0] = ord(event.text)
        new_json = Keys.update_key_in_json(json.load(json_file), hotkey)

        json_file.seek(0)
        json_file.truncate()
        json.dump(new_json, json_file, indent=4, ensure_ascii=False)
    return hotkey[0]


def change_all_hot_keys_from_input(event: pygame.event, hotkeys):
    for hotkey in hotkeys:
        hotkey[0] = change_hot_key_from_input(event, hotkey)


def initialize_settings_ui():
    create_ui_button("Close Settings (ESC)", 0, 0, manager, length_x=WIDTH * 0.12 - 1, length_y=0.08 * HEIGHT - 1)
    create_ui_button("Reset Controls", WIDTH * 0.88 + 1 , 0, manager, length_x=WIDTH * 0.12 - 1,
                     length_y=HEIGHT * 0.08 - 1)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_switch_interface, WIDTH * 0.1, HEIGHT * 0.2, manager, False, "Q")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_leave_simulation, WIDTH * 0.1, HEIGHT * 0.25, manager, False, "X")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_open_settings, WIDTH * 0.1, HEIGHT * 0.3, manager, False, "F1")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_forward, WIDTH * 0.1, HEIGHT * 0.4, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_left, WIDTH * 0.1, HEIGHT * 0.45, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_lower_rocket_boost, WIDTH * 0.1, HEIGHT * 0.5, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_rocket_boost_right, WIDTH * 0.1, HEIGHT * 0.55, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_auto_on_rocket, WIDTH * 0.1, HEIGHT * 0.65, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.H_zoomAutoOnReferencePlanet, WIDTH * 0.1, HEIGHT * 0.7, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_start, WIDTH * 0.1, HEIGHT * 0.75, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_planet, WIDTH * 0.1, HEIGHT * 0.8, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_zoom_rocket_planet_system, WIDTH * 0.1, HEIGHT * 0.85, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenUp, WIDTH * 0.75, HEIGHT * 0.2, manager, False, "UP")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenLeft, WIDTH * 0.75, HEIGHT * 0.25, manager, False, "LEFT")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenRight, WIDTH * 0.75, HEIGHT * 0.3, manager, False,
                                             "RIGHT")
    create_ui_text_box_and_text_entry_hotkey(Keys.H_moveScreenDown, WIDTH * 0.75, HEIGHT * 0.35, manager, False, "DOWN")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_pause_simulation, WIDTH * 0.75, HEIGHT * 0.45, manager, False,
                                             "SPACE")
    create_ui_text_box_and_text_entry_hotkey(Keys.h_draw_line, WIDTH * 0.75, HEIGHT * 0.5, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_show_distance, WIDTH * 0.75, HEIGHT * 0.55, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_shift_time_step_down, WIDTH * 0.75, HEIGHT * 0.65, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_shift_time_step_up, WIDTH * 0.75, HEIGHT * 0.7, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_center_on_rocket, WIDTH * 0.75, HEIGHT * 0.8, manager)
    create_ui_text_box_and_text_entry_hotkey(Keys.h_center_on_sun, WIDTH * 0.75, HEIGHT * 0.85, manager)


def display_ui_text_and_backgrounds():
    # Button Backgrounds
    pygame.draw.rect(WINDOW, (0, 0, 0), (0, 0, WIDTH * 0.12, HEIGHT * 0.08))
    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.88, 0, WIDTH * 0.12, HEIGHT * 0.08))
    # Title Background
    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.4, HEIGHT * 0.04, WIDTH * 0.16, HEIGHT * 0.05))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.4 + 1, HEIGHT * 0.04 + 1, WIDTH * 0.16 - 2, HEIGHT * 0.05 - 2))

    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.44, HEIGHT * 0.09, WIDTH * 0.08, HEIGHT * 0.05))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.44 + 1, HEIGHT * 0.09 + 1, WIDTH * 0.08 - 2, HEIGHT * 0.05 - 2))

    # Hotkey Bars
    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.085, HEIGHT * 0.15, WIDTH * 0.17, HEIGHT * 0.775))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.085 + 1, HEIGHT * 0.15 + 1, WIDTH * 0.17 - 2, HEIGHT * 0.775 - 2))

    pygame.draw.rect(WINDOW, (0, 0, 0), (WIDTH * 0.725, HEIGHT * 0.15, WIDTH * 0.19, HEIGHT * 0.775))
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH * 0.725 + 1, HEIGHT * 0.15 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.775 - 2))

    general_controls_text = settings_font_title.render("Spaceflight Simulator", True, (0, 150, 150))
    WINDOW.blit(general_controls_text, (WIDTH * 0.415, HEIGHT * 0.05))

    general_controls_text = settings_font_title.render("Settings", True, (0, 150, 150))
    WINDOW.blit(general_controls_text, (WIDTH * 0.455, HEIGHT * 0.1))

    # Left Topic Background N1
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.085 + 1, HEIGHT * 0.15 + 1, WIDTH * 0.17 - 2, HEIGHT * 0.0525 - 2))
    general_controls_text = settings_font_header.render("General Controls (not mutable)", True, (0, 150, 150))
    WINDOW.blit(general_controls_text, (WIDTH * 0.1, HEIGHT * 0.175))
    # Left Topic Background N2
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.085 + 1, HEIGHT * 0.35 + 1, WIDTH * 0.17 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Rocket Controls", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.1, HEIGHT * 0.375))
    # Left Topic Background N3
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.085 + 1, HEIGHT * 0.6 + 1, WIDTH * 0.17 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Zoom Controls", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.1, HEIGHT * 0.625))

    # Right Topic Background N1
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.725 + 1, HEIGHT * 0.15 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Navigation Controls (not mutable)", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.75, HEIGHT * 0.175))

    # Right Topic Background N1
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.725 + 1, HEIGHT * 0.4 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Display Controls", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.75, HEIGHT * 0.425))

    # Right Topic Background N1
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.725 + 1, HEIGHT * 0.6 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Time Controls", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.75, HEIGHT * 0.625))

    # Right Topic Background N1
    pygame.draw.rect(WINDOW, (100, 100, 100),
                     (WIDTH * 0.725 + 1, HEIGHT * 0.75 + 1, WIDTH * 0.19 - 2, HEIGHT * 0.0525 - 2))
    rocket_controls_text = settings_font_header.render("Center Controls", True, (0, 150, 150))
    WINDOW.blit(rocket_controls_text, (WIDTH * 0.75, HEIGHT * 0.775))


def show_settings_ui():
    if len(manager.get_sprite_group()) < 4:
        initialize_settings_ui()

    show_gui = True

    while show_gui:
        for event in pygame.event.get():
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "CloseSettings(ESC)_button":
                show_gui = False
            if event.type == pg.UI_BUTTON_PRESSED and event.ui_object_id == "ResetControls_button":
                Keys.reset_overwrite_current()
                manager.clear_and_reset()
                initialize_settings_ui()
            if check_key_down(event, Keys.h_close_window[0]):
                show_gui = False
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
        WINDOW.blit(rocket_background_img, (0, 0))
        display_ui_text_and_backgrounds()
        manager.draw_ui(WINDOW)
        pygame.display.update()

    manager.clear_and_reset()
