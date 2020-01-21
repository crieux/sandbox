##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Config
from pet_projects.dashboards.config import (
    MAP_TOKEN,
    NANTES_DISTRICTS_INFO,
    NANTES_PARKINGS_INFO,
    NANTES_PARKINGS_AVAILABILITY,
    TAN_STOPS,
    TAN_SHAPES,
    TAN_LINES,
)

# Python
# import typing
import requests
import json

# Data science
import pandas as pd
import numpy as np

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


def get_tan_stops() -> pd.DataFrame:
    """
    Read and return the "Transports de l'Agglomération Nantaise" (TAN) tramway and bus
    stops

    :return: the tramway an bus stops
    """
    tan_stops = pd.read_table(TAN_STOPS, header=0, sep=",")
    return tan_stops


def get_and_parse_tan_lines() -> pd.DataFrame:
    """
    Read, parse and return the "Transports de l'Agglomération Nantaise" (TAN) tramway and
    bus lines

    :return: the tramway an bus lines
    """
    tan_shapes = pd.read_table(TAN_SHAPES, header=0, index_col=None, sep=",")
    tan_lines = pd.read_table(TAN_LINES, header=0, index_col=None, sep=",")
    shapes = tan_shapes["shape_id"].unique()
    parsed_tan_shapes = pd.DataFrame(columns=["shape_id", "shape_lat", "shape_lon"])
    for shape in shapes:
        lat = tan_shapes["shape_pt_lat"].loc[tan_shapes["shape_id"] == shape].to_list()
        lon = tan_shapes["shape_pt_lon"].loc[tan_shapes["shape_id"] == shape].to_list()
        parsed_tan_shapes = parsed_tan_shapes.append(
            pd.Series({"shape_id": shape, "shape_lat": lat, "shape_lon": lon}),
            ignore_index=True,
        )
    parsed_tan_lines = tan_lines[
        ["shape_id", "route_id", "trip_headsign"]
    ].drop_duplicates()
    parsed_tan_lines["route_id"] = parsed_tan_lines["route_id"].apply(
        lambda cell: cell.split("-")[0]
    )
    merged = parsed_tan_shapes.merge(parsed_tan_lines, on="shape_id")
    return merged


##########################################################################################
#                                       CONSTANTS
##########################################################################################

MAP_FIG = {
    "data": [
        go.Scattermapbox(
            # name=row["fields.grp_nom"],
            # lon=[row["geometry.coordinates"][0]],
            # lat=[row["geometry.coordinates"][1]],
            # mode="markers",
            # textposition="bottom center",
            # text=f"{row['fields.grp_nom']}<br>"
            # f"{row['fields.adresse']}<br>"
            # f"{row['fields.grp_horodatage']}<br>"
            # f"{row['fields.grp_disponible']}"
            # f" sur {row['fields.grp_exploitation']} places disponibles<br>",
            # # f"{row['fields.acces_transports_communs']}",
            # hoverinfo="text",
            # showlegend=False,
            # marker={"symbol": "car", "size": 10},
        )
        for _, row in get_nantes_parkings_info().iterrows()
    ],
    # + [
    #     go.Scattermapbox(
    #         name=row["stop_name"],
    #         lon=[row["stop_lon"]],
    #         lat=[row["stop_lat"]],
    #         mode="markers",
    #         textposition="bottom center",
    #         text=f"{row['stop_name']}<br>",
    #         hoverinfo="text",
    #         showlegend=False,
    #         marker={"symbol": "bus", "size": 5},
    #     )
    #     for _, row in get_tan_stops().iterrows()
    # ],
    "layout": go.Layout(
        height=700,
        hovermode="closest",
        showlegend=False,
        hoverlabel={"bgcolor": "blue"},
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
