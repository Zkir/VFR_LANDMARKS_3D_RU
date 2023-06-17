
#(c)2023 3d building validator pipeline
all: fin
	echo "that's all, folks!"
	
work_folder: ## make the working folder 
	mkdir work_folder	
	
#****************************************************************************************************************************
#* fetch and update source OSM data  
#****************************************************************************************************************************
work_folder\00_planet.osm:  | work_folder ## make folder for source osm data
	mkdir work_folder\00_planet.osm	

work_folder\00_planet.osm\russia-latest.osm.pbf: | work_folder\00_planet.osm ##download source osm file
	echo "download source osm file"
	scripts\planet_download.bat $(@D)

work_folder\00_planet.osm\russia.poly: | work_folder\00_planet.osm
	copy poly\russia.poly work_folder\00_planet.osm
	
#update osm file 
work_folder\00_planet.osm\russia-latest.o5m: work_folder\00_planet.osm\russia-latest.osm.pbf work_folder\00_planet.osm\russia.poly  	
	echo "update osm file" 
	scripts\planet_update.bat $(@D)

#****************************************************************************************************************************
#* Create geocoder files 
#****************************************************************************************************************************
work_folder\05_geocoder: | work_folder
	mkdir work_folder\05_geocoder
	
work_folder\05_geocoder\geocoder.osm: work_folder\00_planet.osm\russia-latest.o5m	 | work_folder\05_geocoder
	echo "create geocoder files work_folder\05_geocoder work_folder\00_planet.osm" 
	scripts\geocoder_extract.bat work_folder\05_geocoder work_folder\00_planet.osm

#actually geocoder txt should be created from geocode.osm, but the script was lost. 	
work_folder\05_geocoder\geocoder.txt: work_folder\05_geocoder\geocoder.osm	
	copy geocoder.txt work_folder\05_geocoder
	touch $@

#****************************************************************************************************************************
#* Extract objects from OSM
#****************************************************************************************************************************	
work_folder\10_osm_extracts: | work_folder ## make folder for extracted osm buildings 
	mkdir work_folder\10_osm_extracts	
	
work_folder\Quadrants.dat: | work_folder
	copy Quadrants.dat work_folder

work_folder\20_osm_3dmodels: ## make folder for extracted 3d buildings 
	mkdir work_folder\20_osm_3dmodels

#cleanup_20_osm_3dmodels_folder: | work_folder\20_osm_3dmodels ##cleanup folder with output models
#	echo stange cleanup of 3d models, worth removal
#	cleanup.bat work_folder\20_osm_3dmodels
#	touch $@


work_folder\10_osm_extracts\extract_building_models_osm: work_folder\00_planet.osm\russia-latest.o5m work_folder\05_geocoder\geocoder.txt work_folder\Quadrants.dat |  work_folder\10_osm_extracts work_folder\20_osm_3dmodels
	python osmparser\planner.py
	touch $@	

#****************************************************************************************************************************
#* Convert models to x-plane obj and x3d 
#****************************************************************************************************************************		
work_folder\30_3dmodels: | work_folder
	mkdir work_folder\30_3dmodels 
	
work_folder\30_3dmodels\convert_osm_to_obj: work_folder\10_osm_extracts\extract_building_models_osm | work_folder\30_3dmodels 	##Convert 3d objects from osm files to blender and x-plane obj 
	for %%v in (work_folder\20_osm_3dmodels\*.osm) do osm2blend.bat "%%v" work_folder\30_3dmodels
	touch $@		
	
work_folder\30_3dmodels\convert_obj_to_x3d: work_folder\30_3dmodels\convert_osm_to_obj              ##Convert x-plane obj files to x3d, to be used on website.  		
	for %%v in (work_folder\30_3dmodels\*.obj) do obj2x3d.py "%%v"
	touch $@		
	

#****************************************************************************************************************************
#* Upload resulting data and models to web 
#****************************************************************************************************************************	
work_folder\90_uploads: | work_folder
	mkdir work_folder\90_uploads
	
work_folder\90_uploads\upload_models_to_web: work_folder\30_3dmodels\convert_obj_to_x3d | work_folder\90_uploads 	##Upload models and dat files to web  
	upload.bat
	touch $@		
	
fin: work_folder\90_uploads\upload_models_to_web
	echo "All done"