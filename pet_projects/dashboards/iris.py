##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Python
import typing

# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
page_title = html.H1(
    children="Simple example of Plotly Dashboard", style={"text-align": "center"},
)
page_header = html.Div(
    children="(Powered by Dash: A web application framework for Python)",
    style={"text-align": "center"},
)

# Body layout part
body_title = html.Div(
    children="Finding correlation in Iris data set", style={"text-align": "center"},
)
x_axis_dropdown = dcc.Dropdown(
    id="x-axis-dropdown",
    options=[
        {"label": column.capitalize().replace("_", " "), "value": column}
        for column in IRIS_DATA.columns.to_list()[0:4]
    ],
    style={"width": "400px", "margin-right": 5},
    placeholder="Select x axis data",
)
y_axis_dropdown = dcc.Dropdown(
    id="y-axis-dropdown",
    options=[
        {"label": column.capitalize().replace("_", " "), "value": column}
        for column in IRIS_DATA.columns.to_list()[0:4]
    ],
    style={"width": "400px"},
    placeholder="Select y axis data",
)
sepal_scatter = dcc.Graph(
    id="iris-scatter",
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
            "title": "Results",
            "xaxis": {"title": "Sepal length", "zeroline": False},
            "yaxis": {"title": "Sepal width", "zeroline": False},
            "hovermode": "closest",
        },
    },
)

app.layout = html.Div(
    children=[
        html.Div(
            id="iris-header",
            children=[page_title, page_header],
            style={"margin-bottom": 25},
        ),
        html.Div(
            id="iris-body",
            children=[
                html.Div(id="body-title", children=body_title),
                html.Div(
                    id="dropdowns",
                    children=[x_axis_dropdown, y_axis_dropdown],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "margi-top": 10,
                    },
                ),
                html.Div(id="plots", children=[sepal_scatter]),
            ],
        ),
    ]
)


##########################################################################################
#                                       CALLBACKS
##########################################################################################


@app.callback(
    Output("iris-scatter", "figure"),
    [Input("x-axis-dropdown", "value"), Input("y-axis-dropdown", "value")],
)
def update_figure(
    x_axis_dropdown_value: str, y_axis_dropdown_value: str
) -> typing.Dict:
    """
    Callback aimed to changes the Iris scatter content by selecting x nd y axis data

    :param x_axis_dropdown_value: the name of the data that will be displayed in the x
    axis
    :param y_axis_dropdown_value: the name of the data that will be displayed in the y
    axis
    :return: the data and the layout content
    """
    if x_axis_dropdown_value is None:
        x_axis_dropdown_value = "sepal_length"
    if y_axis_dropdown_value is None:
        y_axis_dropdown_value = "sepal_width"
    data = {
        "data": [
            {
                "x": IRIS_DATA[x_axis_dropdown_value],
                "y": IRIS_DATA[y_axis_dropdown_value],
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
            "title": "Results",
            "xaxis": {
                "title": x_axis_dropdown_value.capitalize().replace("_", " "),
                "zeroline": False,
            },
            "yaxis": {
                "title": y_axis_dropdown_value.capitalize().replace("_", " "),
                "zeroline": False,
            },
            "hovermode": "closest",
        },
    }
    return data


##########################################################################################
#                                       RUN SERVER
##########################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
