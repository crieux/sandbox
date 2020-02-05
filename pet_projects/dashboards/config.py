################################################################################
#                              IMPORT LIBRARIES
################################################################################

from pathlib import Path
import os

################################################################################
#                                 CONSTANTS
################################################################################

INPUT_DATA = Path("inputs/")
CONFIG_DATA = Path("config/")
OUTPUT_DATA = Path("outputs/")

# iris.py
IRIS_DATA_PATH = os.path.join(INPUT_DATA, "iris.csv")

# open_data_nantes.py
MAP_TOKEN = os.path.join(CONFIG_DATA, "map_token")
NANTES_DISTRICTS_INFO = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_quartiers-nantes&rows=-1&facet=nom"
NANTES_PARKINGS_INFO = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes&rows=-1&facet=libcategorie&facet=libtype&facet=acces_pmr&facet=service_velo&facet=stationnement_velo&facet=stationnement_velo_securise&facet=moyen_paiement"
NANTES_PARKINGS_AVAILABILITY = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes-disponibilites&rows=-1&facet=grp_nom&facet=grp_statut"
TAN_STOPS = os.path.join(INPUT_DATA, "tan/stops.txt")
TAN_SHAPES = os.path.join(INPUT_DATA, "tan/shapes.txt")
TAN_LINES = os.path.join(INPUT_DATA, "tan/trips.txt")
