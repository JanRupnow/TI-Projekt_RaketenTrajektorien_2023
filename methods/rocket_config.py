import json
from methods.json_methods import *
from objects.rocket import *
from methods.initialise_planets import *

def loadRocketFromPath(path, planets):
    jsonfile = open(path)
    config = json.load(jsonfile)
    
    startplanet = next(filter(lambda x: x.name == 
                                config["Start"]["Startplanet"]["value"], 
                                planets))

    img = pygame.image.load(config["ImagePath"])
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
        next(filter(lambda x: x.name == "Sonne", planets),None),
        img
    )

    if config["Start"]["Thrust"]["value"] > 0:
        rocket.thrust = config["Start"]["Thrust"]["value"]
        rocket.powerchanged = True
        rocket.rocketstarted = True
    rocket.angle = config["Start"]["Angle"]["value"]

    jsonfile.close()
    return rocket


def loadRocket(planets):
    try:
        return loadRocketFromPath("./variables/rocket_config/current_rocket_config.json", planets)
    except:
        # write standard config to current config
        with open("./variables/rocket_config/current_rocket_config.json", "w") as outfile:
            json.dump(json.load(open("./variables/rocket_config/standard_rocket_config.json")), 
                      outfile, 
                      indent=4, 
                      ensure_ascii=False)
            
        return loadRocketFromPath("./variables/rocket_config/current_rocket_config.json", planets)
    
