import json

from ViewController.Planet import *
from ViewController.Rocket.Rocket import Rocket
from ViewController.DrawManager import DrawManager


def load_rocket_from_path(path, planets: list[Planet]) -> Rocket:
    jsonfile = open(path)
    config = json.load(jsonfile)

    startplanet = next(filter(lambda x: x.name == config["Start"]["Startplanet"]["value"], planets))

    img = pygame.image.load(config["Image"]["path"][config["Image"]["selectedNumber"]])
    img = pygame.transform.scale_by(img, 125 / img.get_width())
    rocket = Rocket(
        config["Start"]["AngleOnPlanet"]["value"],
        config["Mass"]["PropellantMass"]["value"],
        config["Mass"]["StructMass"]["value"],
        startplanet,
        config["Radius"],
        (
            config["Color"]["red"],
            config["Color"]["green"],
            config["Color"]["blue"]
        ),
        next(filter(lambda x: x.name == "Sun", planets), None),
        config["BurningRate"]["value"],
        config["ExhaustSpeed"]["value"]
    )

    if config["Start"]["Thrust"]["value"] > 0:
        rocket.thrust = config["Start"]["Thrust"]["value"]
        rocket.powerchanged = True
        rocket.flightState = RocketFlightState.flying
    rocket.angle = config["Start"]["Angle"]["value"]

    DrawManager.set_rocket_image(img, rocket.radius)

    jsonfile.close()
    return rocket


def load_rocket(planets: list[Planet]) -> Rocket:
    try:
        return load_rocket_from_path("./Globals/RocketConfig/CurrentRocketConfig.json", planets)
    except:
        # write standard config to current config
        with open("./Globals/RocketConfig/CurrentRocketConfig.json", "w") as outfile:
            json.dump(json.load(open("./Globals/RocketConfig/StandardRocketConfig.json")),
                      outfile,
                      indent=4,
                      ensure_ascii=False)

        return load_rocket_from_path("./Globals/RocketConfig/CurrentRocketConfig.json", planets)
