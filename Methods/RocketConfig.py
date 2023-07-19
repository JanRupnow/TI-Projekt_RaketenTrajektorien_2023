import json

from ViewController.Rocket.Rocket import *
from ViewController.Planet import *

from Methods.JsonMethods import *
from Methods.ConfigurePlanets import *

def LoadRocketFromPath(path, planets : list[Planet]):
    jsonfile = open(path)
    config = json.load(jsonfile)
    
    startplanet = next(filter(lambda x: x.name == 
                                config["Start"]["Startplanet"]["value"], 
                                planets))

    img = pygame.image.load(config["Image"]["path"][config["Image"]["selectedNumber"]])
    img = pygame.transform.scale_by(img, 125/img.get_width())

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
        next(filter(lambda x: x.name == "Sun", planets),None),
        img
    )

    if config["Start"]["Thrust"]["value"] > 0:
        rocket.thrust = config["Start"]["Thrust"]["value"]
        rocket.powerchanged = True
        rocket.rocketstarted = True
    rocket.angle = config["Start"]["Angle"]["value"]

    jsonfile.close()
    return rocket


def LoadRocket(planets : list[Planet]):
    try:
        return LoadRocketFromPath("./Globals/RocketConfig/CurrentRocketConfig.json", planets)
    except:
        # write standard config to current config
        with open("./Globals/RocketConfig/CurrentRocketConfig.json", "w") as outfile:
            json.dump(json.load(open("./Globals/RocketConfig/StandardRocketConfig.json")), 
                      outfile, 
                      indent=4, 
                      ensure_ascii=False)
            
        return LoadRocketFromPath("./Globals/RocketConfig/CurrentRocketConfig.json", planets)