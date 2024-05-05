import json

import networkx as nx
import random

J = nx.read_gml("graph.txt", destringizer=int)
data1 = nx.node_link_data(J)
# print(json.dumps(data1, indent=4))
links = data1["links"]

routerDict = {}
for i in range(len(links)):
    source = links[i]['source']
    if not source in routerDict:
        routerDict[source] = []
    routerDict[source].append(links[i])
# print(json.dumps(routerDict, indent=4))

f = open("config.xml", "w")
buffer = ''
f.write('<?xml version="1.0"?>\n'
'<OSPFASConfig xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="OSPF.xsd" >\n'
            '<Area id="0.0.0.0" >\n'
            '       <AddressRange address="router5>router1" mask="router5>router1" status="Advertise" />\n'
            '       <AddressRange address="router1>router5" mask="router1>router5" status="Advertise" />\n'
            '       <AddressRange address="host1" mask="host1" />\n'
            '       <AddressRange address="host5" mask="host5" />\n'
            '</Area>\n\n')
buffer += ( '<Area id="0.0.0.1">\n'
            '       <AddressRange address="host4" mask="host4" />\n'
            '       <AddressRange address="host7" mask="host7" />\n'
            '       <AddressRange address="router4>router7" mask="router4>router7" />\n'
            '       <AddressRange address="router7>router4" mask="router7>router4" />\n'
            '</Area>\n\n'
            '<Area id="0.0.0.2">\n'
            '       <AddressRange address="router3>router2" mask="router3>router2" status="Advertise" />\n'
            '       <AddressRange address="router2>router3" mask="router2>router3" status="Advertise" />\n'
            '       <AddressRange address="router3>router6" mask="router3>router6" status="Advertise" />\n'
            '       <AddressRange address="router6>router3" mask="router6>router3" status="Advertise" />\n'
            '       <AddressRange address="router6>router2" mask="router6>router2" status="Advertise" />\n'
            '       <AddressRange address="router2>router6" mask="router2>router6" status="Advertise" />\n'
            '       <AddressRange address="host2" mask="host2" />\n'
            '       <AddressRange address="host3" mask="host3" />\n'
            '       <AddressRange address="host6" mask="host6" />\n'
            '</Area>\n')


for item in routerDict.keys():
        buffer += ('<Router name="router'+str(item)+'" RFC1583Compatible="true" >\n')
        for i in range(len(routerDict[item])):
            arrLength = len(routerDict[item])
            buffer += ('<PointToPointInterface ifName="ppp['+str(routerDict[item][i]["port"])+']" areaID="0.0.0.0" interfaceOutputCost="'+str(routerDict[item][i]["weight"])+'" />\n')
        buffer += ('<BroadcastInterface ifName="ppp['+str(arrLength)+']" areaID="0.0.0.1" interfaceOutputCost="1" />\n'
                   '</Router>\n\n')
buffer += ('</OSPFASConfig>\n\n')
f.write(buffer)
f.close()