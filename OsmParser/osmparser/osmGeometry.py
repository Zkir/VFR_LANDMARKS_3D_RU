#***********************************************************************************************************************
# some arrays to store osm-geometry
# we need this geometry to determine bboxes of objects and find building parts
#***********************************************************************************************************************
DEGREE_LENGTH_M = 111.13 * 1000
from math import cos
Pi = 3.14159265358979

def Sqr(x):
    return (x**0.5)

class TBbox:
    def __init__(self):
        self.minLat = 0
        self.maxLat = 0
        self.minLon = 0
        self.maxLon = 0
        
    def __str__(self):
        return str(self.minLat) + ", " + str(self.minLon) + ", " + str(self.maxLat) + ", " + str(self.maxLon) 

class TNode:
    def __init__(self):
        self.id = "-1"
        self.lat = 0.0
        self.lon = 0.0
        self.version = '-1' 
        self.timestamp = '1900-01-01'
        self.osmtags = {}

class TWay:
    def __init__(self):
        self.id = "-1"
        self.node_count = 0
        self.NodeRefs = []
        self.minLat = 0.0
        self.maxLat = 0.0
        self.minLon = 0.0
        self.maxLon = 0.0
        self.version = '-1' 
        self.timestamp = '1900-01-01'
        self.osmtags = {}
        
    def getBbox(self):
        bbox = TBbox()
        bbox.minLat = self.minLat
        bbox.minLon = self.minLon
        bbox.maxLat = self.maxLat
        bbox.maxLon = self.maxLon    
        return bbox
        
class TRelation:
    def __init__(self):
        self.id = "-1"
        self.way_count = 0
        self.WayRefs = []
        self.minLat = 0.0
        self.maxLat = 0.0
        self.minLon = 0.0
        self.maxLon = 0.0
        self.version = '-1' 
        self.timestamp = '1900-01-01'
        self.osmtags = {}        
        
    def getBbox(self):
        bbox = TBbox()
        bbox.minLat = self.minLat
        bbox.minLon = self.minLon
        bbox.maxLat = self.maxLat
        bbox.maxLon = self.maxLon    
        return bbox    

class clsOsmGeometry():
    """coordinates of nodes"""
    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def AddNode(self, id, lat, lon, version="1", timestamp="1900-01-01"):
        #print("debug",id, lat, lon)
        aNode=TNode()
        aNode.id = id
        aNode.lat = float(lat)
        aNode.lon = float(lon)
        
        aNode.version = version 
        aNode.timestamp = timestamp
        
        self.nodes[id] = aNode
        return id
        

    #To be deleted
    def FindNode(self, node_id):
        if node_id in self.nodes:
            return node_id
        else:
            return None            

    def GetNodeID(self, intNodeNo):
        return self.nodes[intNodeNo].id

    def GetNodeLat(self, intNodeNo):
        return self.nodes[intNodeNo].lat

    def GetNodeLon(self, intNodeNo):
        return self.nodes[intNodeNo].lon

    def AddWay(self, id, version, timestamp, osmtags, NodeRefs, object_incomplete):
        i = 0

        lat = 0
        lon = 0
        minLat = 0
        minLon = 0
        maxLat = 0
        maxLon = 0
        node_count = len(NodeRefs)
        
        aWay = TWay()
        
        #save basic attibutes
        aWay.id = id
        aWay.version = version 
        aWay.timestamp = timestamp
        aWay.osmtags = osmtags
        aWay.NodeRefs = NodeRefs
        aWay.node_count = node_count
        aWay.object_incomplete = object_incomplete
        
        #calculate bbox
        for i in range(node_count):
            
            lat = self.nodes[aWay.NodeRefs[i]].lat
            lon = self.nodes[aWay.NodeRefs[i]].lon
            if i == 0:
                minLat = lat
                minLon = lon
                maxLat = lat
                maxLon = lon
            else:
                if lat < minLat:
                    minLat = lat
                if lat > maxLat:
                    maxLat = lat
                if lon < minLon:
                    minLon = lon
                if lon > maxLon:
                    maxLon = lon
                    
        #store bbox
        aWay.minLat = minLat
        aWay.minLon = minLon
        aWay.maxLat = maxLat
        aWay.maxLon = maxLon
        
        aWay.size = self.CalculateWaySize(aWay)

        self.ways[id] = aWay
        
        return id

    def GetWayBBox(self, intWayNo):
        bbox = self.ways[intWayNo].getBbox()
        return bbox

    def FindWay(self, way_id):
        if way_id in self.ways:
            return way_id
        else:
            return None

    def GetWayID(self, intWayNo):
        return self.ways[intWayNo].id

    def GetWayNodeRefsAndCount(self, intWayNo):
        #anode_count = self.ways(intWayNo).node_count
        return self.ways[intWayNo].NodeRefs

    def CalculateBBoxSize(self, minLat, minLon, maxLat, maxLon):
        #Debug.Print DEGREE_LENGTH_M * (maxLat - minLat), DEGREE_LENGTH_M * (maxLon - minLon) * cos(minLatn / 180 * Pi)
        CalculateSize = DEGREE_LENGTH_M * Sqr(abs(maxLat - minLat) * abs(maxLon - minLon) * cos(minLat / 180 * Pi))
        CalculateSize = round(CalculateSize, 3)
        return CalculateSize

    def CalculateClosedNodeChainArea(self, NodeRefs, N):
        S = 0
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 0
        i = 0
        ZeroLat = 0
        ZeroLon = 0
        S = 0
        ZeroLat = self.nodes[NodeRefs[0]].lat
        ZeroLon = self.nodes[NodeRefs[0]].lon
        if NodeRefs[0] != NodeRefs[N]:
            print('node chain not closed!')
        for i in range(N):
            #s = s + (a[i].x*a[i+1].y - a[i].y*a[i+1].x);

            x0 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i]].lat - ZeroLat )
            y0 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i]].lon - ZeroLon )  * cos(ZeroLat / 180 * Pi)
            x1 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i + 1]].lat - ZeroLat )
            y1 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i + 1]].lon - ZeroLon )  * cos(ZeroLat / 180 * Pi)
            S = S +  ( x0 * y1 - y0 * x1 )
        S = abs(S / 2)
        fn_return_value = S
        return fn_return_value

    def CalculateWaySize(self, way):

        bbox = way.getBbox() #self.GetWayBBox(intWayNo)
        N = len(way.NodeRefs)-1
        #print(N)
        if N<0:
            print("Way without nodes: " + way.id)
            return 0.0
    
        if way.NodeRefs[0] != way.NodeRefs[N]:
            fn_return_value = DEGREE_LENGTH_M * Sqr(abs(bbox.maxLat - bbox.minLat) * abs(bbox.maxLon - bbox.minLon) * cos(( bbox.minLat + bbox.maxLat )  / 2.0 / 180 * Pi))
        else:
            fn_return_value = Sqr(self.CalculateClosedNodeChainArea(way.NodeRefs, N))
        return fn_return_value


    def ExtractCloseNodeChainsFromRelation(self, WayRefs):

        i = 0
        j = 0


        firstNodeId = 0
        lastNodeId = 0
        PrevFirstNodeId = 0
        PrevLastNodeId = 0
        theVeryFirstNodeId = 0
        theVeryLastNodeId = 0

        w_NodeRefs = []
        w_node_count = 0
        w_node_id = ""
        w_node_lat = 0
        w_node_lon = 0
        OutlineNodeRefs = []
        outline_nodeCount = 0
        Outlines=[]
        blnRelationClosed = False
        blnReverseOrder = False
        blnInsertIntoBeginning = False
        #check continuity
        blnRelationClosed = True
        outline_nodeCount = 0
        firstNodeId = - 1
        lastNodeId = - 1
        k = 0
        way_numbers=list(range(len(WayRefs))) #we need just indices instead of list of way refs
        while len(way_numbers)>0:
            for i in way_numbers:
                wayno=WayRefs[i][0]
                role=WayRefs[i][1]
                if role == 'outer' or role == 'inner':
                    w_NodeRefs=self.GetWayNodeRefsAndCount(wayno)
                    w_node_count=len(w_NodeRefs)
                    if firstNodeId != - 1:
                        PrevFirstNodeId = OutlineNodeRefs[0]
                        PrevLastNodeId = OutlineNodeRefs[outline_nodeCount - 1]
                    else:
                        PrevFirstNodeId = firstNodeId
                        PrevLastNodeId = lastNodeId
                    if len(w_NodeRefs)<1:
                        print("Relation is strangely broken")
                    firstNodeId = w_NodeRefs[0]
                    lastNodeId = w_NodeRefs[w_node_count - 1]
                    if k == 0:
                        theVeryFirstNodeId = firstNodeId
                        theVeryLastNodeId = lastNodeId
                        blnInsertIntoBeginning = False
                        k=1 # dirty trick. We need to know that it is no longer first way.

                    else:
                        if firstNodeId == PrevLastNodeId:
                            #Debug.Print "continuation found, direct order"
                            blnReverseOrder = False
                            blnInsertIntoBeginning = False
                        elif lastNodeId == PrevLastNodeId:
                            #Debug.Print "continuation found, reverse order"
                            blnReverseOrder = True
                            blnInsertIntoBeginning = False
                            firstNodeId = w_NodeRefs[w_node_count - 1]
                            lastNodeId = w_NodeRefs[0]
                        elif  ( firstNodeId == PrevFirstNodeId )  or  ( lastNodeId == PrevFirstNodeId ) :
                            # opposite directions of the first two ways!
                            # We need to insert into the beginning
                            if firstNodeId == PrevFirstNodeId:
                                blnReverseOrder = True
                            else:
                                blnReverseOrder = False
                            blnInsertIntoBeginning = True
                            for j in range(w_node_count-1 , -1, - 1):
                                OutlineNodeRefs.insert(0,0)
                                #OutlineNodeRefs[j + w_node_count] = OutlineNodeRefs[j]
                                #OutlineNodeRefs[j] = 0
                            outline_nodeCount = outline_nodeCount + w_node_count
                        else:
                            #print('relation is not sorted?')
                            continue #we should try other members, may be they are not sequential
                    if not blnReverseOrder:
                        for j in range(w_node_count):
                            #'w_node_id = GetNodeID(w_NodeRefs(j))
                            #'Debug.Print w_node_id
                            if blnInsertIntoBeginning:
                                OutlineNodeRefs[j] = w_NodeRefs[j]
                            else:
                                OutlineNodeRefs.append(w_NodeRefs[j])
                                outline_nodeCount = outline_nodeCount + 1
                    else:
                        for j in range(w_node_count - 1, -1, - 1):
                            #'w_node_id = GetNodeID(w_NodeRefs(j))
                            #'Debug.Print w_node_id
                            if blnInsertIntoBeginning:
                                OutlineNodeRefs[w_node_count - 1 - j] = w_NodeRefs[j]
                            else:
                                OutlineNodeRefs.append( w_NodeRefs[j])
                                outline_nodeCount = outline_nodeCount + 1
                # we can exit cycle, because  we have found some way to continue chain
                # and we should remove this way from the list of unprocessed relation members
                way_numbers.remove(i)
                break
            else:
                #we have NOT found any way to continue chain
                print('relation is broken')
                break # nothing else to analyze

            if (k>0) and (OutlineNodeRefs[0] == OutlineNodeRefs[outline_nodeCount - 1]):
                #print("ring closed")
                Outlines.append((OutlineNodeRefs, role))
                #re-initialize
                k=0
                OutlineNodeRefs=[]
                outline_nodeCount=0
                firstNodeId = - 1
                lastNodeId = - 1

        return Outlines

    def CalculateRelationSize(self, id, type, WayRefs):
        
        if type not in ["boundary", "multipolygon"]:
            # other known types of relations are 'site', 'collection', 'waterway' and 'building'! 
            # we do not know how to calculate size for them, and do not really care. 
            return None
        Outlines=self.ExtractCloseNodeChainsFromRelation(WayRefs)

        if len(Outlines) > 0:
            area = 0.0
            for OutlineNodeRefs_with_roles in Outlines:
                OutlineNodeRefs= OutlineNodeRefs_with_roles[0]
                role = OutlineNodeRefs_with_roles[1]
                outline_nodeCount = len(OutlineNodeRefs)
                if OutlineNodeRefs[0] == OutlineNodeRefs[outline_nodeCount - 1]:
                    outline_area = self.CalculateClosedNodeChainArea(OutlineNodeRefs, outline_nodeCount - 1)
                    if role == 'outer':
                        area = area + outline_area
                    elif role =='inner':    
                        area = area - outline_area
                    else: 
                        print('Relation r' + id + ' ('+type+') has unknown role '+role)
                else:
                    print('Relation r' + id + ' ('+type+') is broken. One of the rings is not closed')
        else:
            area = 0  
            print('Relation r' + id + ' ('+type+') is empty. Probably members with outer role is missing or no closed rings ')
        
        if area<0:
            area = 0
            print('Relation r' + id + ' ('+type+') has negative area. Probably outer members are missing.')
            
        
        return Sqr(area) 
        
        
    def AddRelation(self, id, version, timestamp, osmtags, WayRefs, object_incomplete):

        way_count = len(WayRefs)
        aRelation = TRelation()
        aRelation.id = id
        aRelation.version = version 
        aRelation.timestamp = timestamp
        aRelation.osmtags = osmtags
        aRelation.WayRefs =  WayRefs
        aRelation.way_count = way_count
        aRelation.object_incomplete = object_incomplete
        aRelation.type = osmtags.get("type","")
        aRelation.size = self.CalculateRelationSize(id, aRelation.type, WayRefs)

        #calculate bbox
        minLat = 0
        minLon = 0
        maxLat = 0
        maxLon = 0  
        
        for i in range(way_count):
            waybbox = self.GetWayBBox(WayRefs[i][0])
            
            if i == 0:
                minLat = waybbox.minLat
                minLon = waybbox.minLon
                maxLat = waybbox.maxLat
                maxLon = waybbox.maxLon
            else:
                if waybbox.minLat < minLat:
                    minLat = waybbox.minLat
                if waybbox.maxLat > maxLat:
                    maxLat = waybbox.maxLat
                if waybbox.minLon < minLon:
                    minLon = waybbox.minLon
                if waybbox.maxLon > maxLon:
                    maxLon = waybbox.maxLon
                    
        #store bbox
        aRelation.minLat = minLat
        aRelation.minLon = minLon
        aRelation.maxLat = maxLat
        aRelation.maxLon = maxLon        
        
        self.relations[id] = aRelation
        
        return id
        
    def GetRelationBBox(self, intRelationNo):
        bbox = TBbox()
        bbox.minLat = self.relations[intRelationNo].minLat
        bbox.minLon = self.relations[intRelationNo].minLon
        bbox.maxLat = self.relations[intRelationNo].maxLat
        bbox.maxLon = self.relations[intRelationNo].maxLon
        return bbox    