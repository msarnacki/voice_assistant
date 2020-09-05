#from __future__ import print_function
import datetime
from datetime import timedelta, date
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import requests
import winsound
import pyttsx3
import pyttsx3.drivers
import pytz
import weather_key

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

DNI_TYGODNIA = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
DNI_TYGODNIA_PRZYSZLE = ["przyszły poniedziałek", "przyszły wtorek", "przyszła środa", "przyszły czwartek", "przyszły piątek", "przyszła sobota", "przyszła niedziela"]
MONTHS = ["styczeń","luty","marzec","kwiecień", "maj","czerwiec","lipiec","sierpień","wrzesień","październik","listopad","grudzień"]
MONTHS_2 = ["stycznia","lutego","marca","kwietnia", "maja","czerwca","lipca","sierpnia","września","października","listopada","grudnia"]
JUTRO = ["dziś", "jutro", "pojutrze"]
JUTRO_2 = ["dzisiaj"]
DNI_MIESIACA = ["pierwszy", "drugi", "trzeci", "czwarty", "piąty", "szósty", "siódmy", "ósmy", "dziewiąty", "dziesiąty", "jedenasty", "dwunasty", "trzynasty", "czternasty","piętnasty","szesnasty", "siedemnasty", "osiemnasty", "dziewietnasty", "dwudziesty", "dwudziesty pierwszy", "dwudziesty drugi", "dwudziesty trzeci", "dwudziesty czwarty", "dwudziesty piąty", "dwudziesty szósty", "dwudziesty siódmy", "dwudziesty ósmy", "dwudziesty dziewiąty", "trzydziesty", "trzydziesty pierwszy"]
DNI_MIESIACA_2 = ["pierwszego", "drugiego", "trzeciego", "czwartego", "piątego", "szóstego", "siódmego", "ósmego", "dziewiątego", "dziesiątego", "jedenastego", "dwunastego", "trzynastego", "czternastego","piętnastego","szesnastego", "siedemnastego", "osiemnastego", "dziewiętnastego", "dwudziestego", "dwudziestego pierwszego", "dwudziestego drugiego", "dwudziestego trzeciego", "dwudziestego czwartego", "dwudziestego piątego", "dwudziestego szóstego", "dwudziestego siódmego", "dwudziestego ósmego", "dwudziestego dziewiątego", "trzydziestego", "trzydziestego pierwszego"]
SLOWNIK_MIESIACE = {"January":" stycznia","February":" lutego","March":" marca","April":" kwietnia", "May":" maja","June":" czerwca","July":" lipca","August":" sierpnia","September":" września","October":" października","November":" listopada","December":" grudnia"}
SLOWNIK_DNI_MIESIACA = {"01":"pierwszy", "02":"drugi", "03":"trzeci", "04":"czwarty", "05":"piąty", "06":"szósty", "07":"siódmy", "08":"ósmy", "09":"dziewiąty", "10":"dziesiąty", "11":"jedenasty", "12":"dwunasty", "13":"trzynasty", "14":"czternasty","15":"piętnasty","16":"szesnasty", "17":"siedemnasty", "18":"osiemnasty", "19":"dziewietnasty", "20":"dwudziesty", "21":"dwudziesty pierwszy", "22":"dwudziesty drugi", "23":"dwudziesty trzeci", "24":"dwudziesty czwarty", "25":"dwudziesty piąty", "26":"dwudziesty szósty", "27":"dwudziesty siódmy", "28":"dwudziesty ósmy", "29":"dwudziesty dziewiąty", "30":"trzydziesty", "31":"trzydziesty pierwszy"}
slowa_cofajace = "od nowa"

def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-90)
    engine.say(text)
    engine.runAndWait()
    #print("Słucham Cię")

def get_audio():
    print("Słucham Cię")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="pl")
            print(said)
        except Exception as e:
            print("Exception: " + str(e))           
    return said

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
 
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(ile_dni, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time 
    koniec = datetime.datetime.today().date() + timedelta(days = ile_dni)
    koniec = datetime.datetime.combine(koniec, datetime.datetime.max.time())
    #ustalenie daty za odpowiednia liczbe dni
    utc = pytz.UTC
    koniec = koniec.astimezone(utc)
    koniec = koniec + timedelta(hours=2)
    #przystosowanie daty do odpowiedniego formatu: z "rok-mies-dzien godz:min:sek+00:00" na "rok-mies-dzienTgodz:min:sekZ"
    koniec = str(koniec).replace(" ", "T")
    koniec = str(koniec).replace("+00:00", "Z")
    print(f'Pobieram zaplanowane wydarzenia z następnych {ile_dni} dni.')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=koniec, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    start_list = []
    summary_list = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('date', event['start'].get('date'))
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        start = start.date()
        #speak("Dnia " + start + " masz następujące wydarzenia:")
        #if ((start - datetime.datetime.today().date()) < timedelta(days = ile_dni)):

        #pomoc do formatowania czasu http://strftime.org/
        #zmiana daty na taka do przeczytania
        start = start.strftime("%d%B")
        dzien_liczba = start[0:2]
        dzien_slowo = SLOWNIK_DNI_MIESIACA[dzien_liczba]
        ang_month = start[2:]
        pol_month = SLOWNIK_MIESIACE[ang_month]
        start = start.replace(dzien_liczba,dzien_slowo)
        start = start.replace(ang_month,pol_month)
        #zrobienie list z datami i z tytulami zeby potem w petli wyswietlac
        start_list.append(start)
        summary_list.append(event['summary'])

        #wyswietlanie w petli - jesli dzien sie nie zmienia to nie jest czytana data - dzieki temu wszystkie wydarzenia z jednego dnia są czytane razem
        czy_zmiana_dnia = ""
    for index, (start, summary) in enumerate(zip(start_list,summary_list)):
        if czy_zmiana_dnia != start:
            speak(start)
        speak(summary)
        czy_zmiana_dnia = start
    speak("Czy potrzebujesz czegoś jeszcze?")
    print("Jeśli tak to zacznij znowu od przywitania.")
    
def get_actual_time():
    speak("Aktualnie jest: " + datetime.datetime.now().time().strftime('%H:%M'))
    speak("Czy potrzebujesz czegoś jeszcze?")
    print("Jeśli tak to zacznij znowu od przywitania.")

def make_event(service, data, nazwa):
    event = {
        'summary': nazwa,
        #'description': tresc,
        'start':{
            'date': data
            #'datetime': "2019-09-11T10:00:00Z",
            #'timezone': "Europe/Warsaw"
        },
        'end':{
            'date': data
            #'datetime': "2019-09-11T15:00:00Z",
            #'timezone': "Europe/Warsaw"
        }
    }    

    event = service.events().insert(calendarId ='primary', body = event).execute()

def get_date(text):
    text= text.lower()
    today = datetime.date.today()

    # zwraca date dla dni: "DZIŚ" "JUTRO" "POJUTRZE"
    if (text.count(JUTRO[0]) > 0) | (text.count(JUTRO_2[0]) > 0):
        return today
    elif (text.count(JUTRO[1]) > 0):
        return today + timedelta(days = 1)
    elif (text.count(JUTRO[2]) > 0):
        return today + timedelta(days = 2)

    #wprowadzenie zmiennych
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    #wybranie miesiąca
    for word in text.split():
        if (word in MONTHS):
            month = MONTHS.index(word)+1
        elif (word in MONTHS_2):
            month = MONTHS_2.index(word)+1
        elif (word.isdigit()):
            day = int(word)
        elif (word in DNI_TYGODNIA):
            day_of_week = DNI_TYGODNIA.index(word)+1

    #ustalenie dnia miesiąca
    for i in range(0,len(DNI_MIESIACA)):
        if (DNI_MIESIACA[i] in text):
            day = i + 1
        elif (DNI_MIESIACA_2[i] in text):
            day = i + 1

    # ustalenie miesiąca jeśli podany jest sam dzień miesiąca i jeśli podany dzień miesiąca już był
    if (today.day > day) & (month == -1):
        month = (today.month + 1)%12
    elif (today.day < day) & (month == -1):
        month = today.month

    # ustalenie roku jeśli podany jest miesiąc, który w obecnym roku już był
    if today.month > month:
        year = (year + 1)

    if (day_of_week != -1) & (day == -1) & (month == -1):
        current_day_of_week = today.weekday()
        dzien = today+timedelta(days = (abs(current_day_of_week-day_of_week)-1))
        year = dzien.year
        month = dzien.month
        day = dzien.month

    return datetime.date(year = year, month = month, day = day)

def get_actual_weather(city, weather_key):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units': 'metric', 'lang': 'pl'}
    response = requests.get(url,params = params)
    weather = response.json()

    #print(weather)
    datagodzina = datetime.datetime.fromtimestamp(weather['dt'])
    godzina = datagodzina.time().strftime('%H:%M')
    temperatura = round(weather['main']['temp'])
    ogolnie = weather['weather'][0]['description']
    powiedz_prognoze = "Pogoda dla miasta: " + str(city) + ". Aktualnie jest: " + str(godzina) + ". Temperatura wynosi: " + str(temperatura) + " stopni Celcjusza. Jest: " + str(ogolnie) + "." 
    speak(powiedz_prognoze)
    speak("Czy potrzebujesz czegoś jeszcze?")
    print("Jeśli tak to zacznij znowu od przywitania.")

def powiedz_pogode():
    speak("Podaj miasto dla którego mam Ci podać aktualną pogodę")
    #dopóki nie uda się wyszukać miasta w api to bedzie sie powtarzalo pytanie o miasto
    udane = False
    while not udane:
        text = get_audio()
        if ("dzięk" in text):
            break

        try:
            get_actual_weather(text, weather_key)
            udane = True        
        except Exception:
            speak("Nie udało się znaleźć takiego miasta. Podaj jeszcze raz.")

def stwórz_wydarzenie():
    speak("Podaj datę tego wydarzenia.")
    data = ""
    while data == "":
        text = get_audio().lower()
        try:
            data = get_date(text)
        except Exception:
            data = ""
            speak("Wystąpił błąd. Podaj ponownie datę.")

    speak("Jak mam nazwać to wydarzenie?")
    text = get_audio().capitalize()
    make_event(service,str(data),text)
    speak("Stworzono wydarzenie. Czy potrzebujesz czegoś jeszcze?")
    print("Jeśli tak to zacznij znowu od przywitania.")

service = authenticate_google()

print("Przywitaj się ze mną aby rozpocząć")
text = ""
while ("dzięk" not in text):
    #przywitanie - rozpoczęcie rozmowy - później zmienione na słowa kluczowe typu "hej google"
    if ("dzień dobry" in text) | ("siem" in text) | ("cześć" in text):
        bufor = 0
        while(("pogod" not in text) & ("temperat" not in text) & ("tworz" not in text) & ("twórz" not in text) & ("doda" not in text) & ("wydarzeni" not in text) & ("kalendarz" not in text) & ("plan" not in text) & ("najbliższ" not in text) & ("któr" not in text) & ("godzin" not in text)):
        #czy pierwszy raz probojemy podac komende czy któryś
            if(bufor == 0):
                speak("W czym mogę Ci pomóc?")
                text = get_audio().lower()
            elif (bufor > 0):
                speak("Nie zrozumiano polecenia. Podaj jeszcze raz")
                text = get_audio().lower()
            
            #jesli chce sie sprawdzic pogode
            if ("pogod" in text) | ("temperat" in text):
                powiedz_pogode()
            elif("któr" in text) | ("godzin" in text):
                get_actual_time()
            #jesli chce sie zrobic cos z wydarzeniami w google - kalendarzem - zmienic na prosta rzecz - jesli slyszy sie "kalendarz", "wydarzenie", "plany" to pytaj co dalej z tym zrobić
            elif("twórz" in text) | ("tworz" in text) | ("doda" in text):
                stwórz_wydarzenie()
            elif("plan" in text) | ("najbliższ" in text):
                get_events(7,service)
            elif (("wydarzeni" in text) | ("kalendarz" in text)) & ("twórz" not in text) & ("tworz" not in text) & ("doda" not in text):
                while ("tworz" not in text) & ("twórz" not in text) & ("doda" not in text) & ("plan" not in text) & ("najbliższ" not in text):
                    speak("Chcesz utworzyć nowe wydarzenie czy usłyszeć co masz w najbliższych planach?")
                    text = get_audio().lower()
                    if ("tworz" in text) | ("twórz" in text) | ("doda" in text):
                        stwórz_wydarzenie()
                    elif ("plan" in text) | ("najbliższ" in text):
                        #speak("Z ilu najbliższych dni chcesz uszłyszeć swoje zaplanowane wydarzenia?")
                        #text = get_audio() - jesli nie bedzie dzialac na te odmiany liczebnikow to zrobic trzeba słowik i while
                        get_events(7, service)
            else:
                bufor+=1
    text = get_audio().lower()

#zakończenie - pożegnanie
speak("Do usłyszenia.")

'''
try:
    data = get_date(text)
except Exception as e:
    print("Nie udało się rozpoznać daty: " + str(e))

make_event(service,str(data))

get_events(120,service)
'''
