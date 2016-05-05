import json
import requests
import pygal
from datetime import datetime, timedelta

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
def chartByRoom(room, start, stop):

    # params for the get request, variables with be specified by user input
    params = {'climate': 'true', 'building': 'BLI', 'room': room, 'startTime': start, 'stopTime': stop}

    #request
    r = requests.get('http://cs.newpaltz.edu/~loweb/pi/api/climate.php', params=params)
    data = r.text
    # Making the response usable
    list = json.loads(data)


    count = 0
    fAvg = 0
    cAvg = 0 
    listf = []
    listc = []
    listt = []
    
    for x in list['info']:
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
            
    chartf = pygal.StackedLine(fill=True)
    chartf.title = "Graph of Temperatures (F) for " + str(room) + " From " + start + " to " + stop  
    chartf.x_labels = map(str, listt)
    chartf.add("Fahrenheight", listf)
    chartf.render_to_file('/tmp/chartf.svg')
    chartf.render()

    chartc = pygal.StackedLine(fill=True)
    chartc.title = "Graph of Temperatures (C) for " + str(room) + " From " + start + " to " + stop  
    chartc.x_labels = map(str, listt)
    chartc.add("Celsius", listc)
    chartc.render_to_file('/tmp/chartc.svg')
    chartc.render()
chartByRoom(120, "2016-04-20", "2016-04-21")   

#Method to plot temperature data by floor.
#@params:
#start: startTime
#stop: stopTime
def chartByFloor(start, stop):
    count = 0  
    flists = []
    clists = []
    
    listt = []

    rooms = [ "B03", "108", "120", "209", "223", "308", "323"] 
    rcount = 0

    #This loop iterates through the rooms for each data set
    for x in rooms:
        print(x)
        # params for the get request, start and stop variables with be specified by user input
        params = {'climate': 'true', 'building': 'BLI', 'room': x, 'startTime': '2016-04-20', 'stopTime': '2016-04-21'}

        #requests
        r = requests.get('http://cs.newpaltz.edu/~loweb/pi/api/climate.php', params=params)
        data = r.text
        #print(data)
        # Making the response usable
        list = json.loads(data)

        print(rcount)
        if rcount == 0:
            fAvg = 0
            cAvg = 0
            listf = []
            listc = []
            tlist = []
                
            for y in list['info']:
                
                if count < 12:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])
                else:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])

                    listf.append(round(fAvg/count, 1))
                    listc.append(round(cAvg/count, 1))
                    tlist.append(str(y['time'])[10:-3])
                
                    count = 0
                    fAvg = 0
                    cAvg = 0

            flists.append(listf)
            clists.append(listc)
            listt = tlist
        elif rcount % 2 == 1 & rcount != 0:
            print("whats good")
            fAvg = 0
            cAvg = 0
            listf = []
            listc = []
                
            for y in list['info']:
                if count < 12:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])
                else:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])

                    listf.append(round(fAvg/count, 1))
                    listc.append(round(cAvg/count, 1))
                
                    count = 0
                    fAvg = 0
                    cAvg = 0

            flists.append(listf)
            clists.append(listc)
            print(flists)

        else:
            print("yo")
            fAvg = 0
            cAvg = 0
            listf = []
            listc = []
            
            for y in list['info']:
                if count < 12:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])
                else:
                    count += 1
                    fAvg = fAvg + float(y['tempF'])
                    cAvg = cAvg + float(y['tempC'])

                    listf.append(round(fAvg/count, 1))
                    listc.append(round(cAvg/count, 1))

                    count = 0
                    fAvg = 0
                    cAvg = 0
                    
            for z in listf:
                count = 0
                print(count)
                print(z)
                if count < flists[len(flists) - 1]:
                    z = round(((z + flists[len(flists) - 1][count]) / 2), 1)

                else:
                    flists[len(flists) - 1].append(z)

                count += 1    
            flists[len(flists) - 1] = listf
        rcount += 1
        
    print(flists)

    chartf = pygal.Line(fill=True)
    chartf.title = "Graph of Temperatures (F) By Floor From " + start + " to " + stop  
    chartf.x_labels = map(str, listt)

    reverse = 3
    for flist in flists:
        chartf.add(str(reverse), flists[reverse])
        reverse = reverse - 1
    chartf.render_to_file('/tmp/fchartfloor.svg')
    chartf.render()

    chartc = pygal.Line(fill=True)
    chartc.title = "Graph of Temperatures (C) By Floor From " + start + " to " + stop  
    chartc.x_labels = map(str, listt)

    for clist in clists:
        chartc.add(str(clists.index(clist)), clist)
    chartc.render_to_file('/tmp/cchartfloor.svg')
    chartc.render()

chartByFloor('2016-04-20', '2016-04-21')
