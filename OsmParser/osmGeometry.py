#***********************************************************************************************************************
# some arrays to store osm-geometry
# we need this geometry to determine bboxes of objects and find building parts
#***********************************************************************************************************************
from vbFunctions import *
DEGREE_LENGTH_M = 111.13 * 1000
Pi = 3.14159265358979

class TBbox:
    def __init__(self):
        self.minLat = 0
        self.maxLat = 0
        self.minLon = 0
        self.maxLon = 0

class TNode:
    def __init__(self):
        self.id = ""
        self.lat = 0.0
        self.lon = 0.0

class TWay:
    def __init__(self):
        self.id = ""
        self.node_count = 0
        self.NodeRefs = []
        self.minLat = 0.0
        self.maxLat = 0.0
        self.minLon = 0.0
        self.maxLon = 0.0

class clsOsmGeometry():
    """coordinates of nodes"""


    def __init__(self):
        self.nodes = []
        self.nodehash = {}
        self.ways = []
        self.wayhash = {}
        self.max_node = -1
        self.max_way = -1

    def AddNode(self, id, lat, lon):
        #Debug.Print id, lat, lon
        aNode=TNode()
        aNode.id = id
        aNode.lat = float(lat)
        aNode.lon = float(lon)
        self.nodes.append(aNode)

        self.max_node = self.max_node + 1
        self.nodehash[id]=self.max_node

    def FindNode(self, id):
        #i = 0
        #blnFound = False
        #for i in range(0, self.max_node+1):
        #    if self.nodes[i].id == id:
        #        fn_return_value = i
        #        blnFound = True
        #        break
        #if not blnFound:
        #    #print("node id " + id + "not found!") 
        #    fn_return_value = - 1
        #return fn_return_value
        return self.nodehash.get(id,-1)

    def GetNodeID(self, intNodeNo):
        fn_return_value = self.nodes[intNodeNo].id
        return fn_return_value

    def GetNodeLat(self, intNodeNo):
        fn_return_value = self.nodes[intNodeNo].lat
        return fn_return_value

    def GetNodeLon(self, intNodeNo):
        fn_return_value = self.nodes[intNodeNo].lon
        return fn_return_value

    def AddWay(self, id, NodeRefs, node_count):
        i = 0

        lat = 0
        lon = 0
        minLat = 0
        minLon = 0
        maxLat = 0
        maxLon = 0
        #save id
        aWay= TWay()
        self.ways.append(aWay)
        self.max_way = self.max_way + 1
        self.ways[self.max_way].id = id
        self.wayhash[id] = self.max_way
        #save node refs
        self.ways[self.max_way].NodeRefs = []
        for i in range(node_count):
            self.ways[self.max_way].NodeRefs.append( NodeRefs[i])
        self.ways[self.max_way].node_count = node_count
        #calculate bbox
        for i in range(node_count):
            lat = self.nodes[self.ways[self.max_way].NodeRefs[i]].lat
            lon = self.nodes[self.ways[self.max_way].NodeRefs[i]].lon
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
        self.ways[self.max_way].minLat = minLat
        self.ways[self.max_way].minLon = minLon
        self.ways[self.max_way].maxLat = maxLat
        self.ways[self.max_way].maxLon = maxLon
        fn_return_value = self.max_way
        return fn_return_value

    def GetWayBBox(self, intWayNo):
        bbox = TBbox()
        bbox.minLat = self.ways[intWayNo].minLat
        bbox.minLon = self.ways[intWayNo].minLon
        bbox.maxLat = self.ways[intWayNo].maxLat
        bbox.maxLon = self.ways[intWayNo].maxLon
        fn_return_value = bbox
        return fn_return_value

    def FindWay(self, id):
        #i = 0
        #blnFound = False
        #for i in range(self.max_way+1):
        #    if self.ways[i].id == id:
        #        fn_return_value = i
        #        blnFound = True
        #        break
        #if not blnFound:
        #    fn_return_value = - 1
        #return fn_return_value
        return self.wayhash.get(id,-1)

    def GetWayID(self, intWayNo):
        fn_return_value = self.ways[intWayNo].id
        return fn_return_value

    def GetWayNodeRefsAndCount(self, intWayNo):
        #anode_count = self.ways(intWayNo).node_count
        return self.ways[intWayNo].NodeRefs

    def CalculateBBoxSize(self, minLat, minLon, maxLat, maxLon):
        #Debug.Print DEGREE_LENGTH_M * (maxLat - minLat), DEGREE_LENGTH_M * (maxLon - minLon) * Cos(minLatn / 180 * Pi)
        CalculateSize = self.DEGREE_LENGTH_M * Sqr(Abs(maxLat - minLat) * Abs(maxLon - minLon) * Cos(minLat / 180 * self.Pi))
        CalculateSize = Round(CalculateSize)
        return fn_return_value

    def CalculateClosedNodeChainSqure(self, NodeRefs, N):
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
            y0 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i]].lon - ZeroLon )  * Cos(ZeroLat / 180 * Pi)
            x1 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i + 1]].lat - ZeroLat )
            y1 = DEGREE_LENGTH_M *  ( self.nodes[NodeRefs[i + 1]].lon - ZeroLon )  * Cos(ZeroLat / 180 * Pi)
            S = S +  ( x0 * y1 - y0 * x1 )
        S = Abs(S / 2)
        fn_return_value = S
        return fn_return_value

    def CalculateWaySize(self, intWayNo):
        bbox = TBbox()

        N = 0
        bbox = self.GetWayBBox(intWayNo)
        N = len(self.ways[intWayNo].NodeRefs)-1
        if self.ways[intWayNo].NodeRefs[0] != self.ways[intWayNo].NodeRefs[N]:
            # Debug.Print "way not closed " & ways(intWayNo).ID
            fn_return_value = DEGREE_LENGTH_M * Sqr(Abs(bbox.maxLat - bbox.minLat) * Abs(bbox.maxLon - bbox.minLon) * Cos(( bbox.minLat + bbox.maxLat )  / 2.0 / 180 * Pi))
        else:
            # Debug.Print "way  closed"
            fn_return_value = Sqr(self.CalculateClosedNodeChainSqure(self.ways[intWayNo].NodeRefs, N))
        #CalculateWaySize = Round(CalculateWaySize)
        return fn_return_value

    def ExtractCloseNodeChainFromRelation(self, WayRefs):

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
                if role == 'outer':
                    w_NodeRefs=self.GetWayNodeRefsAndCount(wayno)
                    w_node_count=len(w_NodeRefs)
                    if firstNodeId != - 1:
                        PrevFirstNodeId = OutlineNodeRefs[0]
                        PrevLastNodeId = OutlineNodeRefs[outline_nodeCount - 1]
                    else:
                        PrevFirstNodeId = firstNodeId
                        PrevLastNodeId = lastNodeId
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
                Outlines.append(OutlineNodeRefs)
                #re-initialize
                k=0
                OutlineNodeRefs=[]
                outline_nodeCount=0
                firstNodeId = - 1
                lastNodeId = - 1

        return Outlines

    def CalculateRelationSize(self, WayRefs, way_count):
        size = 0.0
        Outlines=self.ExtractCloseNodeChainFromRelation(WayRefs)

        if len(Outlines) > 0:
            for OutlineNodeRefs in Outlines:
                outline_nodeCount = len(OutlineNodeRefs)
                if OutlineNodeRefs[0] == OutlineNodeRefs[outline_nodeCount - 1]:
                    size =size + Sqr(self.CalculateClosedNodeChainSqure(OutlineNodeRefs, outline_nodeCount - 1))
                else:
                    print('Relation is not closed')
        else:
            print('Empty relation. Probably members with outer role is missing or no closed rings ')
        return size