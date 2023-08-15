from ViewController.GameManager import GameManager
from Views.LoadingView import loading_screen
from Views.StartView import *

from Globals.FlightData.FlightDataManager import DATA

from Methods.PackageInstaller import package_installer
from Methods.ConfigurePlanets import configure_planets
from Methods.GameMethods import process_hot_key_events
from Methods.RocketConfig import load_rocket


def main():
    game_manager = GameManager(DATA_df)
    package_installer()
    show_start_ui()

    loading_screen()

    planets = configure_planets()
    rocket = load_rocket(planets)

    while DATA.run:
        CLOCK.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket, planets = process_hot_key_events(event, rocket, planets)

        game_manager.calculate_next_iteration(rocket, planets)
        game_manager.display_iteration(rocket, planets)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
