# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:17:21 2018

@author: newguest
"""
# All the machine specific details are replaced with xxx for security.
import tkinter
from tkinter import Button
import paho.mqtt.client as mqtt
from urllib import request
import re
import MySQLdb
import datetime
import SmartBlindsML
from SmartBlindsML import getPredictedData

def hello(): 
    conn = MySQLdb.connect(host="XXXXX", user="XXXXX", passwd="XXXX", db="smartblinds")
    cursor = conn.cursor()
    AMValue = 'AM'
    if datetime.datetime.now().hour > 12:
        AMValue = 'PM'
    query = """ 
       INSERT INTO smartblinds(date,time,status,timecategory)
       VALUES('""" + datetime.datetime.today().strftime('%Y-%m-%d')+"""',"""+"""'"""+datetime.datetime.now().strftime('%H:%M')+ """'""" +""", 'open','"""+AMValue+"""');"""  
  
    cursor.execute(query)
    conn.commit()
    conn.close()
    mqttc = mqtt.Client('python_pub')
    mqttc.connect('XXXXX', 1883)
    mqttc.publish('XXXXX', '{"blind":"open"}')
#    mqttc.loop(2) 
    print("Single Click, Button-l") 
def Cool():
    conn = MySQLdb.connect(host="XXXXX", user="XXXXX", passwd="XXXXXX", db="smartblinds")
    cursor = conn.cursor()
    AMValue = 'AM'
    if datetime.datetime.now().hour > 12:
        AMValue = 'PM'
    query = """ 
       INSERT INTO smartblinds(date,time,status,timecategory)
       VALUES('""" + datetime.datetime.today().strftime('%Y-%m-%d')+"""',"""+"""'"""+datetime.datetime.now().strftime('%H:%M')+ """'""" +""", 'close','"""+AMValue+"""');"""  
  
    cursor.execute(query)
    conn.commit()
    conn.close()
    mqttc = mqtt.Client('python_pub')
    mqttc.connect('XXXXXX', 1883)
    mqttc.publish('<topic_name>', '{"blind":"close"}')
    #mqttc.loop(2)                          
    print("That's cool!")
    
def calculatesunriseandsunsettimes():
    url = "http://www.bbc.com/weather/5128581"
    html = request.urlopen(url).read().decode('utf8')
    from bs4 import BeautifulSoup
    text2 = BeautifulSoup(html,"lxml").get_text()
#   tokens = word_tokenize(raw)
#   text = nltk.Text(tokens)
#   text2 = text.concordance('Sunrise')
   #print(type(raw))
   #print(text)
  # text2 = text[1:] 
#   print(text2)
   #print(text2[52538:])
    matchforsunrise=text2.find('Sunrise')
    print(matchforsunrise)
    match2 = re.search('\d{2}:\d{2}', text2[matchforsunrise:])
    if(match2):
       print(match2.start(),match2.end())
       sunrise_time = text2[matchforsunrise+match2.start():matchforsunrise+match2.end()]
       matchforsunset=text2[matchforsunrise+match2.end():].find('Sunset')
       print(matchforsunset)   
       match3 = re.search('\d{2}:\d{2}', text2[matchforsunset:])
       if(match3):
           print(match3.start(),match3.end())
           print(text2[matchforsunset+match3.start(): matchforsunset+match3.end()])
       sunset_time = text2[matchforsunset+match3.start(): matchforsunset+match3.end()]
    return [sunrise_time,sunset_time]
    
def helloAtSunRise(): 
    

    # this is the query we will be making 
   
  
    sunrise_time = calculatesunriseandsunsettimes()[0]
    conn = MySQLdb.connect(host="XXXX", user="XXXXX", passwd="XXXXX", db="smartblinds")
    cursor = conn.cursor()
    query = """ 
       INSERT INTO smartblinds(date,time,status,timecategory)
       VALUES('""" + datetime.datetime.today().strftime('%Y-%m-%d')+"""',"""+"""'"""+sunrise_time+ """'""" +""", 'open','AM');"""  
  
    cursor.execute(query)
    conn.commit()
    conn.close()
    
    
def CoolAtSunset():  
    sunset_time = calculatesunriseandsunsettimes()[1]
    conn = MySQLdb.connect(host="XXXX", user="XXXX", passwd="XXXXX", db="smartblinds")
    cursor = conn.cursor()
    query = """ 
       INSERT INTO smartblinds(date,time,status,timecategory)
       VALUES('""" + datetime.datetime.today().strftime('%Y-%m-%d')+"""',"""+"""'"""+sunset_time+ """'""" +""", 'open','PM');"""  
  
    cursor.execute(query)
    conn.commit()
    conn.close()
    mqttc = mqtt.Client('python_pub')
    mqttc.connect('xx.xx.xx.xx', 1883)
    mqttc.publish('<topic_name>', '{"blind":"close"}')
    #mqttc.loop(2)                          
    
win = tkinter.Tk()
widget = Button(win, text='Open the blinds',command =hello)
widget.pack()
#widget.bind('<Button-1>', hello)

widget2 = Button(win, text='Close the blinds',command =Cool)
widget2.pack()

widget3 = Button(win, text='Open the blinds at Sunrise',command =helloAtSunRise)
widget3.pack()
#widget.bind('<Button-1>', hello)

widget4 = Button(win, text='Close the blinds at Sunset',command =CoolAtSunset)
widget4.pack()
#widget2.bind('<Double-1>', Cool)

win.mainloop()

    
today = datetime.datetime.today().strftime('%m/%d/%y')
time = datetime.datetime.now().strftime('%H:%M')
timecategory = 'AM'
if datetime.datetime.now().hour > 12:
    timecategory = 'PM' 
obtained_result = getPredictedData(today,time,timecategory)   
mqttc = mqtt.Client('python_pub')
mqttc.connect('xxxxxxxx', 1883)
message = '{"blind": "'+ obtained_result+'"}'
print(message)
mqttc.publish('<topic_name>', message)

