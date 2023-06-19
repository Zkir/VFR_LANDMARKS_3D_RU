
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
#* create x-plane specific files, e.g dsf per quadrant. 
#****************************************************************************************************************************	
work_folder\all-objects.dat: work_folder\10_osm_extracts\extract_building_models_osm
	python scripts\joindats.py work_folder\all-objects.dat work_folder\10_osm_extracts  
	
work_folder\50_DSF :
	mkdir work_folder\50_DSF

work_folder\50_DSF\+56+038.dat : work_folder\all-objects.dat | work_folder\50_DSF
	python scripts\filterdat.py work_folder\50_DSF\+56+038.dat work_folder\all-objects.dat +56+038   
	
work_folder\50_DSF\+56+038.dsf.txt: work_folder\50_DSF\+56+038.dat	
	python osmparser\mdlDSF.py
	
work_folder\50_DSF\+56+038.dsf: work_folder\50_DSF\+56+038.dsf.txt 
	d:\tools\xplane_tools\tools\dsftool --text2dsf  "$<" "$@"	
	
	
#****************************************************************************************************************************
#* Build X-Plane scenery package
#****************************************************************************************************************************		
x_plane_buildpath = work_folder\80_xplane_release\VFR_LANDMARKS_3D_RU
x_plane_workpath =  work_folder\50_DSF\+56+038
  
$(x_plane_buildpath):
	mkdir "$(x_plane_buildpath)"	
  
work_folder\clean_x_plane_release_folder: $(x_plane_buildpath)
	echo Cleaning the $(x_plane_buildpath)
	rmdir /S /Q $(x_plane_buildpath)
	touch $@
  
work_folder\init_x_plane_release_folder: work_folder\clean_x_plane_release_folder
	echo Creating the build directory structure
	mkdir "$(x_plane_buildpath)"
	mkdir "$(x_plane_buildpath)\Objects"
	mkdir "$(x_plane_buildpath)\Objects-osm"
	mkdir "$(x_plane_buildpath)\Facades"
	mkdir "$(x_plane_buildpath)\Earth nav data"
	mkdir "$(x_plane_buildpath)\Earth nav data\+50+030"
	touch $@
	
work_folder\copy_x_plane_files: work_folder\50_DSF\+56+038.dsf work_folder\30_3dmodels\convert_osm_to_obj  work_folder\init_x_plane_release_folder
	xcopy /Y /Q readme.txt $(x_plane_buildpath)
	xcopy /Y /Q "Custom_models\*.obj" $(x_plane_buildpath)\Objects
	xcopy /Y /Q "Custom_models\*.png" $(x_plane_buildpath)\Objects
	
	xcopy /Y /Q "Facades\*.fac" $(x_plane_buildpath)\Facades
	xcopy /Y /Q "Facades\*.png" $(x_plane_buildpath)\Facades

	xcopy /Y /Q "work_folder\30_3dmodels\*.obj" $(x_plane_buildpath)\Objects-osm
	xcopy /Y /Q "work_folder\30_3dmodels\*.png" $(x_plane_buildpath)\Objects-osm
	
	xcopy /Y /Q "work_folder\50_DSF\+56+038.dsf" "$(x_plane_buildpath)\Earth nav data\+50+030"	
	touch $@


work_folder\81_xplane_release_zip:
	mkdir work_folder\81_xplane_release_zip

work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip: work_folder\copy_x_plane_files  | work_folder\81_xplane_release_zip
	7z a $@ work_folder\80_xplane_Release


#****************************************************************************************************************************
#* Upload resulting data and models to web 
#****************************************************************************************************************************	
work_folder\90_uploads: | work_folder
	mkdir work_folder\90_uploads
	
work_folder\90_uploads\upload_models_to_web: work_folder\30_3dmodels\convert_obj_to_x3d | work_folder\90_uploads 	##Upload models and dat files to web  
	upload.bat
	touch $@		

work_folder\90_uploads\upload_xplane_release_to_web : work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip	| work_folder\90_uploads
	xcopy /Y /Q "work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip"   "3dcheck\downloads"
	touch $@
	
#****************************************************************************************************************************
#* Finish 
#****************************************************************************************************************************	
	
fin: work_folder\90_uploads\upload_models_to_web work_folder\90_uploads\upload_xplane_release_to_web
	echo "All done"