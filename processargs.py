import string


def readConfig(config):
    f = open(config, "r")
    options = {}

    for line in f:
        equals = string.find(line, "=")
        options[line[:equals]] = line[equals + 1:len(line) - 1]

    f.close()

    return options
