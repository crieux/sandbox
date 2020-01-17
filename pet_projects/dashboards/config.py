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
NANTES_DISTRICTS = os.path.join(INPUT_DATA, "quartiers_nantes_16012020.csv")
