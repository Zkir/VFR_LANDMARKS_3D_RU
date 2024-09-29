"""
osm parser to read osm files
"""

# init file for ocgaparser package
from osmparser.main import readOsmXml0
from osmparser.osmGeometry import TBbox as Bbox 
from osmparser.mdlXmlParser import encodeXmlString
from osmparser.osmGeometry  import DEGREE_LENGTH_M
