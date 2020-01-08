################################################################################
#                              IMPORT LIBRARIES
################################################################################

# Config
from pet_projects.dashboards.config import IRIS_DATA_PATH

# Python
import random

# Data science
import pandas as pd


################################################################################
#                                 FUNCTIONS
################################################################################


def set_random_hex() -> int:
    """
    Set a random integer between 0 and 255

    :return: the integer
    """
    return random.randint(0, 255)


def set_random_color() -> str:
    """
    Set a random color in hex format, eg. : "252, 186, 3"

    :return:
    """
    return "#%02X%02X%02X" % (set_random_hex(), set_random_hex(), set_random_hex())


def read_iris_data() -> pd.DataFrame:
    """
    Read iris.csv data from inputs folder

    :return: the iris data
    """
    iris_data = pd.read_csv(IRIS_DATA_PATH, header=0)
    return iris_data


def parse_iris_data() -> pd.DataFrame:
    """
    Parse the iris data by:
        - capitalizing the first letter of "species" column
        - adding a color column that is a random unique color for all species

    :return: the parsed data
    """
    iris_data = read_iris_data()
    iris_data["species"] = iris_data["species"].str.capitalize()
    iris_data["colors"] = iris_data["species"]
    iris_species = iris_data["species"].unique()
    for specie in iris_species:
        iris_data["colors"].replace(specie, set_random_color(), inplace=True)
    return iris_data
