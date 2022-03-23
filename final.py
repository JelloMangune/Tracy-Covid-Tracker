import tkinter as tk
import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY = "tJx9BcUyUome"
PROJECT_TOKEN = "tm0-6vVrJdYU"
RUN_TOKEN = "tYLJ-8Tf67Y7"


#Class for gathering information from the API
class Covid:
    #API request in function form, credits to https://towardsdatascience.com/bye-bye-beautiful-soup-how-i-scraped-covid-19-data-using-python-4dd06f930dc0
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params ={"api_key":self.api_key}
        self.get_data()
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        self.data = json.loads(response.text)

    #Function to get total cases in the whole world
    def get_totalcases(self):
        data = self.data['total']
        for info in data:
            if info['name'] == 'Coronavirus Cases:':
                return info['value']

    #Function to get total deaths in the whole world
    def get_totaldeaths(self):
        data = self.data['total']
        for info in data:
            if info['name'] == 'Deaths:':
                return info['value']

    #Function to get total recovered cases in the whole world
    def get_totalrecovered(self):
        data = self.data['total']
        for info in data:
            if info['name'] == 'Recovered:':
                return info['value']

    #Function to get information about a specific country
    def get_countrydata(self, country):
        data = self.data['country']
        for info in data:
            if info['name'].lower() == country.lower():
                return info

    #Countries in list form, this is used for determining a country in the dialog
    def list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())
        return countries

data = Covid(API_KEY, PROJECT_TOKEN)

def talk(text):
    audio = pyttsx3.init('sapi5')
    voices = audio.getProperty('voices')
    audio.setProperty('rate', 196)
    audio.setProperty('volume', 2.7)
    audio.setProperty('voice', voices[1].id)
    audio.say(text)
    audio.runAndWait()

def mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))
    return said.lower()

def ask(entry):
    data = Covid(API_KEY, PROJECT_TOKEN)
    countrylist = set(list(data.list_of_countries()))
    text = entry
    countrytext = text.split()
    pos = len(countrytext) - 1
    print(text)
    if text.startswith("") and "total cases" in text and (text.endswith("world") or text.endswith("globally")):
        response = "There is a total of " + str(data.get_totalcases()) + " covid cases \n around the globe."
        print(response)
        label2['text'] = response
    if text.startswith("") and "deaths" in text and (text.endswith("world") or text.endswith("globally")):
        response = "There is a total of " + str(data.get_totaldeaths()) + " covid deaths \n around the globe."
        print(response)
        label2['text'] = response
    if text.startswith("") and "recovered" in text and (text.endswith("world") or text.endswith("globally")):
        response = "There is a total of " + str(data.get_totalrecovered()) + " recovered covid patients \n around the globe."
        print(response)
        label2['text'] = response

        #per country
    if text.startswith("") and "total cases" in text and countrytext[pos] in countrylist:
        response = "There are " + data.get_countrydata(countrytext[pos])['total_cases'] + " covid cases in \n " + countrytext[pos]
        print(response)
        label2['text'] = response
    if text.startswith("") and "deaths" in text and countrytext[pos] in countrylist:
        response = "There are " + data.get_countrydata(countrytext[pos])['total_deaths'] + " covid deaths in \n " + countrytext[pos]
        print(response)
        label2['text'] = response
    if text.startswith("") and "recovered" in text and countrytext[pos] in countrylist:
        response = "There are " + data.get_countrydata(countrytext[pos])['total_recovered'] + " recovered covid patients in \n " + countrytext[pos]
        print(response)
        label2['text'] = response

    #country only
    if text in countrylist:
        response = countrytext[pos].upper() + ":\n" + data.get_countrydata(countrytext[pos])['total_cases'] + " covid cases \n" + data.get_countrydata(countrytext[pos])['total_deaths'] + " covid deaths \n" + data.get_countrydata(countrytext[pos])['total_recovered'] + " recovered patients"
        print(response)
        label2['text'] = response

def talking():
    data = Covid(API_KEY, PROJECT_TOKEN)
    print("Hello, I am Tracy!")
    talk("Hello, I am Tracy!")
    talk("What can I do for you?")
    END_PHRASE = "stop"
    countrylist = set(list(data.list_of_countries()))

    while True:

        print("Listening...")
        text = mic()
        countrytext = text.split()
        pos = len(countrytext) - 1
        print(text)
        if text.startswith("") and "total cases" in text and (text.endswith("world") or text.endswith("globally")):
            response = "There is a total of " + str(data.get_totalcases()) + " covid cases around the globe."
            print(response)
            talk(response)
            print()
        if text.startswith("") and "deaths" in text and (text.endswith("world") or text.endswith("globally")):
            response = "There is a total of " + str(data.get_totaldeaths()) + " covid deaths around the globe."
            print(response)
            talk(response)
            print()
        if text.startswith("") and "recovered" in text and (text.endswith("world") or text.endswith("globally")):
            response = "There is a total of " + str(data.get_totalrecovered()) + " recovered covid patients around the globe."
            print(response)
            talk(response)
            print()

        #per country
        if text.startswith("") and "total cases" in text and countrytext[pos] in countrylist:
            response = "There are " + data.get_countrydata(countrytext[pos])['total_cases'] + " covid cases in the " + countrytext[pos]
            print(response)
            talk(response)
            print()
        if text.startswith("") and "deaths" in text and countrytext[pos] in countrylist:
            response = "There are " + data.get_countrydata(countrytext[pos])['total_deaths'] + " covid deaths in the " + countrytext[pos]
            print(response)
            talk(response)
            print()
        if text.startswith("") and "recovered" in text and countrytext[pos] in countrylist:
            response = "There are " + data.get_countrydata(countrytext[pos])['total_recovered'] + " recovered covid patients in the " + countrytext[pos]
            print(response)
            talk(response)
            print()

        #country only
        if text in countrylist:
            response = countrytext[pos].upper() + ":\n" + data.get_countrydata(countrytext[pos])['total_cases'] + " covid cases \n" + data.get_countrydata(countrytext[pos])['total_deaths'] + " covid deaths \n" + data.get_countrydata(countrytext[pos])['total_recovered'] + " recovered patients"
            print(response)
            talk(response)
            print()

        if text == END_PHRASE:
            print("Thank you for using Trace-C")
            talk("Thank you for using Trace-C")
            label2['text'] = ""
            entry.delete(0, 'end')
            break


root = tk.Tk()
root.title("TRACE-C")

canvas = tk.Canvas(root, height=450, width=600)
canvas.pack()

micimg = tk.PhotoImage(file='mic.png')

bgimage = tk.PhotoImage(file='bgbg4.png')
bglabel = tk.Label(root, image=bgimage)
bglabel.place(x=0,y=0,relwidth=1, relheight=1)

frameside =tk.Frame(root, bg='#00221B', bd=2)
frameside.place(relx=.95, rely=0.03, relwidth=0.08, relheight=0.1, anchor='ne')

button2 = tk.Button(frameside, image = micimg, text="MIC", font=40, command = talking)
button2.place(relheight=0.9, relwidth=0.9, relx = 0.075, rely=0.075)

frame = tk.Frame(root, bg='#00221B', bd=5)
frame.place(relx=0.45, rely=0.05, relwidth=0.8, relheight=0.075, anchor='n')

entry = tk.Entry(frame, font =('Monaco bold', 11))
entry.place(relwidth=0.78,relheight=1)

button = tk.Button(frame, font =('Monaco bold', 11), text="Ask", command =lambda: ask(entry.get().lower()))
button.place(relx=0.80, relheight=1, relwidth=0.2)

frame2 = tk.Frame(root, bg='#00221B', bd=10)
frame2.place(relx=0.5, rely=0.15, relwidth=0.8,relheight=0.80, anchor='n')

label2 = tk.Label(frame2, font =('Monaco', 10), text = "")
label2.place(relwidth=1, relheight=1)



root.mainloop()
