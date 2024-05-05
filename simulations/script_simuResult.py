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


def _prepareResultSkeleton():
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


def _prepareScalarMetrics(scalarArr, hostwiseData):
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

            if not metricName == 'endToEndDelay' or type == 'app[' + str(idMap[hostName]-1) + ']':
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
    packet_received = 0
    packet_sent = 0
    sum_average_delay =0
    # print(json.dumps(configObj, indent=4))

    for hostName in hostwiseData.keys():
        hostData = hostwiseData[hostName]
        # print(json.dumps(hostData, indent=4))
        for type in hostData.keys():
            typeData = hostData[type]
            if type.startswith('app'):
                flows_obj = {}
                for i in range(len(flows_fields)):
                    flows_obj[flows_fields[i]] = -1
                # flows_obj['avg_bw'] = configObj['*.' + hostName + '.' + type + '.datarate']
                flows_obj['avg_delay'] = typeData.get('endToEndDelay', {}).get('mean', 0)
                #if flows_obj['avg_delay'] is not None:
                #sum_average_delay += flows_obj['avg_delay']
                    # print(sum_average_delay)
                # print(json.dumps(typeData.get('endToEndDelay', {}).get('mean')))
                # print(hostData['udp']['packetSent:count'])
                flows_obj['total_packets_transmitted'] = hostData['udp']['packetSent:count']
                flows_obj['total_packets_lost'] = typeData['dropPk:count']
                # print(typeData['endToEndDelay'])
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
                for i in range(len(configObj)):
                    dest = configObj['*.' + hostName + '.' + type + '.destAddresses']
                    dest_num = int(re.search(r'\d+', dest).group())
                    flows_obj['dst'] = dest_num
                flows_obj['targetRouterName'] = 'router'+str(dstMap[type])
                simulationResult['flows'].append(flows_obj)
                # print(json.dumps(simulationResult, indent=4))
            # lost = 0
            # if type.startswith('ppp'):
            #     loss = hostwiseData[hostName]['ppp[0]']['droppedPacketsQueueOverflow:count']/3600
            #     print(loss)

        # sum =0
        sum+=hostData['udp']['packetSent:count']
        packet_received += hostData['udp']['packetReceived:count']
        packet_sent += hostData['udp']['packetSent:count']
        diff = packet_sent - packet_received
        # print(packet_received)
        # print(diff)
        if packet_sent !=0 :
            if diff is not None:
                diff_val = diff/packet_sent
        else:
            diff_val = 0
        # print(sum)
    global_obj = {}
                #     sum += hostData['udp']['packetSent:count']
                #     # print(sum)
                #     total_packets = sum
    r = str(configObj['sim-time-limit'])
    stime = ''.join(x for x in r if x.isdigit())
    # print(int(stime))
    # if sum is not None:
    #     global_obj['avg_packets_per_second'] = sum / int(stime)
    # global_obj['avg_packets_per_second'] = sum/3600
    global_obj['avg_packets_per_second'] = 200000000/1000
    global_obj['avg_packets_lost_per_second'] = diff_val*100
    global_obj['avg_packet_delay'] = sum_average_delay
    # print(global_obj)
    simulationResult['global'] =global_obj

with open('results/result_scaler.json') as user_file:
    file_contents = user_file.read()
jsonData = json.loads(file_contents)
jsonObj = next(iter(jsonData.values())) # get the object under 'General-0-<datetimestamp>' key

idMap = {'host1': 1, 'host2': 2, 'host3': 3, 'host4': 4, 'host5': 5, 'host6': 6,'host7':7}
appMap = {'app[0]': 1, 'app[1]': 2, 'app[2]': 3, 'app[3]': 4, 'app[4]': 5, 'app[5]': 6,'app[6]':7}

configArr = jsonObj['config']
scalarArr = jsonObj['scalars']
histogramArr = jsonObj['histograms']

configObj = _prepareConfig(configArr)
# print(json.dumps(configObj, indent=4))

simulationResult = _prepareResultSkeleton()
# print(json.dumps(simulationResult, indent=4))

hostwiseData = {}
_prepareScalarMetrics(scalarArr, hostwiseData)
_prepareHistogramMetrics(histogramArr, hostwiseData)
# _populateLinkResult(idMap, appMap, hostwiseData, configObj, simulationResult)
# print(json.dumps(hostwiseData, indent=4))

_populateResult(idMap, appMap, hostwiseData, configObj, simulationResult)
# print(json.dumps(simulationResult, indent=4))

# print(json.dumps(simulationResult, indent=4))
f = open("results/simulationResults.json", "w")
f.write(json.dumps(simulationResult, indent=4))
f.close()
