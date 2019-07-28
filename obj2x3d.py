# =======================================================================================================================
# Converter X-plane OBJ to X3D
# =======================================================================================================================
import sys

class OBJVT:
    x = 0
    y = 0
    z = 0
    nx = 0
    ny = 0
    nz = 0
    u = 0
    v = 0


#strInputFile = "d:\models-osm\R7464383.obj"
#strInputFile =  "d:\models-osm\R3030568.obj"
strInputFile =sys.argv[1]

#strInputFile = "d:/test/Cube.obj"
#strOutputFile = "test.x3d"
#print(len(sys.argv))
if len(sys.argv)>2:
    strOutputFile =sys.argv[2]
else:
    if (strInputFile[len(strInputFile)-4:len(strInputFile):]) == ".obj":
        strOutputFile = strInputFile[0:len(strInputFile)-4] + '.x3d'
    else:
        strOutputFile=strInputFile + '.x3d'

print("Converter X-plane OBJ to X3D")
print("(c) Zkir 2019")
print("Input file: "+ strInputFile )
filehandle = open(strInputFile, 'r')
vertices = []
indices =[]
strTexture=""


txt = filehandle.readline()
while len(txt) != 0:

    txt=txt.replace("\t"," ")
    if txt[0:8] == "TEXTURE ":
        strTexture = txt.strip().split(" ")[1]

    if txt[0:3] == "VT ":
        #print("="+ txt[0:3]+"=" )
        vt = OBJVT()
        vt.x =txt.strip().split(" ")[1]
        vt.y =txt.strip().split(" ")[2]
        vt.z =txt.strip().split(" ")[3]
        vt.nx =txt.strip().split(" ")[4]
        vt.ny =txt.strip().split(" ")[5]
        vt.nz =txt.strip().split(" ")[6]
        vt.u =txt.strip().split(" ")[7]
        vt.v =txt.strip().split(" ")[8]
        #print(vt.x,vt.y, vt.z)
        vertices.append(vt)

    if txt[0:6] == "IDX10 ":
        idx0 = txt.strip().split(" ")[1]
        idx1 = txt.strip().split(" ")[2]
        idx2 = txt.strip().split(" ")[3]
        idx3 = txt.strip().split(" ")[4]
        idx4 = txt.strip().split(" ")[5]
        idx5 = txt.strip().split(" ")[6]
        idx6 = txt.strip().split(" ")[7]
        idx7 = txt.strip().split(" ")[8]
        idx8 = txt.strip().split(" ")[9]
        idx9 = txt.strip().split(" ")[10]
        #print(idx0, idx1, idx9)

        indices.append(idx0)
        indices.append(idx1)
        indices.append(idx2)
        indices.append(idx3)
        indices.append(idx4)
        indices.append(idx5)
        indices.append(idx6)
        indices.append(idx7)
        indices.append(idx8)
        indices.append(idx9)

    if txt[0:4] == "IDX ":
        idx0 = txt.strip().split(" ")[1]
        #print(idx0)
        indices.append(idx0)
    txt = filehandle.readline()
    # end of while

print ("Vertices read: "+ str(len(vertices)))
print ("Indices read: "+ str(len(indices)))
filehandle.close()

print("Output file: "+ strOutputFile )

filehandle = open(strOutputFile, 'w')
filehandle.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
filehandle.write("<!DOCTYPE X3D PUBLIC \"ISO//Web3D//DTD X3D 3.0//EN\" \"http://www.web3d.org/specifications/x3d-3.0.dtd\">\n")
filehandle.write("<X3D version=\"3.0\" profile=\"Immersive\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema-instance\" xsd:noNamespaceSchemaLocation=\"http://www.web3d.org/specifications/x3d-3.0.xsd\">\n")
filehandle.write("  <head>")
filehandle.write("    <meta name=\"filename\" content=\"R8755333-2.x3d\" />\n")
filehandle.write("    <meta name=\"generator\" content=\"obj2x3d by Zkir\" />\n")
filehandle.write("  </head>\n")
filehandle.write("  <Scene>\n")
filehandle.write("    <Viewpoint position=\"-43.20339 23.75755 -40.43003\"\n")
filehandle.write("               orientation=\"0.01690 0.99435 0.10476 3.94177\"\n")
filehandle.write("               description=\"defaultX3DViewpointNode\">\n")
filehandle.write("    </Viewpoint>\n")
filehandle.write("    <NavigationInfo headlight=\"true\"\n")
filehandle.write("                    visibilityLimit=\"0.0\"\n")
filehandle.write("                    type='\"EXAMINE\", \"ANY\"'\n")
filehandle.write("                    avatarSize=\"0.25, 1.75, 0.75\"\n")
filehandle.write("                    />\n")
filehandle.write("    <Background DEF=\"WO_World\"\n")
filehandle.write("                    groundColor=\"1 1 1\"\n")
filehandle.write("                    skyColor=\"1 1 1\"\n")
filehandle.write("		               />\n")


filehandle.write("      <Shape>\n")
filehandle.write("        <Appearance>\n")
if strTexture != "":
    filehandle.write("            <ImageTexture  url=\""+strTexture+"\" ></ImageTexture>\n")
#filehandle.write("            <Material DEF=\"MA_white\"\n")
#filehandle.write("                      diffuseColor=\"0.9 0.9 0.9\"\n")
#filehandle.write("                      specularColor=\"0.401 0.401 0.401\"\n")
#filehandle.write("                      emissiveColor=\"0.300 0.300 0.300\"\n")
#filehandle.write("                      ambientIntensity=\"0.333\"\n")
#filehandle.write("                      shininess=\"0.098\"\n")
#filehandle.write("                      transparency=\"0.0\"\n")
#filehandle.write("                      />\n")
filehandle.write("          </Appearance>\n")
filehandle.write("          <IndexedTriangleSet  solid=\"false\"\n")
filehandle.write("                               normalPerVertex=\"true\"\n")
filehandle.write("                               index=\"")
for i in range (len(indices)):
    idx=indices[i]
    #filehandle.write(str(int(idx) + 1))
    filehandle.write(idx)
    filehandle.write(" ")
#filehandle.write("0 1 2 3 4 5 6 7 8")
filehandle.write("\">\n")
filehandle.write("              <Coordinate  point=\"")

for vt in vertices:
    filehandle.write(vt.x)
    filehandle.write(" ")
    filehandle.write( vt.y)
    filehandle.write(" ")
    filehandle.write( vt.z)
    filehandle.write(" ")
filehandle.write("\"/>\n")

filehandle.write("              <Normal vector=\"")
for vt in vertices:
    filehandle.write(vt.nx)
    filehandle.write(" ")
    filehandle.write( vt.ny)
    filehandle.write(" ")
    filehandle.write( vt.nz)
    filehandle.write(" ")
filehandle.write("\"/>\n")

filehandle.write("              <TextureCoordinate point=\"")
for vt in vertices:
    filehandle.write(vt.u)
    filehandle.write(" ")
    filehandle.write( vt.v)
    filehandle.write(" ")
filehandle.write("\"/>\n")

filehandle.write("          </IndexedTriangleSet>\n")
filehandle.write("        </Shape>\n")

filehandle.write("	</Scene>\n")
filehandle.write("</X3D>")

filehandle.close()
print ("done")

