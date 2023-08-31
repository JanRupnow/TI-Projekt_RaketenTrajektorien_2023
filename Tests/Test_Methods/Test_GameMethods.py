import numpy as np
import pytest
from Globals.Constants import WIDTH, HEIGHT, AllTimeSteps, STARTSCALE
from Globals.FlightData.FlightDataManager import DATA
from Methods.GameMethods import convert_to_line_in_screen, planet_is_in_screen, shift_time_step, scale_relative, \
    mouse_position_shift_screen


# Centering Methods are tested optically

@pytest.mark.parametrize("factor", [2, 0.5])
def test_scale_relative(factor: float) -> None:
    scale_relative(factor)
    assert DATA.scale == STARTSCALE * factor


@pytest.mark.parametrize("mouse_x, mouse_y, move_x, move_y", [
    (10, 10, -10, -10),
    (10, 0, -10, -10),
    (0, 10, -10, -10),
    (0, 0, -10, -10),
    (-10, 0, -10, -10),
    (0, -10, -10, -10),
    (-10, -10, -10, -10),
    (10, 10, 0, 0),
    (10, 0, 0, 0),
    (0, 10, 0, 0),
    (0, 0, 0, 0),
    (-10, 0, 0, 0),
    (0, -10, 0, 0),
    (-10, -10, 0, 0),
    (10, 10, 10, 10),
    (10, 0, 10, 10),
    (0, 10, 10, 10),
    (0, 0, 10, 10),
    (-10, 0, 10, 10),
    (0, -10, 10, 10),
    (-10, -10, 10, 10),
])
def test_mouse_position_shift_screen(mouse_x: int, mouse_y: int, move_x: int, move_y: int) -> None:
    DATA.move_x = move_x
    DATA.move_y = move_y
    DATA.mouse_x = mouse_x
    DATA.mouse_y = mouse_y

    mouse_position_shift_screen()
    expected_x = move_x - (mouse_x - WIDTH / 2) / 2
    expected_y = move_y - (mouse_y - HEIGHT / 2) / 2
    assert DATA.move_x == expected_x
    assert DATA.move_y == expected_y


@pytest.mark.parametrize("shift_up, expected_time_step_rocket, expected_time_step_planet", [
    (False, AllTimeSteps[3], AllTimeSteps[3]),  # Time shift down
    (True, AllTimeSteps[5], AllTimeSteps[5])  # Time shift up
])
def test_shift_time_step(shift_up, expected_time_step_rocket, expected_time_step_planet) -> None:
    class Rocket:
        def __init__(self):
            self.time_step = AllTimeSteps[4]

    class Planet:
        def __init__(self):
            self.time_step = AllTimeSteps[4]

    rocket = Rocket()
    planets = [Planet(), Planet()]

    DATA.time_step = AllTimeSteps[4]

    shift_time_step(shift_up, planets, rocket)

    assert rocket.time_step == expected_time_step_rocket
    for planet in planets:
        assert planet.time_step == expected_time_step_planet


def test_convert_to_line_in_screen() -> None:
    # Create a line that partially falls within and outside the screen boundaries
    line = np.array(
        [[-WIDTH * 2, -HEIGHT * 2], [-WIDTH * 2, 0], [0, -HEIGHT * 2], [0, 0], [WIDTH + 30, 0], [0, HEIGHT + 30],
         [WIDTH + 30, HEIGHT + 30]])
    #               [[false, false] [false, true], [true, false], [true, true], [false, true], [true, false], [false, false]]
    DATA.move_x = 5
    DATA.move_y = 15
    result = convert_to_line_in_screen(line)

    # Define the expected output based on the points within the screen boundaries
    expected_output = np.array([[WIDTH / 2 + 5, HEIGHT / 2 + 15]])

    # Verify that the method correctly filters points outside the screen
    np.testing.assert_array_equal(result, expected_output)


@pytest.mark.parametrize("expected_output, step", [
    (False, 0),  # Both positions to low
    (False, 1),  # X-Position to low
    (False, 2),  # Y-Position to low
    (True, 3),  # Radius keeps the planet inside
    (False, 4),  # X-Position to high
    (False, 5),  # Y-Position to high
    (False, 6),  # Both positions to high
])
def test_planet_is_in_screen(expected_output: bool, step: int) -> None:
    # Create a line that partially falls within and outside the screen boundaries
    class Planet:
        def __init__(self):
            # -WIDTH-30 should be outside the screen but radius puts it inside
            # -HEIGHT-30 should be outside the screen but radius puts it inside
            self.position_X = np.array([-WIDTH * 2, -WIDTH * 2, -WIDTH - 30, -WIDTH + 30, WIDTH * 2, 0, WIDTH * 2])
            self.position_Y = np.array([-HEIGHT * 2, 0, -HEIGHT * 2, -HEIGHT - 30, 0, HEIGHT * 2, HEIGHT * 2])
            self.radius = 100
            self.currentStep = step

    #      [[false, false] [false, true], [true, false], [true, true], [false, true], [true, false], [false, false]]
    DATA.move_x = 0
    DATA.move_y = 0
    DATA.scale = 0.5
    planet = Planet()
    result = planet_is_in_screen(planet)
    assert np.isclose(result, expected_output), f"Expected: {expected_output}, Got: {result}"
