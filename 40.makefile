all: fin 

work_folder\40_osm_extracts_1x1:
	mkdir work_folder\40_osm_extracts_1x1
	

work_folder\40_osm_extracts_1x1\+56+038: | work_folder\40_osm_extracts_1x1
	mkdir work_folder\40_osm_extracts_1x1\+56+038	
	
work_folder\40_osm_extracts_1x1\+56+038\+56+038.osm.pbf:  work_folder\00_planet.osm\russia-latest.osm.pbf | work_folder\40_osm_extracts_1x1\+56+038
	osmconvert work_folder\00_planet.osm\russia-latest.osm.pbf -B=poly\+56+038.poly --complete-multipolygons  -o="work_folder\40_osm_extracts_1x1\+56+038\+56+038.osm.pbf"	

work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m:  work_folder\40_osm_extracts_1x1\+56+038\+56+038.osm.pbf | work_folder\40_osm_extracts_1x1\+56+038
	osmconvert work_folder\40_osm_extracts_1x1\+56+038\+56+038.osm.pbf -o="work_folder\40_osm_extracts_1x1\+56+038\+56+038-pre.o5m"
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038-pre.o5m \
	    --drop-tags="landuse=logging =peat_cutting =basin =village_green" \
		--modify-tags="landuse=forest to natural=wood landuse=grass to natural=grass landuse=farmland to natural=farmland landuse=meadow to natural=meadow landuse=orchard to natural=orchard leisure=park to amenity=park" \
		-o="work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m"
	
	
work_folder\40_osm_extracts_1x1\+56+038\buildings.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="building=*" >work_folder\40_osm_extracts_1x1\+56+038\buildings.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\buildings.osm work_folder\40_osm_extracts_1x1\+56+038\buildings.geojson \
        --action=write_poly --keep="building=" --required-tags="height building:* roof:*"	
		
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="man_made=*" --drop="building=*" >work_folder\40_osm_extracts_1x1\+56+038\manmades.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\manmades.osm  work_folder\40_osm_extracts_1x1\+56+038\manmades.geojson \
        --action=write_poly --keep="man_made="


work_folder\40_osm_extracts_1x1\+56+038\landuses.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="landuse=*" --drop="landuse=military" >work_folder\40_osm_extracts_1x1\+56+038\landuses.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\landuses.osm  work_folder\40_osm_extracts_1x1\+56+038\landuses.geojson  --action=write_poly --keep="landuse= " --required-tags="natural"	

work_folder\40_osm_extracts_1x1\+56+038\naturals.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m ##extract naturals polygons	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="natural=* " >work_folder\40_osm_extracts_1x1\+56+038\naturals.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\naturals.osm  work_folder\40_osm_extracts_1x1\+56+038\naturals.geojson  --action=write_poly --keep="natural= and not landuse= " --required-tags="landuse"	
	
work_folder\40_osm_extracts_1x1\+56+038\highways.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="highway=*" --drop="highway=path =service =footway =steps =construction =proposed or area=yes" >work_folder\40_osm_extracts_1x1\+56+038\highways.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\highways.osm  $@  --action=write_lines --keep="highway=" 
	
work_folder\40_osm_extracts_1x1\+56+038\highways-area.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="( highway=* and area=yes ) or area:highway= " >work_folder\40_osm_extracts_1x1\+56+038\highways-area.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\highways-area.osm  $@  --action=write_poly --keep=" ( highway= and area=yes ) or area:highway= " 

work_folder\40_osm_extracts_1x1\+56+038\highways2.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="highway=path =service =footway =steps =construction =proposed" --drop="area=yes" >work_folder\40_osm_extracts_1x1\+56+038\highways2.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\highways2.osm  $@  --action=write_lines --keep="highway=" 


work_folder\40_osm_extracts_1x1\+56+038\leisures.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="leisure=*" --drop="building=*"  >work_folder\40_osm_extracts_1x1\+56+038\leisures.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\leisures.osm  $@  --action=write_poly --keep="leisure= and not leisure=nature_reserve"  --required-tags="surface"

work_folder\40_osm_extracts_1x1\+56+038\amenities.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="amenity=*" --drop="building=*"  >work_folder\40_osm_extracts_1x1\+56+038\amenities.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\amenities.osm  $@  --action=write_poly --keep="amenity=park =school =kindergarten =university =hospital and not landuse=" 

work_folder\40_osm_extracts_1x1\+56+038\parkings.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m 	
	osmfilter work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m --keep="amenity=parking" --drop="building=*"  >work_folder\40_osm_extracts_1x1\+56+038\parkings.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\parkings.osm  $@  --action=write_poly --keep="amenity=parking and not landuse=" 		
	
work_folder\40_osm_extracts_1x1\+56+038\places.geojson: 	work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter $< --keep="place=city =town =village =hamlet"   >work_folder\40_osm_extracts_1x1\+56+038\places.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\places.osm  $@  --action=write_poly --keep="place= " 	
	
work_folder\40_osm_extracts_1x1\+56+038\places-points.geojson: 	work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter $< --keep= --keep-nodes="place=city =town =village =hamlet"   >work_folder\40_osm_extracts_1x1\+56+038\places-poi.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\places-poi.osm  $@  --action=write_poi  --keep="place= " 	


work_folder\40_osm_extracts_1x1\+56+038\waterways.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter $< --keep="waterway=*"   >work_folder\40_osm_extracts_1x1\+56+038\waterways.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\waterways.osm  $@  --action=write_lines  --keep="waterway= " 	

work_folder\40_osm_extracts_1x1\+56+038\railways.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter $< --keep="railway=*"   >work_folder\40_osm_extracts_1x1\+56+038\railways.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\railways.osm  $@  --action=write_lines  --keep="railway= " 	

work_folder\40_osm_extracts_1x1\+56+038\barriers.geojson: work_folder\40_osm_extracts_1x1\+56+038\+56+038.o5m
	osmfilter $< --keep="barrier=*"   >work_folder\40_osm_extracts_1x1\+56+038\barriers.osm	
	python zOsm2GeoJSON\zOsm2GeoJSON.py work_folder\40_osm_extracts_1x1\+56+038\barriers.osm  $@  --action=write_lines  --keep="barrier= " 	
	

work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped.geojson : \
                     work_folder\40_osm_extracts_1x1\+56+038\highways.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\leisures.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\amenities.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\places.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\places-points.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\naturals.geojson \
                     work_folder\40_osm_extracts_1x1\+56+038\landuses.geojson
	python clip_dsf_layers.py
	
work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped-all.geojson: work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped.geojson work_folder\40_osm_extracts_1x1\+56+038\amenities-clipped.geojson
	python join_geojsons.py $@ $^

work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped-enriched.geojson: work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped-all.geojson work_folder\40_osm_extracts_1x1\+56+038\buildings.geojson
	python enrich_landuses.py
	
work_folder\40_osm_extracts_1x1\+56+038\+56+038.geojson	:  work_folder\40_osm_extracts_1x1\+56+038\landuses-clipped-enriched.geojson work_folder\40_osm_extracts_1x1\+56+038\naturals-clipped.geojson
	python join_geojsons.py $@ $^

work_folder\40_osm_extracts_1x1\+56+038\+56+038.dsf.txt:  work_folder\40_osm_extracts_1x1\+56+038\+56+038.geojson
	python geojson2dsftxt.py $< $@
	python dsftxt2geojson.py $@ work_folder\40_osm_extracts_1x1\+56+038\+56+038.decompiled.geojson

work_folder\40_osm_extracts_1x1\+56+038\+56+038.dsf: work_folder\40_osm_extracts_1x1\+56+038\+56+038.dsf.txt 
	dsftool --text2dsf $< $@
	xcopy /Q /Y $@ "d:\SteamLibrary\steamapps\common\X-Plane 11\Custom Scenery\zzz_zkir_global_scenery0\Earth nav data\+50+030"


fin: work_folder\40_osm_extracts_1x1\+56+038\+56+038.dsf
