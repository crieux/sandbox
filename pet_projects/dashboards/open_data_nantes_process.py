##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Config
from pet_projects.dashboards.config import MAP_TOKEN, NANTES_DISTRICTS

# Python
# import typing

# Data science
import pandas as pd


##########################################################################################
#                                       FUNCTIONS
##########################################################################################


def get_mapbox_token() -> str:
    """
    Read and return the map box token

    :return: the map ox token
    """
    mapbox_token = open(MAP_TOKEN).read()
    return mapbox_token


def get_nantes_district_data() -> pd.DataFrame:
    """
    Read and return the Nantes districts data

    :return: the Nantes districts data
    """
    nantes_districts = pd.read_csv(NANTES_DISTRICTS, header=0, encoding="ISO-8859-1")
    nantes_districts.sort_values("Quartier", inplace=True)
    return nantes_districts
