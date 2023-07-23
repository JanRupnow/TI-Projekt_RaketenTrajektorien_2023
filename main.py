from Views.FlightView import render_flight_interface
from Views.StartView import *

from ViewController.GameManager import GameManager

from Methods.PackageInstaller import install_all_packages
from Methods.ConfigurePlanets import configure_planets
from Methods.GameMethods import process_hot_key_events
from Methods.RocketConfig import load_rocket


def main():
    install_all_packages()
    show_start_ui()

    now = datetime.datetime.now()

    planets = configure_planets()
    rocket = load_rocket(planets)

    while DATA.get_run():
        CLOCK.tick(60)

        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket = process_hot_key_events(event, rocket, planets)

        GameManager.calculate_next_iteration(rocket, planets)
        GameManager.display_iteration(rocket, planets)
        render_flight_interface(rocket, now)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
