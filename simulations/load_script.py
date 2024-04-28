# parser for taking values from traffic json and create omnetpp.ini file
# @author Mohima Hossain
# date : March 05
import csv
import json

with open('traffic_input.json') as user_file:
    file_contents = user_file.read()
jsonObj = json.loads(file_contents)


max_bandwidth = jsonObj["global"]["max_bandwidth"]
duration = jsonObj["global"]["duration"]
flows_arr = jsonObj["flows"]
hostdict={}

for i in range (len(flows_arr)):
    flow_obj = flows_arr[i]
    source = str(flow_obj['src'])

    if not source in hostdict:
        hostdict[source] = []

    hostdict[source].append(flow_obj)

f = open("omnetpp.ini", "w")
f.write('network = NetworkSimulation2\n'
        '**.ospf.ospfConfig = xmldoc("config.xml")\n'
        'sim-time-limit      = '+str(duration)+'s\n'
        '**.host*.app[*].typename = "UdpBasicBurst"\n'
        '**.host*.app[*].chooseDestAddrMode = "once"\n'
        '**.fifo[*].queueLength.result-recording-modes = +vector\n'
        '**.router*.ppp[*].queue.typename  = "inet.examples.inet.netperfmeter.REDQueue" \n'
        # '**.queue.numQueues = 2\n'
        '**.router*.ppp[*].queue.packetCapacity = 10\n'
        '**.router*.ppp[*].PacketBuffer = 16000\n'
        # **.router*.app[*].source.productionInterval = exponential(200us)
        # **.router*.app[*].phyLayer.transmitter.utilization.interval = 0.2s
        '\n')
buffer = ''
jsonData={}
buffer +=      ('**.host*.app[0].destPort = 1000'+ '\n'
               '**.host*.app[1].destPort = 1001'+ '\n'
               '**.host*.app[2].destPort = 1002'+ '\n'
               '**.host*.app[3].destPort = 1003'+ '\n'
               '**.host*.app[4].destPort = 1004'+ '\n'
               '**.host*.app[5].destPort = 1005'+ '\n'
               '**.host*.app[6].destPort = 1006'+ '\n'
               '**.host*.app[0].localPort = 1000'+ '\n'
               '**.host*.app[1].localPort = 1001'+ '\n'
               '**.host*.app[2].localPort = 1002'+ '\n'
               '**.host*.app[3].localPort = 1003'+ '\n'
               '**.host*.app[4].localPort = 1004'+ '\n'
               '**.host*.app[5].localPort = 1005'+ '\n'
               '**.host*.app[6].localPort = 1006' + '\n\n'
                )
for item in hostdict.keys():
    count = len(hostdict[item])
    buffer += ('*.host' + item + '.numApps = ' + str(count) + '\n')
    for i in range(len(hostdict[item])):
        jsonData={}

        buffer += ('*.host' + item + '.app[' + str(i) + '].typename = "UdpBasicBurst"\n'
                   '*.host' + item + '.app[' + str(i) + '].destAddresses = "host' + str(hostdict[item][i]["dest"]) + '"\n'
                   '*.host' + item + '.app[' + str(i) + '].datarate = ' + str(hostdict[item][i]["avg_bw"]) + '\n'
                   '*.host' + item + '.app[' + str(i) + '].messageLength = ' + str(hostdict[item][i]["pkt_size"]) + 'Byte\n'
                   '*.host' + item + '.app[' + str(i) + '].tos = ' + str(hostdict[item][i]["tos"]) + '\n'
                   )
        if hostdict[item][i]["time_dist"] == 0:
            buffer += ('*.host' + item + '.app[' + str(i) + '].sendInterval = poisson(8.82) * 1s \n'
                        '*.host' + item + '.app[' + str(i) + '].sleepDuration = '  + '0s\n'
                        '*.host' + item + '.app[' + str(i) + '].burstDuration = '  + '0s\n\n\n')
        elif hostdict[item][i]["time_dist"] == 1:
                buffer += ('*.host' + item + '.app[' + str(i) + '].sendInterval = ' + str(hostdict[item][i]["time_dist"]) + 's\n'
                        '*.host' + item + '.app[' + str(i) + '].sleepDuration = ' + '0s\n'
                        '*.host' + item + '.app[' + str(i) + '].burstDuration = ' + '0s\n\n\n')
        elif hostdict[item][i]["time_dist"] == 2:
                    buffer += ('*.host' + item + '.app[' + str(i) + '].sendInterval = ' + str(hostdict[item][i]["time_dist"]) + 's\n'
                    '*.host' + item + '.app[' + str(i) + '].sleepDuration =' + str(hostdict[item][i]["avg_time_off"]) + 's\n'
                    '*.host' + item + '.app[' + str(i) + '].burstDuration = ' + str(hostdict[item][i]["avg_time_on"]) + 's\n\n\n')
        else:
            buffer += ('*.host' + item + '.app[' + str(i) + '].sendInterval = ' + str(hostdict[item][i]["time_dist"]) + 's\n\n\n')
# print(buffer)
f.write(buffer)
f.close()
#wrinting end
#open and read the file after the appending:
# f = open("omnetpp.ini", "r")
#print(f.read())








