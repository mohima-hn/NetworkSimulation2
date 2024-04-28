# prepare the linkUsage.json file from simulation result
# @author Mohima Hossain
# date :
import json
import csv
import re
import json

import networkx as nx
import random

# J = nx.read_gml("graph.txt", destringizer=int)
# data1 = nx.node_link_data(J)
# # print(json.dumps(data1, indent=4))
# # print(json.dumps(data1["links"], indent=4))
# links = data1["links"]
# routerDict = {}
# for i in range(len(links)):
#     source = 'router' + str(links[i]['source'])
#     port = 'ppp[' + str(links[i]['port']) + ']'
#     if not source in routerDict:
#         routerDict[source] = {}
#     routerDict[source][port] = links[i]
# print(json.dumps(routerDict, indent=4))



with open('graph_gate.json') as user_file:
    file_contents = user_file.read()
routerDict = json.loads(file_contents)
# print(json.dumps(routerDict, indent=4))


with open('results/router.json') as user_file:
    file_contents = user_file.read()
jsonData = json.loads(file_contents)
jsonObj = next(iter(jsonData.values())) # get the object under 'General-0-<datetimestamp>' key
scalarArr = jsonObj['scalars']
configArr = jsonObj['config']
routerwiseData = {}
configObj = {}
for i in range(len(configArr)):
    item = configArr[i]  # a json object
    key, value = next(iter(item.items()))
    configObj[key] = value
    # print(configObj[key])
    # print(json.dumps(configObj, indent=4))

# print(configObj['sim-time-limit'])

for i in range(len(scalarArr)):
    item = scalarArr[i]  # a json object
    moduleName = item['module']  # NetworkSimulation2.router5.ppp[0].queue.fifo
    parts = moduleName.split('.')  # [NetworkSimulation2, router5 , ppp[0], queue ,fifo
    routerName = parts[1]
    type = parts[2]

    if routerName.startswith('router'):
        routerData = routerwiseData.get(routerName, {})

        if type.startswith('ppp'):
            typeData = routerData.get(type, {})
            itemName = item['name']  # packetSent:count
            itemValue = item['value']  # 6031
            typeData[itemName] = itemValue
            # update routerData mapping
            routerData[type] = typeData

        routerwiseData[routerName] = routerData
# print(json.dumps(routerwiseData, indent=4))

linkResult = {}  # an empty json object with an empty array
links = []

for routerName in routerwiseData.keys():
    # print(routerName)
    routerData = routerwiseData[routerName]
    # print(json.dumps(routerData, indent=4))
    for type in routerData.keys():
        typeData = routerData[type]
        flows_obj = {}
        # Link Utilization = Amount of data sent/Max. amount of data that could be sent.
        flows_obj['avg_utilization'] = routerwiseData[routerName][type]['outgoingPacketLengths:sum']/routerDict[routerName][type]['bandwidth']
        drppackQ = routerwiseData[routerName][type]['droppedPacketsQueueOverflow:count']
        r = str(configObj['sim-time-limit'])
        stime = ''.join(x for x in r if x.isdigit())
        # print(int(stime))
        if drppackQ is not None:
            flows_obj['avg_packets_lost'] = drppackQ/int(stime)
        else:
            flows_obj['avg_packets_lost'] = 0
        flows_obj['avg_packet_size'] = routerwiseData[routerName][type]['queueBitLength:timeavg']/16000
        flows_obj['src'] = routerDict[routerName][type]['source']
        flows_obj['dst'] = routerDict[routerName][type]['target']
        flows_obj['port'] = routerDict[routerName][type]['port']
        flows_obj['host'] = ''

        links.append(flows_obj)

linkResult['links'] = links
# print(json.dumps(linkResult, indent=4))


f = open("results/linkUsage.json", "w")
f.write(json.dumps(linkResult, indent=4))
f.close()

