import json

def getMonth():
    jsonfile = open("./variables/rocket_config/current_rocket_config.json")
    config = json.load(jsonfile)
    month = config["StartTime"]["Month"]["value"]
    return month

def getDay():
    jsonfile = open("./variables/rocket_config/current_rocket_config.json")
    config = json.load(jsonfile)
    day = config["StartTime"]["Day"]["value"]
    return day

def getYear():
    jsonfile = open("./variables/rocket_config/current_rocket_config.json")
    config = json.load(jsonfile)
    year = config["StartTime"]["Year"]["value"]
    return year

def checkDate(month, day ):
    if month in [1,3,5,7,8,10,12]:
         if day > 0 and 31 >= day:
              return True
    elif month in [4,6,8,11]:
         if day > 0 and 30 >= day:
              return True
    else:
        if getYear() % 4 != 0:
            if day > 0 and 28>= day:
                return True
        else:
             if day> 0 and 29>= day:
                  return True
    return False
def overWriteStandardDay():
    jsonfile = open("./variables/rocket_config/current_rocket_config.json", "r+")
    config = json.load(jsonfile)
    config["StartTime"]["Day"]["value"] = 28
    jsonfile.seek(0)
    jsonfile.truncate()
    json.dump(config, jsonfile, indent=4, ensure_ascii=False)