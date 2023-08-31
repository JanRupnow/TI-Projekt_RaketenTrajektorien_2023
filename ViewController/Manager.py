from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket


class Manager:
    def set_rocket_and_planets(self, rocket: Rocket, planets: list[Planet]):
        self.rocket = rocket
        self.planets = planets