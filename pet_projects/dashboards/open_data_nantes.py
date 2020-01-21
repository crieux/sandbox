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
    get_and_parse_tan_lines,
)

# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
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
        for _, district in get_nantes_districts_data().iterrows()
    ],
    multi=True,
    style={"width": "400px", "margin-right": 5},
    placeholder="Select a district...",
)
tan_lines_dropdown = dcc.Dropdown(
    id="tan-lines-dropdown",
    options=[
        {"label": line, "value": line}
        for line in get_and_parse_tan_lines()["route_id"].sort_values().unique()
    ],
    multi=True,
    style={"width": "400px", "margin-right": 5},
    placeholder="Select a tan line...",
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
                    id="map-dropdowns",
                    children=[districts_dropdown, tan_lines_dropdown],
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
    Output("map", "figure"),
    [Input("districts-dropdown", "value"), Input("tan-lines-dropdown", "value")],
)
def update_map(
    districts_geometry_coordinates: typing.List[str], tan_lines: typing.List[str]
) -> typing.Dict:
    """
    Update the layers of the map with district polygons, tan lines etc...

    :param districts_geometry_coordinates: the geometry of the selected district(s) to be
    displayed
    :param tan_lines: the names of the selected tan line(s) to be displayed
    :return: the figure
    """
    figure = copy.deepcopy(MAP_FIG)
    if districts_geometry_coordinates is not None:
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
    if tan_lines is not None:
        all_lines = get_and_parse_tan_lines()
        selected_lines = all_lines.loc[all_lines["route_id"].isin(tan_lines)]
        current_data = figure["data"]
        figure["data"] = list(current_data) + [
            go.Scattermapbox(
                name=row["route_id"],
                mode="lines",
                lon=row["shape_lon"],
                lat=row["shape_lat"],
                text=row["trip_headsign"],
                marker={"size": 5, "color": "black"},
            )
            for _, row in selected_lines.iterrows()
        ]
    return figure


##########################################################################################
#                                    RUNNING SERVER
##########################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
