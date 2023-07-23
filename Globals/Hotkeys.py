import json

from Methods.JsonMethods import *

try:
    jsonFile = open("./Globals/HotkeysConfig/CurrentHotkeys.json")
    hotkeysJson = json.load(jsonFile)

    list_hot_keys = []

    # Rocket Controls

    h_rocket_boost_forward = get_h_rocket_boost_forward(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_forward)
    h_rocket_boost_left = get_h_rocket_boost_left(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_left)
    h_rocket_boost_right = get_h_rocket_boost_right(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_right)
    h_lower_rocket_boost = get_h_lower_rocket_boost(hotkeysJson)
    list_hot_keys.append(h_lower_rocket_boost)

    # Rocket Zooms
    h_zoom_rocket_start = get_h_zoom_rocket_start(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_start)
    h_zoom_rocket_planet = get_h_zoom_rocket_planet(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_planet)
    h_zoom_rocket_planet_system = get_h_zoom_rocket_planet_system(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_planet_system)
    h_zoom_auto_on_rocket = get_h_zoom_auto_on_rocket(hotkeysJson)
    list_hot_keys.append(h_zoom_auto_on_rocket)
    H_zoomAutoOnReferencePlanet = get_h_zoom_auto_on_reference_planet(hotkeysJson)
    list_hot_keys.append(H_zoomAutoOnReferencePlanet)

    # Centering
    h_center_on_sun = get_h_center_on_sun(hotkeysJson)
    list_hot_keys.append(h_center_on_sun)
    h_center_on_rocket = get_h_center_on_rocket(hotkeysJson)
    list_hot_keys.append(h_center_on_rocket)

    # Time Manipulation
    h_shift_time_step_up = get_h_shift_time_step_up(hotkeysJson)
    list_hot_keys.append(h_shift_time_step_up)
    h_shift_time_step_down = get_h_shift_time_step_down(hotkeysJson)
    list_hot_keys.append(h_shift_time_step_down)

    # Generals
    h_draw_line = get_h_draw_line(hotkeysJson)
    list_hot_keys.append(h_draw_line)
    h_show_distance = get_h_show_distance(hotkeysJson)
    list_hot_keys.append(h_show_distance)
    h_pause_simulation = get_h_pause_simulation(hotkeysJson)
    list_hot_keys.append(h_pause_simulation)

    # Navigation
    h_display_hot_keys = get_h_display_hot_keys(hotkeysJson)
    list_hot_keys.append(h_display_hot_keys)
    h_leave_simulation = get_h_leave_simulation(hotkeysJson)
    list_hot_keys.append(h_leave_simulation)
    h_open_settings = get_h_open_settings(hotkeysJson)
    list_hot_keys.append(h_open_settings)
    h_close_window = get_h_close_window(hotkeysJson)
    list_hot_keys.append(h_close_window)
    H_moveScreenUp = get_h_move_screen_up(hotkeysJson)
    list_hot_keys.append(H_moveScreenUp)
    H_moveScreenDown = get_h_move_screen_down(hotkeysJson)
    list_hot_keys.append(H_moveScreenDown)
    H_moveScreenRight = get_h_move_screen_right(hotkeysJson)
    list_hot_keys.append(H_moveScreenRight)
    H_moveScreenLeft = get_h_move_screen_left(hotkeysJson)
    list_hot_keys.append(H_moveScreenLeft)

except:
    # Error or Empty while Reading triggers copy from standard to current
    jsonFile = open("./Globals/HotkeysConfig/StandardHotkeys.json")

    hotkeysJson = json.load(jsonFile)

    with open("./Globals/HotkeysConfig/CurrentHotkeys.json", "w") as outfile:
        json.dump(hotkeysJson, outfile, indent=4, ensure_ascii=False)

    list_hot_keys = []

    # Rocket Controls

    h_rocket_boost_forward = get_h_rocket_boost_forward(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_forward)
    h_rocket_boost_left = get_h_rocket_boost_left(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_left)
    h_rocket_boost_right = get_h_rocket_boost_right(hotkeysJson)
    list_hot_keys.append(h_rocket_boost_right)
    h_lower_rocket_boost = get_h_lower_rocket_boost(hotkeysJson)
    list_hot_keys.append(h_lower_rocket_boost)

    # Rocket Zooms
    h_zoom_rocket_start = get_h_zoom_rocket_start(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_start)
    h_zoom_rocket_planet = get_h_zoom_rocket_planet(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_planet)
    h_zoom_rocket_planet_system = get_h_zoom_rocket_planet_system(hotkeysJson)
    list_hot_keys.append(h_zoom_rocket_planet_system)
    h_zoom_auto_on_rocket = get_h_zoom_auto_on_rocket(hotkeysJson)
    list_hot_keys.append(h_zoom_auto_on_rocket)
    H_zoomAutoOnReferencePlanet = get_h_zoom_auto_on_reference_planet(hotkeysJson)
    list_hot_keys.append(H_zoomAutoOnReferencePlanet)

    # Centering
    h_center_on_sun = get_h_center_on_sun(hotkeysJson)
    list_hot_keys.append(h_center_on_sun)
    h_center_on_rocket = get_h_center_on_rocket(hotkeysJson)
    list_hot_keys.append(h_center_on_rocket)

    # Time Manipulation
    h_shift_time_step_up = get_h_shift_time_step_up(hotkeysJson)
    list_hot_keys.append(h_shift_time_step_up)
    h_shift_time_step_down = get_h_shift_time_step_down(hotkeysJson)
    list_hot_keys.append(h_shift_time_step_down)

    # Generals
    h_draw_line = get_h_draw_line(hotkeysJson)
    list_hot_keys.append(h_draw_line)
    h_show_distance = get_h_show_distance(hotkeysJson)
    list_hot_keys.append(h_show_distance)
    h_pause_simulation = get_h_pause_simulation(hotkeysJson)
    list_hot_keys.append(h_pause_simulation)

    # Navigation
    h_display_hot_keys = get_h_display_hot_keys(hotkeysJson)
    list_hot_keys.append(h_display_hot_keys)
    h_leave_simulation = get_h_leave_simulation(hotkeysJson)
    list_hot_keys.append(h_leave_simulation)
    h_open_settings = get_h_open_settings(hotkeysJson)
    list_hot_keys.append(h_open_settings)
    h_close_window = get_h_close_window(hotkeysJson)
    list_hot_keys.append(h_close_window)
    H_moveScreenUp = get_h_move_screen_up(hotkeysJson)
    list_hot_keys.append(H_moveScreenUp)
    H_moveScreenDown = get_h_move_screen_down(hotkeysJson)
    list_hot_keys.append(H_moveScreenDown)
    H_moveScreenRight = get_h_move_screen_right(hotkeysJson)
    list_hot_keys.append(H_moveScreenRight)
    H_moveScreenLeft = get_h_move_screen_left(hotkeysJson)
    list_hot_keys.append(H_moveScreenLeft)

jsonFile.close()


def reset_overwrite_current():
    global list_hot_keys, h_rocket_boost_forward, h_rocket_boost_left, h_rocket_boost_right, h_lower_rocket_boost, h_zoom_rocket_start, h_zoom_rocket_planet, h_zoom_rocket_planet_system, h_zoom_auto_on_rocket, h_center_on_sun, h_center_on_rocket, h_shift_time_step_up, h_center_on_rocket, h_shift_time_step_up, h_shift_time_step_down, h_draw_line, h_show_distance, h_pause_simulation, h_display_hot_keys, h_leave_simulation, h_open_settings, h_close_window
    json_file = open("./Globals/HotkeysConfig/StandardHotkeys.json")
    hotkeys_json = json.load(json_file)

    with open("./Globals/HotkeysConfig/CurrentHotkeys.json", "w") as file:
        json.dump(hotkeys_json, file, indent=4, ensure_ascii=False)

    list_hot_keys = []
    json_file = open("./Globals/HotkeysConfig/CurrentHotkeys.json")
    hotkeys_json = json.load(json_file)
    # Rocket Controls

    h_rocket_boost_forward = get_h_rocket_boost_forward(hotkeys_json)
    list_hot_keys.append(h_rocket_boost_forward)
    h_rocket_boost_left = get_h_rocket_boost_left(hotkeys_json)
    list_hot_keys.append(h_rocket_boost_left)
    h_rocket_boost_right = get_h_rocket_boost_right(hotkeys_json)
    list_hot_keys.append(h_rocket_boost_right)
    h_lower_rocket_boost = get_h_lower_rocket_boost(hotkeys_json)
    list_hot_keys.append(h_lower_rocket_boost)

    # Rocket Zooms
    h_zoom_rocket_start = get_h_zoom_rocket_start(hotkeys_json)
    list_hot_keys.append(h_zoom_rocket_start)
    h_zoom_rocket_planet = get_h_zoom_rocket_planet(hotkeys_json)
    list_hot_keys.append(h_zoom_rocket_planet)
    h_zoom_rocket_planet_system = get_h_zoom_rocket_planet_system(hotkeys_json)
    list_hot_keys.append(h_zoom_rocket_planet_system)
    h_zoom_auto_on_rocket = get_h_zoom_auto_on_rocket(hotkeys_json)
    list_hot_keys.append(h_zoom_auto_on_rocket)
    h_zoom_auto_on_reference_planet = get_h_zoom_auto_on_reference_planet(hotkeys_json)
    list_hot_keys.append(h_zoom_auto_on_reference_planet)

    # Centering
    h_center_on_sun = get_h_center_on_sun(hotkeys_json)
    list_hot_keys.append(h_center_on_sun)
    h_center_on_rocket = get_h_center_on_rocket(hotkeys_json)
    list_hot_keys.append(h_center_on_rocket)

    # Time Manipulation
    h_shift_time_step_up = get_h_shift_time_step_up(hotkeys_json)
    list_hot_keys.append(h_shift_time_step_up)
    h_shift_time_step_down = get_h_shift_time_step_down(hotkeys_json)
    list_hot_keys.append(h_shift_time_step_down)

    # Generals
    h_draw_line = get_h_draw_line(hotkeys_json)
    list_hot_keys.append(h_draw_line)
    h_show_distance = get_h_show_distance(hotkeys_json)
    list_hot_keys.append(h_show_distance)
    h_pause_simulation = get_h_pause_simulation(hotkeys_json)
    list_hot_keys.append(h_pause_simulation)

    # Navigation
    h_display_hot_keys = get_h_display_hot_keys(hotkeys_json)
    list_hot_keys.append(h_display_hot_keys)
    h_leave_simulation = get_h_leave_simulation(hotkeys_json)
    list_hot_keys.append(h_leave_simulation)
    h_open_settings = get_h_open_settings(hotkeys_json)
    list_hot_keys.append(h_open_settings)
    h_close_window = get_h_close_window(hotkeys_json)
    list_hot_keys.append(h_close_window)
    h_move_screen_up = get_h_move_screen_up(hotkeys_json)
    list_hot_keys.append(h_move_screen_up)
    h_move_screen_down = get_h_move_screen_down(hotkeys_json)
    list_hot_keys.append(h_move_screen_down)
    h_move_screen_right = get_h_move_screen_right(hotkeys_json)
    list_hot_keys.append(h_move_screen_right)
    h_move_screen_left = get_h_move_screen_left(hotkeys_json)
    list_hot_keys.append(h_move_screen_left)

    json_file.close()
