################################################################################
#                              IMPORT LIBRARIES
################################################################################

from pathlib import Path
import os

################################################################################
#                                 CONSTANTS
################################################################################

INPUT_DATA = Path("inputs/")
OUTPUT_DATA = Path("outputs/")

IRIS_DATA_PATH = os.path.join(INPUT_DATA, "iris.csv")
MAP_TOKEN = os.path.join(INPUT_DATA, "map_token")
NANTES_DISTRICTS_INFO = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_quartiers-nantes&rows=-1&facet=nom"
NANTES_PARKINGS_INFO = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes&rows=-1&facet=libcategorie&facet=libtype&facet=acces_pmr&facet=service_velo&facet=stationnement_velo&facet=stationnement_velo_securise&facet=moyen_paiement"
NANTES_PARKINGS_AVAILABILITY = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_parkings-publics-nantes-disponibilites&rows=-1&facet=grp_nom&facet=grp_statut"
