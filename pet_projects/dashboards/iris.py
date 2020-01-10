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
from pet_projects.dashboards.iris_process import (
    CLUSTERING_METHODS,
    parse_iris_data,
    compute_pearson_correlation_coefficient,
    compute_clustering,
)


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
    children="Simple example of Plotly Dashboard based on Iris data set",
    style={"text-align": "center"},
)
page_header = html.Div(
    children="(Powered by Dash: A web application framework for Python)",
    style={"text-align": "center"},
)

# Correlation layout part
correlation_title = html.Div(
    children="Finding correlation", style={"text-align": "center"},
)
correlation_x_axis_dropdown = dcc.Dropdown(
    id="correlation-x-axis-dropdown",
    options=[
        {"label": column.capitalize().replace("_", " "), "value": column}
        for column in IRIS_DATA.columns.to_list()[0:4]
    ],
    style={"width": "400px", "margin-right": 5},
    placeholder="Select x axis data (default Sepal length)",
)
correlation_y_axis_dropdown = dcc.Dropdown(
    id="correlation-y-axis-dropdown",
    options=[
        {"label": column.capitalize().replace("_", " "), "value": column}
        for column in IRIS_DATA.columns.to_list()[0:4]
    ],
    style={"width": "400px"},
    placeholder="Select y axis data (default Sepal width)",
)
correlation_scatter = dcc.Graph(id="correlation-scatter",)
clustering_title = html.Div(
    children="Finding cluster(s)", style={"text-align": "center"},
)
clustering_method_dropdown = dcc.Dropdown(
    id="clustering-method-dropdown",
    options=[{"label": method, "value": method} for method in CLUSTERING_METHODS],
    style={"width": "400px"},
    placeholder="Select clustering method (default K-means)",
)
clustering_cluster_nb_dropdown = dcc.Dropdown(
    id="clustering-cluster-nb-dropdown",
    options=[{"label": cluster_nb, "value": cluster_nb} for cluster_nb in range(1, 6)],
    style={"width": "400px"},
    placeholder="Select the number of cluster (default 3)",
)
clustering_scatter = dcc.Graph(id="clustering-scatter",)

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
                html.Div(id="correlation-title", children=correlation_title),
                html.Div(
                    id="correlation-dropdowns",
                    children=[correlation_x_axis_dropdown, correlation_y_axis_dropdown],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "margi-top": 10,
                    },
                ),
                html.Div(id="correlation-plot", children=[correlation_scatter]),
                html.Div(id="clustering-title", children=[clustering_title]),
                html.Div(
                    id="clustering-dropdowns",
                    children=[
                        clustering_method_dropdown,
                        clustering_cluster_nb_dropdown,
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "margi-top": 10,
                    },
                ),
                html.Div(id="clustering-plot", children=[clustering_scatter]),
            ],
        ),
    ]
)

##########################################################################################
#                                       CALLBACKS
##########################################################################################


@app.callback(
    Output("correlation-scatter", "figure"),
    [
        Input("correlation-x-axis-dropdown", "value"),
        Input("correlation-y-axis-dropdown", "value"),
    ],
)
def update_correlation_scatter_figure(
    x_axis_dropdown_value: str, y_axis_dropdown_value: str
) -> typing.Dict:
    """
    Callback aimed to changes the Iris scatter content by selecting x and y axis data sets

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
    x_data = IRIS_DATA[x_axis_dropdown_value]
    y_data = IRIS_DATA[y_axis_dropdown_value]
    coef, p_value = compute_pearson_correlation_coefficient(x_data, y_data)
    figure = {
        "data": [
            {
                "x": x_data,
                "y": y_data,
                "text": IRIS_DATA["species"],
                "mode": "markers",
                "marker": {
                    "color": IRIS_DATA["colors"],
                    "size": 20,
                    "line": {"width": 3, "color": "black"},
                },
            },
        ],
        "layout": {
            "title": f"Pearson correlation coefficient: {coef}, p-value: {p_value}",
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
    return figure


@app.callback(
    Output("clustering-scatter", "figure"),
    [
        Input("correlation-x-axis-dropdown", "value"),
        Input("correlation-y-axis-dropdown", "value"),
        Input("clustering-method-dropdown", "value"),
        Input("clustering-cluster-nb-dropdown", "value"),
    ],
)
def update_clustering_scatter_figure(
    x_axis_dropdown_value: str,
    y_axis_dropdown_value: str,
    clustering_method: str,
    cluster_nb: int,
) -> typing.Dict:
    """
    Callback aimed to update clustering scatter content by selecting x and y axis data
    sets and clustering method

    :param x_axis_dropdown_value: the name of the data that will be displayed in the x
    axis
    :param y_axis_dropdown_value: the name of the data that will be displayed in the y
    axis
    :param clustering_method: the name of the clustering method
    :param cluster_nb: the number of cluster
    :return: the data and the layout content
    """
    if x_axis_dropdown_value is None:
        x_axis_dropdown_value = "sepal_length"
    if y_axis_dropdown_value is None:
        y_axis_dropdown_value = "sepal_width"
    if clustering_method is None:
        clustering_method = "K-means"
    if cluster_nb is None:
        cluster_nb = 3
    x_data = IRIS_DATA[x_axis_dropdown_value]
    y_data = IRIS_DATA[y_axis_dropdown_value]
    figure = {
        "data": [
            {
                "x": x_data,
                "y": y_data,
                "text": IRIS_DATA["species"],
                "mode": "markers",
                "marker": {
                    "color": IRIS_DATA["colors"],
                    "size": 20,
                    "line": {
                        "width": 3,
                        "color": compute_clustering(
                            x_data, y_data, clustering_method, cluster_nb,
                        ),
                    },
                },
            },
        ],
        "layout": {
            "xaxis": {"title": "Sepal length", "zeroline": False},
            "yaxis": {"title": "Sepal width", "zeroline": False},
            "hovermode": "closest",
        },
    }
    return figure


##########################################################################################
#                                       RUN SERVER
##########################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
