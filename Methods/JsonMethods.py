from Methods.SupportMethods import *


def update_key_in_json(json, hotkey):
    for category in json.Keys():
        for key in json[category].Keys():
            if hotkey[1] == json[category][key]["text"]:
                json[category][key]["key"] = hotkey[0]
    return json


def update_key_in_json_rocket(json, identifier, value):
    for category in json.keys():
        try:
            for key in json[category].keys():
                # didn't need to catch because this method should only update values
                # which are in the form of the if clause
                try:
                    if identifier == remove_spaces(
                            json[category][key]["text"] + "_input") or identifier == remove_spaces(
                        json[category][key]["text"] + "_dropdown"):
                        if value.isdigit():
                            json[category][key]["value"] = int(value)
                        else:
                            json[category][key]["value"] = value
                except:
                    pass
        except:
            pass
    return json


# Rocket Controls
def get_h_rocket_boost_forward(hotkeys_json):
    return [
        hotkeys_json["RocketControls"]["H_rocketBoostForward"]["key"],
        hotkeys_json["RocketControls"]["H_rocketBoostForward"]["text"]
    ]


def get_h_rocket_boost_left(hotkeys_json):
    return [
        hotkeys_json["RocketControls"]["H_rocketBoostLeft"]["key"],
        hotkeys_json["RocketControls"]["H_rocketBoostLeft"]["text"]
    ]


def get_h_rocket_boost_right(hotkeys_json):
    return [
        hotkeys_json["RocketControls"]["H_rocketBoostRight"]["key"],
        hotkeys_json["RocketControls"]["H_rocketBoostRight"]["text"]
    ]


def get_h_lower_rocket_boost(hotkeys_json):
    return [
        hotkeys_json["RocketControls"]["H_lowerRocketBoost"]["key"],
        hotkeys_json["RocketControls"]["H_lowerRocketBoost"]["text"]
    ]


# Rocket Zooms
def get_h_zoom_rocket_start(hotkeys_json):
    return [
        hotkeys_json["RocketZooms"]["H_zoomRocketStart"]["key"],
        hotkeys_json["RocketZooms"]["H_zoomRocketStart"]["text"]
    ]


def get_h_zoom_rocket_planet(hotkeys_json):
    return [
        hotkeys_json["RocketZooms"]["H_zoomRocketPlanet"]["key"],
        hotkeys_json["RocketZooms"]["H_zoomRocketPlanet"]["text"]
    ]


def get_h_zoom_rocket_planet_system(hotkeys_json):
    return [
        hotkeys_json["RocketZooms"]["H_zoomRocketPlanetSystem"]["key"],
        hotkeys_json["RocketZooms"]["H_zoomRocketPlanetSystem"]["text"]
    ]


def get_h_zoom_auto_on_rocket(hotkeys_json):
    return [
        hotkeys_json["RocketZooms"]["H_zoomAutoOnRocket"]["key"],
        hotkeys_json["RocketZooms"]["H_zoomAutoOnRocket"]["text"]
    ]


def get_h_zoom_auto_on_reference_planet(hotkeys_json):
    return [
        hotkeys_json["RocketZooms"]["H_zoomAutoOnReferencePlanet"]["key"],
        hotkeys_json["RocketZooms"]["H_zoomAutoOnReferencePlanet"]["text"]
    ]


# Centering
def get_h_center_on_sun(hotkeys_json):
    return [
        hotkeys_json["Centering"]["H_centerOnSun"]["key"],
        hotkeys_json["Centering"]["H_centerOnSun"]["text"]
    ]


def get_h_center_on_rocket(hotkeys_json):
    return [
        hotkeys_json["Centering"]["H_centerOnRocket"]["key"],
        hotkeys_json["Centering"]["H_centerOnRocket"]["text"]
    ]


# Time Manipulation
def get_h_shift_time_step_up(hotkeys_json):
    return [
        hotkeys_json["TimeManipulation"]["H_shiftTimeStepUp"]["key"],
        hotkeys_json["TimeManipulation"]["H_shiftTimeStepUp"]["text"]
    ]


def get_h_shift_time_step_down(hotkeys_json):
    return [
        hotkeys_json["TimeManipulation"]["H_shiftTimeStepDown"]["key"],
        hotkeys_json["TimeManipulation"]["H_shiftTimeStepDown"]["text"]
    ]


# Generals
def get_h_draw_line(hotkeys_json):
    return [
        hotkeys_json["Generals"]["H_drawLine"]["key"],
        hotkeys_json["Generals"]["H_drawLine"]["text"]
    ]


def get_h_show_distance(hotkeys_json):
    return [
        hotkeys_json["Generals"]["H_showDistance"]["key"],
        hotkeys_json["Generals"]["H_showDistance"]["text"]
    ]


def get_h_pause_simulation(hotkeys_json):
    return [
        hotkeys_json["Generals"]["H_pauseSimulation"]["key"],
        hotkeys_json["Generals"]["H_pauseSimulation"]["text"]
    ]


def get_h_switch_interface(hotkeys_json):
    return [
        hotkeys_json["Generals"]["H_interfaceMode"]["key"],
        hotkeys_json["Generals"]["H_interfaceMode"]["text"]
    ]


# Navigation
def get_h_leave_simulation(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_leaveSimulation"]["key"],
        hotkeys_json["Navigation"]["H_leaveSimulation"]["text"]
    ]


def get_h_open_settings(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_openSettings"]["key"],
        hotkeys_json["Navigation"]["H_openSettings"]["text"]
    ]


def get_h_close_window(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_closeWindow"]["key"],
        hotkeys_json["Navigation"]["H_closeWindow"]["text"]
    ]


def get_h_move_screen_up(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_moveScreenUp"]["key"],
        hotkeys_json["Navigation"]["H_moveScreenUp"]["text"]
    ]


def get_h_move_screen_down(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_moveScreenDown"]["key"],
        hotkeys_json["Navigation"]["H_moveScreenDown"]["text"]
    ]


def get_h_move_screen_right(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_moveScreenRight"]["key"],
        hotkeys_json["Navigation"]["H_moveScreenRight"]["text"]
    ]


def get_h_move_screen_left(hotkeys_json):
    return [
        hotkeys_json["Navigation"]["H_moveScreenLeft"]["key"],
        hotkeys_json["Navigation"]["H_moveScreenLeft"]["text"]
    ]
