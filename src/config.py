"""
config.py

All paths and constants for the pipeline. EDIT THIS FILE if your input
parquet files live somewhere else.
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent

# INPUT FILES
YELLOW_PARQUET = PROJECT_ROOT / "data" / "processed" / "yellow_taxi" / "yellow_taxi_2025.parquet"
HVFHV_PARQUET = PROJECT_ROOT / "data" / "processed" / "hvfhv" / "hvfhv_2025.parquet"
YELLOW_CLEAN05_PARQUET = PROJECT_ROOT / "data" / "processed" / "yellow_taxi" / "yellow_taxi_2025_clean05.parquet"
HVFHV_CLEAN005_PARQUET = PROJECT_ROOT / "data" / "processed" / "hvfhv" / "hvfhv_2025_uber_lyft_clean005.parquet"
HVFHV_CLEAN05_PARQUET = PROJECT_ROOT / "data" / "processed" / "hvfhv" / "hvfhv_2025_uber_lyft_clean05.parquet"
YELLOW_CLEAN05_CSV = PROJECT_ROOT / "data" / "processed" / "yellow_taxi" / "yellow_taxi_2025_clean05.csv"
HVFHV_CLEAN005_CSV = PROJECT_ROOT / "data" / "processed" / "hvfhv" / "hvfhv_2025_uber_lyft_clean005.csv"
HVFHV_CLEAN05_CSV = PROJECT_ROOT / "data" / "processed" / "hvfhv" / "hvfhv_2025_uber_lyft_clean05.csv"
NYC_WEATHER_PARQUET = PROJECT_ROOT / "data" / "raw" / "weather" / "nyc_central_park_weather_2025.xlsx"
NYC_BOROUGH_MAPPING = PROJECT_ROOT / "data" / "taxi_zone_lookup.csv"
SUBWAY_CSV_1 = PROJECT_ROOT / "data" / "raw" / "subway" / "MTA_Subway_Hourly_Ridership__Beginning_202501_202506.csv"
SUBWAY_CSV_2 = PROJECT_ROOT / "data" / "raw" / "subway" / "MTA_Subway_Hourly_Ridership__Beginning_202507_202512.csv"
SUBWAY_PARQUET = PROJECT_ROOT / "data" / "processed" / "subway" / "MTA_subway_hourly_2025.csv"

# OUTPUT DIRECTORIES
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"
CHART_DIR = OUTPUT_DIR / "charts"

# -----------------------------------------------------------------------------
# Time window
# -----------------------------------------------------------------------------
YEARS = 2025

# Sample rate of the HVFHV file
YELLOW_SAMPLE_RATE = 0.01
HVFHV_SAMPLE_RATE = 0.001
YELLOW_SCALE_FACTOR = 1.0 / YELLOW_SAMPLE_RATE   # 100x
HVFHV_SCALE_FACTOR = 1.0 / HVFHV_SAMPLE_RATE   # 1000x

# -----------------------------------------------------------------------------
# Congestion Relief Zone (CBD)
# -----------------------------------------------------------------------------
# Effective Jan 5, 2025. Manhattan south of and including 60th Street.
# These TLC zone IDs cover the CBD (compiled from TLC zone names mapped to the
# CRZ boundary). May be slightly approximate at the 60th St boundary -- ok for
# our purposes since the regression has zone fixed effects anyway.
CBD_ZONE_IDS = {
    4,    # Alphabet City
    12,   # Battery Park
    13,   # Battery Park City
    24,   # Bloomingdale (UWS area near 60th -- borderline; included)
    41,   # Central Harlem (no -- this is wrong, exclude)
    45,   # Chinatown
    48,   # Clinton East
    50,   # Clinton West
    68,   # East Chelsea
    79,   # East Village
    87,   # Financial District North
    88,   # Financial District South
    90,   # Flatiron
    100,  # Garment District
    103,  # Governor's Island
    104,  # Liberty Island
    105,  # Ellis Island
    107,  # Gramercy
    113,  # Greenwich Village North
    114,  # Greenwich Village South
    125,  # Hudson Sq
    137,  # Kips Bay
    140,  # Lenox Hill East (60th-77th -- borderline; exclude in strict CRZ)
    141,  # Lenox Hill West (borderline; exclude)
    144,  # Little Italy / NoLiTa
    148,  # Lower East Side
    151,  # Manhattan Valley (no -- exclude)
    158,  # Meatpacking / West Village
    161,  # Midtown Center
    162,  # Midtown East
    163,  # Midtown North
    164,  # Midtown South
    170,  # Murray Hill
    186,  # Penn Station / Madison Sq W
    194,  # Randalls Island (no, exclude)
    202,  # Roosevelt Island (north of 60th -- exclude)
    209,  # Seaport
    211,  # SoHo
    224,  # Stuy Town / Peter Cooper Village
    229,  # Sutton Place / Turtle Bay North (north of 60th -- exclude)
    230,  # Times Sq / Theatre District
    231,  # TriBeCa / Civic Center
    232,  # Two Bridges / Seward Park
    233,  # UN / Turtle Bay South
    234,  # Union Sq
    246,  # West Chelsea / Hudson Yards
    249,  # West Village
    261,  # World Trade Center
    262,  # Yorkville East (north of 60th -- exclude)
    263,  # Yorkville West (north of 60th -- exclude)
}

# Strict version: remove the borderline / north-of-60th zones flagged above
# EXCLUDE_FROM_CBD = {41, 140, 141, 151, 194, 202, 229, 24, 262, 263}
# CBD_ZONE_IDS = CBD_ZONE_IDS - EXCLUDE_FROM_CBD

# CBD fee start date (NY local time)
import pandas as pd
CBD_START = pd.Timestamp("2025-01-01 00:00:00")
