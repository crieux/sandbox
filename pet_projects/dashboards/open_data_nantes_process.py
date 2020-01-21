##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Config
from pet_projects.dashboards.config import (
    MAP_TOKEN,
    NANTES_DISTRICTS_INFO,
    NANTES_PARKINGS_INFO,
    NANTES_PARKINGS_AVAILABILITY,
)

# Python
# import typing
import requests
import json

# Data science
import pandas as pd

# Dashboard
import plotly.graph_objects as go


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


def get_nantes_districts_data() -> pd.DataFrame:
    """
    Read and return the Nantes districts data

    :return: the Nantes districts data
    """
    r_districts = requests.get(NANTES_DISTRICTS_INFO)
    all_districts_info = pd.io.json.json_normalize(
        json.loads(r_districts.text)["records"]
    )
    all_districts_info.sort_values("fields.nom", inplace=True)
    return all_districts_info


def get_nantes_parkings_info() -> pd.DataFrame:
    """
    Retrieve the Nantes parks info from the API and convert it into a pd.DataFrame

    :return: the Nantes parks info
    """
    r_all_parkings_info = requests.get(NANTES_PARKINGS_INFO)
    all_parkings_info = pd.io.json.json_normalize(
        json.loads(r_all_parkings_info.text)["records"]
    )
    r_parkings_availability = requests.get(NANTES_PARKINGS_AVAILABILITY)
    parkings_availability = pd.io.json.json_normalize(
        json.loads(r_parkings_availability.text)["records"]
    )
    parkings_availability["fields.grp_nom"] = parkings_availability[
        "fields.grp_nom"
    ].apply(lambda cell: f"Parking {cell}")
    all_parkings_info.rename(
        columns={"fields.nom_complet": "fields.grp_nom"}, inplace=True
    )
    merged_parking_data = all_parkings_info.merge(
        parkings_availability, on="fields.grp_nom"
    )
    return merged_parking_data


##########################################################################################
#                                       CONSTANTS
##########################################################################################

MAP_FIG = {
    "data": [
        go.Scattermapbox(
            name=row["fields.grp_nom"],
            lon=[row["geometry.coordinates"][0]],
            lat=[row["geometry.coordinates"][1]],
            mode="markers",
            textposition="bottom center",
            text=f"{row['fields.grp_horodatage']}<br>{row['fields.grp_disponible']}"
            f" sur {row['fields.grp_exploitation']} places disponibles",
            hoverinfo="text",
            showlegend=False,
            marker={"symbol": "car", "size": 15},
        )
        for _, row in get_nantes_parkings_info().iterrows()
    ],
    "layout": go.Layout(
        height=700,
        hovermode="closest",
        geo={"projection": {"type": "equirectangular"}},
        mapbox={
            "accesstoken": get_mapbox_token(),
            "bearing": 0,
            "center": {"lon": -1.5534, "lat": 47.2173},
            "pitch": 0,
            "zoom": 12,
            "style": "outdoors",
            "layers": [],
        },
    ),
}
