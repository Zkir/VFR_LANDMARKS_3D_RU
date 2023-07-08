import geopandas as gpd
import matplotlib.pyplot as plt

workfolder="work_folder\\40_osm_extracts_1x1\\+56+038\\"

QUADARANT = (38, 56, 39, 57)


df_places = gpd.read_file(workfolder+"places.geojson")
df_places_points = gpd.read_file(workfolder+"places-points.geojson")

ds_places_pop = gpd.sjoin(
    df_places, 
    df_places_points, 
    how='left',
    predicate="contains",
)
ds_places_pop['geometry'] = ds_places_pop.geometry.make_valid()
ds_places_pop = ds_places_pop.clip(QUADARANT)
ds_places_pop.to_file(workfolder+'places-pop.geojson')


# create poligonal objects that we will use to patch other polygons.
df0 = gpd.read_file(workfolder+'highways.geojson')
df = df0.clip(QUADARANT)
#df.to_file(workfolder+'highways-clipped.geojson')


df = df.to_crs("EPSG:32637") # reproject, so that buffer can be in meeters
df['geometry'] = df.geometry.buffer(6, resolution=3 )
df=df.to_crs("EPSG:4326") # reproject back to WGS84!

df.to_file(workfolder+'highways-buffered.geojson')

#subtract roads from amenities.
df_amenities = gpd.read_file(workfolder+"amenities.geojson")
df_amenities['geometry'] = df_amenities.geometry.make_valid()
df_amenities = df_amenities.overlay(df, how='difference', keep_geom_type=False)
df_amenities = df_amenities.clip(QUADARANT)
df_amenities = df_amenities.explode(ignore_index=True)
df_amenities.to_file(workfolder+"amenities-clipped.geojson")

#subtract roads from naturals
df_naturals = gpd.read_file(workfolder+"naturals.geojson")
df_naturals['geometry'] = df_naturals.geometry.make_valid()
df_naturals = df_naturals.overlay(df, how='difference', keep_geom_type=False)
df_naturals = df_naturals.clip(QUADARANT)
df_naturals = df_naturals.explode(ignore_index=True)
df_naturals.to_file(workfolder+"naturals-clipped.geojson")



#subtract roads from landuses
#subtract amenities from landuses
df_landuses = gpd.read_file(workfolder+"landuses.geojson")
df_landuses['geometry'] = df_landuses.geometry.make_valid()
df_landuses = df_landuses.overlay(df, how='difference', keep_geom_type=False)
df_landuses = df_landuses.overlay(df_amenities, how='difference', keep_geom_type=False)
df_landuses = df_landuses.clip(QUADARANT)
df_landuses = df_landuses.explode(ignore_index=True)
df_landuses.to_file(workfolder+"landuses-clipped.geojson")


#subtract naturals from landuses???


#ds_places_pop.plot()
#plt.show()




