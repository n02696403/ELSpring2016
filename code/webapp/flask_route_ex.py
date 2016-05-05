from flask import Flask, render_template
import datetime
import requests
import json

app = Flask(__name__)
@app.route("/")
def hello():
  p = {'climate': 'true', 'building': 'BLI', 'room': '120','startTime': '2016-04-20'}
  r = requests.get('http://cs.newpaltz.edu/~loweb/pi/api/climate.php', params=p)
  # This is to get it into parsable form. Don't ask why. 
  data = r.text
  list = json.loads(data)
  jobj = json.dumps(list)
  
 
  #construct three lists , celsius, farenheight, and time
  flist = []
  clist = []
  tlist = []

  #iterate through 'info' key of the json object 
  for x in list['info']:
	flist.append(x['tempF'].encode('utf-8'))
	clist.append(x['tempC'].encode('utf-8'))
	tlist.append(x['time'].encode('utf-8'))  

  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")
  templateData = {
	'title': 'Temperature',
	'time': timeString,
	't': tlist,
	'f': flist,
	'c': clist,
	't': tlist	}
  return render_template('main.html', **templateData)

@app.route("/getInfo/<val>")
def info(val): 
  now = datetime.datetime.now()
  if (val=='time'):
 	timeString = now.strftime("%H:%M")
	templateData = { 'title' : 'Time on this PI',
		'name' : 'Time is',
		'datetime' : timeString}
  if (val=='date'):
	timeString = now.strftime("%Y-%m-%d")
	templateData = { 'title' : 'Date on this Pi',
		'name' : 'Date on the pi',
		'dateTime' : timeString}
	return render_template('date_time.html', **templateData)
if __name__=="__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
