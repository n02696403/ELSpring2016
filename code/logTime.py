#!/usr/bin/python
import sqlite3 as mydb #imports module to connect to the database
import sys
import time 

def logTime():
   #Establish the connection
   connection = mydb.connect('testTime.db') 
   d = time.strftime("%x")
   t = time.strftime("%X")
   #Create the list of date and time values
   timeLog = [d, t]                          
   
   with connection:
      c = connection.cursor()
      #insert the values from timeLog lisrt into the two columns
      c.execute('insert into testTime values (?,?)', timeLog)
   print timeLog
   print d
   print t
   #Finally, close out the database connection
   connection.close()
logTime()
