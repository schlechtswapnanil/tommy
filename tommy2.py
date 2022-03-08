import speech_recognition as sr
import pywhatkit as pw
import sounddevice as sd 
import wikipedia
import datetime as dt
import os
import webbrowser as wb
import smtplib
import pyttsx3
import phonenumbers
from phonenumbers import geocoder
import requests
from bs4 import BeautifulSoup

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voices', voices[2].id)

MASTER="Shopnoneel"

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    talk("Waking tommy up...")
    hour=dt.datetime.now().hour
    if hour>4 and hour<12:
        talk("Good Morning "+MASTER)
    elif hour>=12 and hour<17:
        talk("Good Afternoon "+MASTER)
    elif hour>=17 and hour<21:
        talk("Good Evening "+MASTER)
    elif hour>=22 and hour<24:
        talk("Good Night "+MASTER)
    else:
        talk("Still awake? What are you doing at this late hour of night?")
    talk("What can I do for you now ?")

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....go ahead.")
        audio=r.listen(source, phrase_time_limit=2)
    try:
        #print("Recognizing")
        command=r.recognize_google(audio, language='en-in')
        #print(MASTER+" said: "+command)
    except:
        talk("Speak clearly again please")
        takecommand()
    return command

def genq(q):
    
    query =q

    URL = "https://www.google.co.in/search?q=" +query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }
    page=requests.get(URL)
    soup= BeautifulSoup(page.content, 'html.parser')
    result=soup.find(class_="kp-header").get_text()
    if(result):
        talk(result)
    else:
        talk("Class mismatch in the web scraper, try again please")

        
            
genq("What is the birthday of narendra Modi?")

while False:
    headfirst=takecommand()
    if("start" in headfirst or "wake up" in headfirst): #all logic to make Tommy work
        greet()
        while True:
            query=takecommand()
            if query==None:
                continue
            elif("Time now" in query):
                now = dt.datetime.now()
                current_time = now.strftime("%H:%M")
                talk("Right now, it's "+ current_time)
                continue
            elif("date today" in query):
                today=dt.date.today().strftime("%B %d, %Y")
                talk("today it's "+today)
            elif("weather" in query):
                talk("Weather of which place again?")
                city=takecommand()
                URL = "https://www.google.com/search?q=weather+of+"+city
                headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
                }
                html=requests.get(URL).content
                page = requests.get(URL, headers=headers)
                soup = BeautifulSoup(html, 'html.parser')
                temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
                temp.replace("C","Centigrade")
                str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
                
                # formatting data
                data = str.split('\n')
                time = data[0]
                sky = data[1]
                
                # getting all div tag
                listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
                strd = listdiv[5].text
                
                # getting other required data
                pos = strd.find('Wind')
                other_data = strd[pos:]
                
                talk("The weather details of "+city+" is as follows ")
                talk("Temperature will approximately be"+temp)
                talk("The Skies will be: "+sky)
                talk(other_data)
                continue
            elif ("who is" in query):
                sq=query.replace("who is","")
                wiki=wikipedia.summary(sq, sentences=2)
                talk(wiki)
            elif("play the song" in query):
                song=query.replace("play the song", "")
                talk("Playing "+song+" for you")
                pw.playonyt(song)
                talk("anything else?")
                continue
            elif("open" in query):
                task=query.replace("open","")
                task.lower()
                if('teams' in task):
                    talk("Opening "+task+" for you now")
                    os.system('msteams')
                elif('word' in task):
                    talk("Opening Microsoft Word for you now")
                    os.system('winword')
                elif('google' in task) or('Chrome' in task):
                    talk("Opening Google Chrome for you now")
                    os.system('chrome')
                elif('browser' in task) or ('fire fox' in task):
                    talk("Got it. Opening Morzilla Firefox for you now")
                    os.system('firefox')
                else:
                    talk("Opening "+task+" for you now")
                    os.system(task)            

            elif("What's App" in query):
                talk("enter the number of the reciepent")
                wappno=input("Enter the reciepent's number here: ")
                wappno="+91"+wappno
                talk("speak out your message within 10 seconds")
                mess=Message()
                talk("Sending your message which is "+ mess)
                pw.sendwhatmsg_instantly(wappno, mess)
            else:
                genq(query)
                continue