
#(c)2023 3d building validator pipeline
all: fin ##ultimate target 
	echo "that's all, folks!"

.PHONY: clean
clean: 
	IF EXIST "work_folder\05_geocoder" RMDIR "work_folder\05_geocoder" /S /Q	
	IF EXIST "work_folder\07_building_data" RMDIR "work_folder\07_building_data" /S /Q	
	IF EXIST "work_folder\10_osm_extracts" RMDIR "work_folder\10_osm_extracts" /S /Q	
	IF EXIST "work_folder\20_osm_3dmodels" RMDIR "work_folder\20_osm_3dmodels" /S /Q
	IF EXIST "work_folder\21_osm_objects_list" RMDIR "work_folder\21_osm_objects_list" /S /Q	
	IF EXIST "work_folder\22_all_osm_objects_list" RMDIR "work_folder\22_all_osm_objects_list" /S /Q	
	IF EXIST "work_folder\30_3dmodels" RMDIR "work_folder\30_3dmodels" /S /Q	

.PHONY: planet-update
planet-update: work_folder\00_planet.osm\russia-latest.osm.pbf work_folder\00_planet.osm\russia.poly  ## update source osm file	
	echo "update osm file" 
	scripts\planet_update.bat work_folder\00_planet.osm	
	
#****************************************************************************************************************************
#* __ Prepare quadrants/regions list
#****************************************************************************************************************************		
work_folder: ## make the working folder 
	mkdir work_folder	
	
work_folder\Quadrants.dat: | work_folder ## initialize quadrant summary file 
	copy Quadrants.dat work_folder	
	
#****************************************************************************************************************************
#* 00 fetch and update source OSM data  
#****************************************************************************************************************************
work_folder\00_planet.osm:  | work_folder ## make folder for source osm data
	mkdir work_folder\00_planet.osm	

work_folder\00_planet.osm\russia-latest.osm.pbf: | work_folder\00_planet.osm ##download source osm file
	echo "download source osm file"
	scripts\planet_download.bat $(@D)

work_folder\00_planet.osm\russia.poly: | work_folder\00_planet.osm ## prepare poly file 
	copy poly\russia.poly work_folder\00_planet.osm
	
#update osm file 
work_folder\00_planet.osm\russia-latest.o5m: work_folder\00_planet.osm\russia-latest.osm.pbf work_folder\00_planet.osm\russia.poly  ## update source osm file	
	echo "update osm file" 
	scripts\planet_update.bat $(@D)

#****************************************************************************************************************************
#* 05 Create geocoder files 
#****************************************************************************************************************************
work_folder\05_geocoder: | work_folder ## prepare geocoder folder 
	mkdir work_folder\05_geocoder
	
work_folder\05_geocoder\geocoder.osm: work_folder\00_planet.osm\russia-latest.o5m | work_folder\05_geocoder ## create geocoder osm file
	scripts\geocoder_extract.bat work_folder\05_geocoder work_folder\00_planet.osm

work_folder\05_geocoder\geocoder.txt: work_folder\05_geocoder\geocoder.osm  ##create geocoder mp file. Actually geocoder txt should be created from geocode.osm, but the script was lost. 	
	copy geocoder.txt work_folder\05_geocoder
	touch $@

#****************************************************************************************************************************
#* 07 Extract building data 
#****************************************************************************************************************************	
work_folder\07_building_data: | work_folder ## make folder for building data
	mkdir work_folder\07_building_data	

work_folder\07_building_data\objects-with-parts.osm: work_folder\00_planet.osm\russia-latest.o5m |  work_folder\07_building_data
	scripts\buildings_extract.bat
	
#****************************************************************************************************************************
#* 10 Make region/quadrant extracts
#****************************************************************************************************************************	
work_folder\10_osm_extracts: | work_folder ## make folder for extracted osm buildings 
	mkdir work_folder\10_osm_extracts	

work_folder\10_osm_extracts\extract_osm_data: work_folder\07_building_data\objects-with-parts.osm  | work_folder\Quadrants.dat work_folder\10_osm_extracts ## extract osm data per region
	for /F "eol=# tokens=1 delims=|" %%i in (work_folder\Quadrants.dat) do scripts\buildings_extract-per-region.bat %%i %%i.poly
	touch $@		

#****************************************************************************************************************************
#* 20 Extract individual osm-files for 3d objecs
#****************************************************************************************************************************		
work_folder\20_osm_3dmodels: | work_folder ## make folder for extracted 3d buildings 
	mkdir work_folder\20_osm_3dmodels
	
work_folder\21_osm_objects_list: | work_folder ## make folder for osm object list (dat)
	mkdir work_folder\21_osm_objects_list
	
work_folder\22_all_osm_objects_list : | work_folder
	mkdir work_folder\22_all_osm_objects_list

work_folder\20_osm_3dmodels\extract_building_models_osm: work_folder\10_osm_extracts\extract_osm_data work_folder\05_geocoder\geocoder.txt | work_folder\21_osm_objects_list work_folder\20_osm_3dmodels ## extract osm buildings  into separate osm files
	for /F "eol=# tokens=1 delims=|" %%i in (work_folder\Quadrants.dat) do python OsmParser\main.py %%i
	touch $@
	
work_folder\22_all_osm_objects_list\all-objects.dat: work_folder\20_osm_3dmodels\extract_building_models_osm | work_folder\22_all_osm_objects_list ##join object lists from different quadrants
	python scripts\joindats.py $@ work_folder\21_osm_objects_list

work_folder\22_all_osm_objects_list\RUS_TOP.dat: work_folder\22_all_osm_objects_list\all-objects.dat
	python OsmParser\make_tops.py $@ $<

#****************************************************************************************************************************
#* 30 Convert models to x-plane obj and x3d 
#****************************************************************************************************************************		
work_folder\30_3dmodels: | work_folder ## Prepare folder for 3d models (obj/x3d)
	mkdir work_folder\30_3dmodels 
	
work_folder\30_3dmodels\convert_osm_to_obj: work_folder\20_osm_3dmodels\extract_building_models_osm | work_folder\30_3dmodels 	##Convert 3d objects from osm files to blender and x-plane obj 
	for %%v in (work_folder\20_osm_3dmodels\*.osm) do osm2blend.bat "%%v" work_folder\30_3dmodels
	touch $@		
	
work_folder\30_3dmodels\convert_obj_to_x3d: work_folder\30_3dmodels\convert_osm_to_obj              ##Convert x-plane obj files to x3d, to be used on website.  		
	for %%v in (work_folder\30_3dmodels\*.obj) do obj2x3d.py "%%v"
	touch $@		

#****************************************************************************************************************************
#* 50 create x-plane specific files, e.g dsf per quadrant. 
#****************************************************************************************************************************	
	
work_folder\50_DSF : ## Prepare folder for DSFs
	mkdir work_folder\50_DSF

work_folder\50_DSF\+56+038.dat : work_folder\22_all_osm_objects_list\all-objects.dat | work_folder\50_DSF ## recreate object list for x-plane quadrant(s)
	python scripts\filterdat.py $@ $< +56+038   
	
work_folder\50_DSF\+56+038.dsf.txt: work_folder\50_DSF\+56+038.dat	## generate dsf.txt from quadrant object list 
	python osmparser\mdlDSF.py
	
work_folder\50_DSF\+56+038.dsf: work_folder\50_DSF\+56+038.dsf.txt ## compile binary dsf from dsf-txt 
	d:\tools\xplane_tools\tools\dsftool --text2dsf  "$<" "$@"	
	
	
#****************************************************************************************************************************
#* 80 Build X-Plane scenery package
#****************************************************************************************************************************		
xplane_buildpath = work_folder\80_xplane_release\VFR_LANDMARKS_3D_RU
xplane_workpath =  work_folder\50_DSF\+56+038
  
$(xplane_buildpath):
	mkdir "$(xplane_buildpath)"	
  
work_folder\clean_xplane_release_folder: $(xplane_buildpath) ## clean up x-plane scenery folder 
	echo Cleaning the $(xplane_buildpath)
	rmdir /S /Q $(xplane_buildpath)
	touch $@
  
work_folder\init_xplane_release_folder: work_folder\clean_xplane_release_folder ## create subdirectories for x-plane scenery folder
	echo Creating the build directory structure
	mkdir "$(xplane_buildpath)"
	mkdir "$(xplane_buildpath)\Objects"
	mkdir "$(xplane_buildpath)\Objects-osm"
	mkdir "$(xplane_buildpath)\Facades"
	mkdir "$(xplane_buildpath)\Earth nav data"
	mkdir "$(xplane_buildpath)\Earth nav data\+50+030"
	touch $@
	
work_folder\copy_xplane_files: work_folder\50_DSF\+56+038.dsf work_folder\30_3dmodels\convert_osm_to_obj  work_folder\init_xplane_release_folder ## collect all the files, both generated and pre-produced into x-plane scenery folder 
	xcopy /Y /Q readme.txt $(xplane_buildpath)
	xcopy /Y /Q "Custom_models\*.obj" $(xplane_buildpath)\Objects
	xcopy /Y /Q "Custom_models\*.png" $(xplane_buildpath)\Objects
	
	xcopy /Y /Q "Facades\*.fac" $(xplane_buildpath)\Facades
	xcopy /Y /Q "Facades\*.png" $(xplane_buildpath)\Facades

	xcopy /Y /Q "work_folder\30_3dmodels\*.obj" $(xplane_buildpath)\Objects-osm
	xcopy /Y /Q "work_folder\30_3dmodels\*.png" $(xplane_buildpath)\Objects-osm
	
	xcopy /Y /Q "work_folder\50_DSF\+56+038.dsf" "$(xplane_buildpath)\Earth nav data\+50+030"	
	touch $@


work_folder\81_xplane_release_zip: ## prepare folder for zipped x-plane scenery package 
	mkdir work_folder\81_xplane_release_zip

work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip: work_folder\copy_xplane_files  | work_folder\81_xplane_release_zip ## zip x-plane scenery 
	7z a $@ work_folder\80_xplane_Release


#****************************************************************************************************************************
#* 90 Upload resulting data and models to web 
#****************************************************************************************************************************	
work_folder\90_uploads: | work_folder ## prepare uploads folder 
	mkdir work_folder\90_uploads
	
work_folder\90_uploads\upload_models_to_web: work_folder\30_3dmodels\convert_obj_to_x3d work_folder\22_all_osm_objects_list\RUS_TOP.dat | work_folder\90_uploads 	##Upload 3d models and dat files to web (validator)  
	scripts\upload.bat
	touch $@		

work_folder\90_uploads\upload_xplane_release_to_web : work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip	| work_folder\90_uploads ## upload x-plane scenery package to web
	xcopy /Y /Q "work_folder\81_xplane_release_zip\VFR_LANDMARKS_3D_RU.zip"   "3dcheck\downloads"
	touch $@
	
#****************************************************************************************************************************
#* Finish 
#****************************************************************************************************************************	
	
fin: work_folder\90_uploads\upload_models_to_web work_folder\90_uploads\upload_xplane_release_to_web ##final target
	echo "All done"