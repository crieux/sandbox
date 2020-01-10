##########################################################################################
#                                     IMPORT LIBRARIES
##########################################################################################

# Config
from pet_projects.dashboards.config import IRIS_DATA_PATH

# Python
import random
import typing

# Data science
import pandas as pd
import numpy as np
from decimal import Decimal
import scipy.stats as ss
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation


##########################################################################################
#                                       FUNCTIONS
##########################################################################################

CLUSTERING_METHODS = [
    "K-means",
    "Affinity propagation",
    "Mean-shift",
    "Special clustering",
    "Ward hierarchical clustering",
    "DBSCAN",
    "OPTICS",
    "Gaussian mixtures",
    "Birch",
]


##########################################################################################
#                                       FUNCTIONS
##########################################################################################


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


def compute_pearson_correlation_coefficient(
    x_data: pd.Series, y_data: pd.Series
) -> typing.Tuple[float, float]:
    """
    Compute the Pearson correlation coefficient from Scipy library:
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html

    :param x_data: the x data set
    :param y_data: the y data set
    :return: the rounded Pearson correlation coefficient and the associated p-value
    """
    coef, p_value = ss.pearsonr(x_data, y_data)
    return round(coef, 2), "%.2E" % Decimal(p_value)


def compute_clustering(
    x_data: pd.Series, y_data: pd.Series, method: str, nb_clusters: int
) -> np.array:
    """
    Compute clustering using Scikit-learn:
    https://scikit-learn.org/stable/modules/clustering.html
    Several algorithms can be chosen:
        - K-means: https://scikit-learn.org/stable/modules/clustering.html#k-means
        - Affinity propagation: https://scikit-learn.org/stable/modules/generated/sklearn\
        .cluster.AffinityPropagation.html#sklearn.cluster.AffinityPropagation

    :param x_data: the x data set
    :param y_data: the y data set
    :param method: name of the algorithm used to perform clustering
    :param nb_clusters: number of clusters used to split data
    :return: the data set labels used to color scatter points
    """
    mapped_data = [row for row in zip(x_data, y_data)]
    if method == "K-means":
        kmeans = KMeans(n_clusters=nb_clusters, random_state=0).fit(mapped_data)
        return kmeans.labels_
    if method == "Affinity propagation":
        clustering = AffinityPropagation().fit(mapped_data)
        return clustering.labels_
