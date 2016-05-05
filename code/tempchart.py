import json
import requests
import pygal
from datetime import datetime, timedelta

# params for the get request, variables with be specified by user input
params = {'climate': 'true', 'building': 'BLI', 'room': '120', 'startTime': '2016-04-20', 'stopTime': '2016-04-21'}

#request
r = requests.get('http://cs.newpaltz.edu/~loweb/pi/api/climate.php', params=params)
data = r.text
# Making the response usable
list = json.loads(data)

#Intial data parsing test
#-----------------------------------------------------------------
#print(list)

#flist = []
#clist = []
#tlist = []

#for x in list['info']:
#   flist.append(x['tempF'])
#   clist.append(x['tempC'])
#   tlist.append(x['time'])
#print(tlist, clist, flist)
#------------------------------------------------------------------

#This method calculates 2-hour averages, and produces two charts (F & C)for a single room
# @params - these will be dictated by user input when integrated with Flask
# room : room number
# start: startTime
# stop: stopTime
def chartByDay(room, start, stop):
    count = 0
    fAvg = 0
    cAvg = 0 
    listf = []
    listc = []
    listt = []
    
    for x in room['info']:
        if count < 12:
            count += 1
            fAvg = fAvg + float(x['tempF'])
            cAvg = cAvg + float(x['tempC'])
        else:
            count += 1
            fAvg = fAvg + float(x['tempF'])
            cAvg = cAvg + float(x['tempC'])

            listf.append(round(fAvg/count, 1))
            listc.append(round(cAvg/count, 1))
            listt.append(str(x['time'])[10:-3])
            count = 0
            fAvg = 0
            cAvg = 0 

    print(listt)
    print(listf)
    print(listc)

    chartf = pygal.StackedLine(fill=True)
    chartf.title = "Graph of Temperatures (F) for " + room['room'] + " From " + start + " to " + stop  
    chartf.x_labels = map(str, listt)
    chartf.add("Fahrenheight", listf)
    chartf.render_to_file('/tmp/chartf.svg')
    chartf.render()

    chartc = pygal.StackedLine(fill=True)
    chartc.title = "Graph of Temperatures (C) for " + room['room'] + " From " + start + " to " + stop  
    chartc.x_labels = map(str, listt)
    chartc.add("Celsius", listc)
    chartc.render_to_file('/tmp/chartc.svg')
    chartc.render()
chartByDay(list, "2016-04-20", "2016-04-21")   
