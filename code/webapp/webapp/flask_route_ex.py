from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
import json
import pygal
from pygal.style import DarkSolarizedStyle

app = Flask(__name__)
@app.route('/')
def Chart():

    templateData = {
	'title': 'Temperature',
	'rooms': [ "B03", "108", "120", "209", "223", "308", "323", "OUTSIDE"],
	}
    return render_template('main.html', **templateData)

@app.route('/roomchart', methods=['POST', 'GET'])
def chartByRoom():

    #receive start, stop, and rooms selected from main.html
    get = json.dumps(request.args)
    get = json.loads(get)
    start = str(get['start'])
    stop = str(get['stop'])
    rooms = [ "B03", "108", "120", "209", "223", "308", "323", "OUTSIDE"]
    
    selected = []
    timecount = 0

    #check for which rooms to request data for
    for arg in get:
      for room in rooms:
        if arg == room:
          selected.append(room)

    #Generate initial graphs for celcius and farenheight
    chartf = pygal.Line(width=1200, height=600, explicit_size=True, disable_xml_declaration=True, style=DarkSolarizedStyle)
    chartf.title = "Graph of Temperatures (F) From " + start + " to " + stop

    chartc = pygal.Line(width=1200, height=600, explicit_size=True, disable_xml_declaration=True, style=DarkSolarizedStyle)
    chartc.title = "Graph of Temperatures (C) From " + start + " to " + stop  
        

    for checked in selected:
        # params for the get request, variables with be specified by user input
        params = {'climate': 'true', 'building': 'BLI', 'room': checked, 'startTime': start, 'stopTime': stop}

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

        #calculate how many data points to plot based on the length of the list
        points = (len(list['info'])/144) * 12
        for x in list['info']:
            if count < points:
                count += 1
                fAvg = fAvg + float(x['tempF'])
                cAvg = cAvg + float(x['tempC'])
            else:
                count += 1
                fAvg = fAvg + float(x['tempF'])
                cAvg = cAvg + float(x['tempC'])

                listf.append(round(fAvg/count, 1))
                listc.append(round(cAvg/count, 1))
                if timecount == 0:
                  listt.append(str(x['time'])[10:-3])
                count = 0
                fAvg = 0
                cAvg = 0

        if timecount == 0:
          chartf.x_labels = map(str, listt)        
          chartc.x_labels = map(str, listt)
          timecount += 1
        
        chartf.add(str(checked), listf)
        chartc.add(str(checked), listc)

    return render_template('room.html', chartf=chartf, chartc=chartc, selected=selected, start=start, rooms=rooms)

      

@app.route('/floorchart')
#Plot by floor given start and stop time
def chartByFloor():
    get = json.dumps(request.args)
    get = json.loads(get)
    start = str(get['start'])
    stop = str(get['stop'])
    
    count = 0  
    flists = []
    clists = []
    
    listt = []

    rooms = [ "B03", "108", "120", "209", "223", "308", "323"] 
    rcount = 0

    #This loop iterates through the rooms for each data set
    for x in rooms:
        # params for the get request, start and stop variables with be specified by user input
        params = {'climate': 'true', 'building': 'BLI', 'room': x, 'startTime': '2016-04-20', 'stopTime': '2016-04-21'}
        #requests
        r = requests.get('http://cs.newpaltz.edu/~loweb/pi/api/climate.php', params=params)
        data = r.text
        # Making the response usable
        list = json.loads(data)

        # Basement 
        if rcount == 0:
            fAvg = 0
            cAvg = 0
            listf = []
            listc = []
            tlist = []
        #create lists        
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
        # establish lists of odd indicies in flists
        elif rcount % 2 == 1 & rcount != 0:
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
        # averages previous room list in flists and current room
        else:
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
            print(flists[len(flists) - 1])
        rcount += 1
        
    print(flists)

    chartf = pygal.Line(width=1200, height=600, explicit_size=True, disable_xml_declaration=True, style=DarkSolarizedStyle)
    chartf.title = "Graph of Temperatures (F) By Floor From " + start + " to " + stop  
    chartf.x_labels = map(str, listt)

    reverse = 3
    for flist in flists:
        chartf.add(str(reverse), flists[reverse])
        reverse = reverse - 1
    chartf.render_to_file('/tmp/fchartfloor.svg')
    chartf.render()

    chartc = pygal.Line(width=1200, height=600, explicit_size=True, disable_xml_declaration=True, style=DarkSolarizedStyle)
    chartc.title = "Graph of Temperatures (C) By Floor From " + start + " to " + stop  
    chartc.x_labels = map(str, listt)

    
    for clist in clists:
        chartc.add(str(clists.index(clist)), clist)
    chartc.render_to_file('/tmp/cchartfloor.svg')
    chartc.render()

    return render_template('floor.html', chartf=chartf, chartc=chartc)

if __name__=='__main__':
      app.run(port=80)
