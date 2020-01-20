##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Config
from pet_projects.dashboards.config import MAP_TOKEN, NANTES_DISTRICTS

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


def get_nantes_district_data() -> pd.DataFrame:
    """
    Read and return the Nantes districts data

    :return: the Nantes districts data
    """
    nantes_districts = pd.read_csv(NANTES_DISTRICTS, header=0, encoding="ISO-8859-1")
    nantes_districts.sort_values("Quartier", inplace=True)
    return nantes_districts


def get_nantes_parkings_info() -> pd.DataFrame:
    """
    Retrieve the Nantes parks info from the API and convert it into a pd.DataFrame

    :return: the Nantes parks info
    """
    # r_parkings_places = requests.get(
    #     "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes-disponibilites&facet=grp_nom&facet=grp_statut"
    # )
    # parkings_places = pd.io.json.json_normalize(json.loads(r_parks_places.text)["records"])
    r_all_parkings_info = requests.get(
        "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes&facet=libcategorie&facet=libtype&facet=acces_pmr&facet=service_velo&facet=stationnement_velo&facet=stationnement_velo_securise&facet=moyen_paiement"
    )
    all_parkings_info = pd.io.json.json_normalize(
        json.loads(r_all_parkings_info.text)["records"]
    )
    return all_parkings_info


##########################################################################################
#                                       CONSTANTS
##########################################################################################

MAP_FIG = {
    "data": [
        go.Scattermapbox(
            name=row["fields.nom_complet"],
            lon=[row["geometry.coordinates"][0]],
            lat=[row["geometry.coordinates"][1]],
            mode="markers",
            textposition="bottom center",
            text=row["fields.nom_complet"],
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
