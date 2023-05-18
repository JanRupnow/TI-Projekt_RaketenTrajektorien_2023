import json
from methods.json_methods import *
from objects.rocket import *
from methods.initialise_planets import *

def loadRocketFromPath(path, planets):
    jsonfile = open(path)
    config = json.load(jsonfile)
    
    startplanet = next(filter(lambda x: x.name == 
                                config["start"]["start planet"], 
                                planets))

    img = pygame.image.load(config["image_path"])
    img = pygame.transform.scale_by(img, 125/img.get_width())

    rocket = Rocket(
        config["start"]["angle on planet"],
        config["start"]["start angle"],
        config["mass"]["propellant mass"],
        config["mass"]["rocket structure mass"],
        startplanet,
        config["radius"],
        (
            config["color"]["red"],
            config["color"]["green"],
            config["color"]["blue"]
        ),
        next(filter(lambda x: x.name == "Sonne", planets),None),
        img
    )
    #if config["start"]["start thrust"]
    jsonfile.close()
    return rocket


def loadRocket(planets):
    try:
        return loadRocketFromPath("./variables/rocket_config/current_rocket_config.json", planets)
    except:
        return loadRocketFromPath("./variables/rocket_config/standard_rocket_config.json", planets)
    
