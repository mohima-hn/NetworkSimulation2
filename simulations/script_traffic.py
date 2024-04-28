import csv
import json

with open('traffic_input.json') as user_file:
    file_contents = user_file.read()
jsonObj = json.loads(file_contents)

flows_arr = jsonObj["flows"]
hostdict={}

for i in range (len(flows_arr)):
    flow_obj = flows_arr[i]
    source = str(flow_obj['src'])

    if not source in hostdict:
        hostdict[source] = []

    hostdict[source].append(flow_obj)


# with open('input.txt') as f:
#     reader = csv.reader(f, delimiter=',')
#     rows = []
#     for row in reader:
#         rows.append(row)
# print(rows)
# print(json.dumps(rows, indent=4))
#
# names = ["src", "dest", "data_rate", "time_dist", "pkt_dist", "pkt_size_1", "prob_1","tos"]
# names_onoff = ["src", "dest", "data_rate", "time_dist", "on_time", "off_time", "pkt_dist", "pkt_size_1", "prob_1","tos"]
#
# for i in range(len(rows)):
#     dict = {}
#     timedist=-1
#     for j in range(len(rows[i])):
#         if j == 3:
#             timedist = int(rows[i][j])
#
#         if not timedist == 2:
#             dict[names[j]] = rows[i][j]
#         else:
#             dict[names_onoff[j]] = rows[i][j]
#
#     source = dict['src']
#     if not source in hostdict:
#         hostdict[source] = []
#
#     hostdict[source].append(dict)

# print(hostdict)
print(json.dumps(hostdict, indent=4))

f = open("traffic.json", "w")
f.write('{\n'
        '   "global" : {\n'
				'       "max_bandwidth": 1000000000 \n'
                '       "duration": 3600s \n'
           '},\n'
           '        "flows": [')

buffer = ''
for item in hostdict.keys():
    count = len(hostdict[item])
    for i in range(len(hostdict[item])):
        buffer += (         '       {\n'
                            '           "src": host' + str(item)+',\n'
                            '           "dst": host'+ str(hostdict[item][i]["dest"]) + ',\n'
                            '           "avg_bw": '+ str(hostdict[item][i]["avg_bw"])+',\n'
                            '           "tos": '+ str(hostdict[item][i]["tos"]) +', \n'
                            )
        if hostdict[item][i]["time_dist"] == '0':
            buffer += (     '           "time_dist": Poisson ,\n'
                            '           "avg_time_on": -1,\n'
                            '           "avg_time_off": -1\n'
                            '       }\n')
        elif hostdict[item][i]["time_dist"] == '1':
            buffer += (     '           "time_dist": CBR ,\n'
                            '           "avg_time_on": -1,\n'
                            '           "avg_time_off": -1\n' + '\n'        
                            '       }\n')
        elif hostdict[item][i]["time_dist"] == '2':
            buffer += (     '           "time_dist": On-Off \n'
                            '           "avg_time_on":'+ str(hostdict[item][i]["avg_time_off"]) + '\n'
                            '           "avg_time_off":' + str(hostdict[item][i]["avg_time_on"]) + '\n'
                            '       }\n')
        else:
            buffer += (     '           "time_dist":' + str(hostdict[item][i]["time_dist"]) + '\n'
                            '           "avg_time_on":' + str(hostdict[item][i]["avg_time_off"]) + '\n'
                            '           "avg_time_off":' + str(hostdict[item][i]["avg_time_on"]) + '\n'
                            )
print(buffer)
f.write(buffer)
f.write(
        '   }]\n'
'}\n')
f.close()
                







