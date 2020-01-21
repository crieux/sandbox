##########################################################################################
#                                    IMPORT LIBRARIES
##########################################################################################

# Python
import typing
import json
import copy

# Config
from pet_projects.dashboards.open_data_nantes_process import (
    MAP_FIG,
    get_nantes_districts_data,
)

# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


##########################################################################################
#                                       BUILD APP
##########################################################################################

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##########################################################################################
#                                      BUILD LAYOUT
##########################################################################################

# Header layout part
page_title = html.H1(
    children="Simple example of Plotly Dashboard", style={"text-align": "center"},
)
page_header = html.Div(
    children="(Powered by Dash: A web application framework for Python)",
    style={"text-align": "center"},
)

# Map layout part
map_title = html.Div(
    children='Open data from "Nantes métropole"', style={"text-align": "center"},
)

districts_dropdown = dcc.Dropdown(
    id="districts-dropdown",
    options=[
        {
            "label": district["fields.nom"].capitalize(),
            "value": f"{district['fields.geometry.coordinates']}",
        }
        for index, district in get_nantes_districts_data().iterrows()
    ],
    multi=True,
    style={"width": "400px", "margin-right": 5},
    placeholder="Select a district...",
)
mapbox = dcc.Graph(id="map", figure=MAP_FIG, animate=False)

app.layout = html.Div(
    children=[
        html.Div(
            id="map-header",
            children=[page_title, page_header],
            style={"margin-bottom": 25},
        ),
        html.Div(
            id="map-body",
            children=[
                html.Div(id="map-title", children=map_title),
                html.Div(
                    id="districts-dropdowns",
                    children=[districts_dropdown],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "margin-top": 10,
                        "margin-bottom": 10,
                    },
                ),
                html.Div(id="map-content", children=[mapbox]),
            ],
        ),
    ]
)


##########################################################################################
#                                       CALLBACKS
##########################################################################################


@app.callback(
    Output("map", "figure"), [Input("districts-dropdown", "value")],
)
def update_map(districts_geometry_coordinates: typing.List[str],) -> typing.Dict:
    """
    Update the layers of the map for districts, etc...

    :param districts_geometry_coordinates: the geometry of the district to be displayed
    :return: the figure
    """
    if districts_geometry_coordinates is None:
        return MAP_FIG
    figure = copy.deepcopy(MAP_FIG)
    current_layer = figure["layout"]["mapbox"]["layers"]
    figure["layout"]["mapbox"]["layers"] = list(current_layer) + [
        {
            "sourcetype": "geojson",
            "source": {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": json.loads(geometry_coordinates),
                },
            },
            "color": "blue",
            "opacity": 0.7,
            "type": "line",
        }
        for geometry_coordinates in districts_geometry_coordinates
    ]
    return figure


##########################################################################################
#                                    RUNNING SERVER
##########################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
