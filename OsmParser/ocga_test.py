from ocga_engine import ocga_process

from ocga_samples.main_cathedral_of_russian_army_ocga import checkRulesMy as checkRules1
from ocga_samples.church_of_st_louis_ocga import checkRulesMy as checkRules2
from ocga_samples.gorky_park_entrance_ocga import checkRulesMy as checkRules3
from ocga_samples.gorky_park_rotunda_ocga import checkRulesMy as checkRules4
from ocga_samples.tsaritsino_rotunda_ocga import checkRulesMy as checkRules5

print("ocga test")
SAMPLES_DIR="d:\\_VFR_LANDMARKS_3D_RU\\OsmParser\\ocga_samples"
OUTPUT_DIR="d:\\_VFR_LANDMARKS_3D_RU\\OsmParser\\ocga_output"

# objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
# objOsmGeom, Objects = readOsmXml("d:\\egorievsk.osm")

ocga_process(SAMPLES_DIR + "/main_cathedral_of_russian_army.osm",
             OUTPUT_DIR + "/main_cathedral_of_russian_army-rewrite.osm",
             checkRules1)

ocga_process(SAMPLES_DIR + "/church_of_st_louis.osm",
             OUTPUT_DIR + "/church_of_st_louis-rewrite.osm",
             checkRules2)

ocga_process(SAMPLES_DIR + "/gorky_park_entrance.osm",
             OUTPUT_DIR + "/gorky_park_entrance-rewrite.osm",
             checkRules3)

ocga_process(SAMPLES_DIR + "/gorky_park_rotunda.osm",
             OUTPUT_DIR + "/gorky_park_rotunda-rewrite.osm",
             checkRules4)

ocga_process(SAMPLES_DIR + "/tsaritsino_rotunda.osm",
             OUTPUT_DIR + "/tsaritsino_rotunda-rewrite.osm",
             checkRules5)

print("done")