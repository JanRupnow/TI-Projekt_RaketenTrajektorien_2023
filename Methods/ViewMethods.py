import json


def get_start_month() -> int:
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    month = config["StartTime"]["Month"]["value"]
    return month


def get_start_day() -> int:
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    day = config["StartTime"]["Day"]["value"]
    return day


def get_start_year() -> int:
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    year = config["StartTime"]["Year"]["value"]
    return year


def check_date_is_legal( day: int, month: int, year: int) -> bool:
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if 0 < day <= 31:
            return True
        else:
            return False
    elif month in [4, 6, 9, 11]:
        if 0 < day <= 30:
            return True
        else:
            return False
    elif month == 2:
        if year % 4 != 0:
            if 0 < day <= 28:
                return True
            else:
                return False
        else:
            if 0 < day <= 29:
                return True
            else:
                return False #this test pls
    else:
        return False


def over_write_standard_day():
    with open("./Globals/RocketConfig/CurrentRocketConfig.json", "r+") as jsonfile:
        config = json.load(jsonfile)
        config["StartTime"]["Day"]["value"] = 28
        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(config, jsonfile, indent=4, ensure_ascii=False)
        jsonfile.close()
