import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from math import cos
from math import pi as PI
DEG_LENGTH = 111300

workfolder = "work_folder\\40_osm_extracts_1x1\\+56+038\\"

QUADARANT = (38, 56, 39, 57)
# Latitude is also hardcoded below, beware!!!!

df_landuses = gpd.read_file(workfolder+"landuses-clipped-all.geojson")
df_buildings = gpd.read_file(workfolder+"buildings.geojson")
ds_building_areas = df_buildings.geometry.area

print()
print("invalid objects", "buildings.geojson")
df= df_buildings
invalid = df.loc[~df.geometry.is_valid]
print(invalid)

print()
print("invalid objects", "landuses-clipped-all.geojson")
df= df_landuses
invalid = df.loc[~df.geometry.is_valid]
print(invalid)


df_buildings.geometry = df_buildings.geometry.make_valid()
print(df_buildings)

for index, row in df_landuses.iterrows():

    

    m = df_buildings.geometry.intersects(row.geometry).loc[lambda x: x == True]
    n = m.size
    df_landuses.at[index, 'number_of_buildings'] = n  # number of buildings within the area
    landuse_area = row.geometry.area
    if n > 0:  # there are buildings withing this area
        number_of_buildings_with_levels = 0
        avg_levels = 0.0
        max_levels = 0.0
        min_levels = 0.0
        total_buildings_area = 0
        for i, row_buildings in m.items():
            building_levels = df_buildings.at[i, 'building:levels']
            building_footprint_area = ds_building_areas[i]
            total_buildings_area = total_buildings_area + building_footprint_area
            try:
                building_levels = float(building_levels)
            except ValueError:
                building_levels = float("nan")

            if not pd.isna(building_levels):

                avg_levels = avg_levels + building_levels
                number_of_buildings_with_levels = number_of_buildings_with_levels + 1

                if building_levels > max_levels:
                    max_levels = building_levels

                if min_levels==0:
                    min_levels = building_levels # we need to initialize min with the first value.
                if building_levels < min_levels:
                    min_levels = building_levels

        if number_of_buildings_with_levels > 0:
            # average building levels, min building levels, max building levels. -- to understand heights
            avg_levels = avg_levels / number_of_buildings_with_levels
            df_landuses.at[index, 'average_level'] = round (avg_levels,1)
            df_landuses.at[index, 'max_level'] = max_levels
            df_landuses.at[index, 'min_level'] = min_levels

        df_landuses.at[index, 'number_of_buildings_with_levels'] = number_of_buildings_with_levels
        # total area of buildings within the area, to calculate buiding density: area of buildings/area of landuse
        df_landuses.at[index, 'buildings_density'] = round(total_buildings_area / landuse_area, 3)
        # average building footprint area -- to understand what those buildings are
        df_landuses.at[index, 'average_building_area'] = round(total_buildings_area / n * DEG_LENGTH*DEG_LENGTH*cos(56.5/180*PI))
        df_landuses.at[index, 'area'] = round (landuse_area * DEG_LENGTH * DEG_LENGTH * cos(56.5/180*PI))

    else:
        # there are no buildings
        pass  # no means no!

df_landuses.to_file(workfolder+'landuses-clipped-enriched.geojson')
