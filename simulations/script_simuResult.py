# prepare the simulationResult.json file from simulation result
# @author Mohima Hossain
# date : March 5
import json
import csv
import re
import socket
import decimal


def _prepareConfig(configArr):
    configObj = {}
    for i in range(len(configArr)):
        item = configArr[i]  # a json object
        key,value = next(iter(item.items()))
        configObj[key] = value

    return configObj


def _prepareResultSkeleton(idMap):
    global_fields = ['avg_packets_per_second', 'avg_packets_lost_per_second', 'avg_packet_delay']

    simulationResult = {}  # an empty json object
    simulationResult['global'] = {}  # an empty json object
    simulationResult['flows'] = []  # an empty array
    # simulationResult['links'] = []  # an empty array

    for i in range(len(global_fields)):
        simulationResult['global'][global_fields[i]] = -1

    # for i in range(len(idMap)):
    #     flows_obj = {}
    #     for j in range(len(flows_fields)):
    #         flows_obj[flows_fields[j]] = -1
    #     simulationResult['flows'].append(flows_obj)

    return simulationResult


def _prepareScalarMetrics(idMap, scalarArr, hostwiseData):
    for i in range(len(scalarArr)):
        item = scalarArr[i]  # a json object
        moduleName = item['module']  # NetworkSimulation2.host0.[app[0]|udp]
        parts = moduleName.split('.')  # [NetworkSimulation2, host0, app[0]|udp]
        hostName = parts[1]
        type = parts[2]

        if hostName.startswith('host'):
            hostData = hostwiseData.get(hostName, {})

            if type.startswith('app') or type.startswith('udp') or type.startswith('ppp'):
                typeData = hostData.get(type, {})
                itemName = item['name']  # packetSent:count
                itemValue = item['value']  # 6031
                typeData[itemName] = itemValue

                #update hostData mapping
                hostData[type] = typeData
                hostwiseData[hostName] = hostData


def _prepareHistogramMetrics(histogramArr, hostwiseData):
    metricAttr = ['count', 'mean', 'stddev', 'min', 'max', 'sum', 'sqrsum']

    for i in range(len(histogramArr)):
        item = histogramArr[i]  # a json object
        moduleName = item['module']  # NetworkSimulation2.host0.ppp[0].queue
        parts = moduleName.split('.')  # [NetworkSimulation2, host0, ppp[0], queue]
        hostName = parts[1]
        type = parts[2]

        if hostName.startswith('host'):
            hostData = hostwiseData.get(hostName, {})
            typeData = hostData.get(type, {})

            itemName = item['name']  # queueingTime:histogram
            parts = itemName.split(':')  # [queueingTime, histogram]
            metricName = parts[0]  # queueingTime

            if not metricName == 'endToEndDelay' or type == 'app[' + str(idMap[hostName]) + ']':
                metricObj = {}
                for ma in metricAttr:
                    metricObj[ma] = item[ma]

                typeData[metricName] = metricObj
                hostData[type] = typeData
                hostwiseData[hostName] = hostData


def _populateResult(srcMap, dstMap, hostwiseData, configObj, simulationResult):
    global_fields = ['avg_packets_per_second', 'avg_packets_lost_per_second', 'avg_packet_delay']
    flows_fields = ['avg_delay',
                    'total_packets_transmitted',
                    'total_packets_lost',
                    'avg_delay',
                    'delay_variance',
                    'avg_In_delay',
                    '10_percentile_delay',
                    '20_percentile_delay',
                    '50_percentile_delay',
                    '80_percentile_delay',
                    '90_percentile_delay',
                    'sourceRouterName',
                    'src',
                    'dst',
                    'targetRouterName'
                    ]
    sum = 0

    for hostName in hostwiseData.keys():
        hostData = hostwiseData[hostName]

        for type in hostData.keys():
            typeData = hostData[type]
            if type.startswith('app'):
                flows_obj = {}

                for i in range(len(flows_fields)):
                    flows_obj[flows_fields[i]] = -1
                # flows_obj['avg_bw'] = configObj['*.' + hostName + '.' + type + '.datarate']
                flows_obj['avg_delay'] = typeData.get('endToEndDelay', {}).get('mean', -1)
                flows_obj['total_packets_transmitted'] = hostData['udp']['packetSent:count']
                flows_obj['total_packets_lost'] = typeData['dropPk:count']

                stddev = typeData.get('endToEndDelay', {}).get('stddev', -1)
                delay_variance = -1
                # if not stddev == -1:
                if stddev is not None:
                        delay_variance = stddev * stddev
                flows_obj['delay_variance'] = delay_variance
                flows_obj['avg_In_delay'] = -1
                flows_obj['10_percentile_delay'] = -1
                flows_obj['20_percentile_delay'] = -1
                flows_obj['50_percentile_delay'] = -1
                flows_obj['80_percentile_delay'] = -1
                flows_obj['sourceRouterName'] = 'router'+str(srcMap[hostName])
                flows_obj['src'] = srcMap[hostName]
                flows_obj['dst'] = dstMap[type]
                flows_obj['targetRouterName'] = 'router'+str(dstMap[type])
                simulationResult['flows'].append(flows_obj)
            # lost = 0
            # if type.startswith('ppp'):
            #     loss = hostwiseData[hostName]['ppp[0]']['droppedPacketsQueueOverflow:count']/3600
            #     print(loss)
        sum+=hostData['udp']['packetSent:count']
        # print(sum)
    global_obj = {}
                #     sum += hostData['udp']['packetSent:count']
                #     # print(sum)
                #     total_packets = sum
    global_obj['avg_packets_per_second'] = sum/3600
    global_obj['avg_packets_lost_per_second'] = -1
    global_obj['avg_packet_delay'] = -1
    # print(global_obj)
    simulationResult['global'] =global_obj

def _populateLinkResult(srcMap, dstMap, hostwiseData, configObj, simulationResult):
    links_fields = ['src',
                    'dst',
                    'avg_bw',
                    'port',
                    'avg_utilization',
                    'avg_packets_lost',
                    'avg_packet_size',
                   ]
    for hostName in hostwiseData.keys():
        hostData = hostwiseData[hostName]
        for type in hostData.keys():
            typeData = hostData[type]
            if type.startswith('ppp'):
                flows_obj = {}
                for i in range(len(links_fields)):
                    flows_obj[links_fields[i]] = -1
                flows_obj['src'] = srcMap[hostName]
                flows_obj['dst'] = -1#dstMap[type]
                flows_obj['avg_bw'] = -1#configObj['*.' + hostName + '.' + type + '.datarate']
                flows_obj['port'] = -1#configObj['**.' + hostName + '*.' + type + '.localport']
                flows_obj['avg_utilization'] = -1
                flows_obj['avg_packets_lost'] = -1
                flows_obj['avg_packet_size'] = -1#hostName+'.app[' + str(idMap[hostName]) +']'+['queueBitLength:timeavg']

                simulationResult['links'].append(flows_obj)


with open('results/result_scaler.json') as user_file:
    file_contents = user_file.read()
jsonData = json.loads(file_contents)
jsonObj = next(iter(jsonData.values())) # get the object under 'General-0-<datetimestamp>' key

idMap = {'host1': 1, 'host2': 2, 'host3': 3, 'host4': 4, 'host5': 5, 'host6': 6,'host7':7}
appMap = {'app[0]': 0, 'app[1]': 1, 'app[2]': 2, 'app[3]': 3, 'app[4]': 4, 'app[5]': 5,'app[6]':6}

configArr = jsonObj['config']
scalarArr = jsonObj['scalars']
histogramArr = jsonObj['histograms']

configObj = _prepareConfig(configArr)
# print(json.dumps(configObj, indent=4))

simulationResult = _prepareResultSkeleton(idMap)
# print(json.dumps(simulationResult, indent=4))

hostwiseData = {}
_prepareScalarMetrics(idMap, scalarArr, hostwiseData)
_prepareHistogramMetrics(histogramArr, hostwiseData)
# _populateLinkResult(idMap, appMap, hostwiseData, configObj, simulationResult)
# print(json.dumps(hostwiseData, indent=4))

_populateResult(idMap, appMap, hostwiseData, configObj, simulationResult)
# print(json.dumps(simulationResult, indent=4))

# print(json.dumps(simulationResult, indent=4))
f = open("results/simulationResults.json", "w")
f.write(json.dumps(simulationResult, indent=4))
f.close()
