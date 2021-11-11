import json


def openJSON(filename):
    """
    Function reads output.txt file generated from visit_matrix_vis
    and returns a dictionary mapping every
    building name (key) to the corresponding array of
    infected.
    """
    container = {}

    with open(filename) as file:
        db = json.load(file)

    length = len(db["Buildings"])

    for i in range(length):
        tempdict = db["Buildings"][i]
        keys = list(tempdict.keys())
        key = tempdict[keys[0]]
        value = tempdict[keys[1]]
        container[key] = value

    return container


def openJSON_to_file(filename):
    """
    Function reads output.txt file generated from visit_matrix_vis
    and returns a json file mapping every
    building name (key) to the corresponding array of
    infected.
    """
    container = {}

    with open(filename) as file:
        db = json.load(file)

    length = len(db["Buildings"])

    for i in range(length):
        tempdict = db["Buildings"][i]
        keys = list(tempdict.keys())
        key = tempdict[keys[0]]
        value = tempdict[keys[1]]
        container[key] = value

    with open('data.json', 'w') as towrite:
        json.dump(container, towrite, indent=4)


if __name__ == "__main__":
    openJSON_to_file('output.json')