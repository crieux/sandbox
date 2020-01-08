##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Data science
# import pandas as pd

# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html

# Process
from pet_projects.dashboards.iris_process import parse_iris_data


##########################################################################################
#                                        CONSTANTS
##########################################################################################

IRIS_DATA = parse_iris_data()

##########################################################################################
#                                        BUILD APP
##########################################################################################

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##########################################################################################
#                                        BUILD LAYOUT
##########################################################################################

# Header layout part
title = html.H1(children="Simple example of Plotly Dashboard based on Iris dataset")
header = html.Div(children="Powered by Dash: A web application framework for Python")

# Body layout part
sepal_scatter = dcc.Graph(
    id="sepal-scatter",
    figure={
        "data": [
            {
                "x": IRIS_DATA["sepal_length"],
                "y": IRIS_DATA["sepal_width"],
                "text": IRIS_DATA["species"],
                "mode": "markers",
                "opacity": 0.7,
                "marker": {
                    "color": IRIS_DATA["colors"],
                    "size": 8,
                    "line": {"width": 0.5, "color": "white"},
                },
            },
        ],
        "layout": {
            "title": "Sepal length VS sepal width",
            "xaxis": {"title": "Sepal length", "zeroline": False},
            "yaxis": {"title": "Sepal width", "zeroline": False},
        },
    },
)
petal_scatter = dcc.Graph(
    id="petal-scatter",
    figure={
        "data": [
            {
                "x": IRIS_DATA["petal_length"],
                "y": IRIS_DATA["petal_width"],
                "text": IRIS_DATA["species"],
                "mode": "markers",
                "opacity": 0.7,
                "marker": {
                    "color": IRIS_DATA["colors"],
                    "size": 8,
                    "line": {"width": 0.5, "color": "white"},
                },
            },
        ],
        "layout": {
            "title": "Petal length VS petal width",
            "xaxis": {"title": "Petal length", "zeroline": False},
            "yaxis": {"title": "Petal width", "zeroline": False},
        },
    },
)

app.layout = html.Div(children=[title, header, sepal_scatter, petal_scatter])


##########################################################################################
#                                       RUN SERVER
##########################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
