# Voice Assistant (PL)

<p align="left">
    <img src="https://img.shields.io/github/stars/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/watchers/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/commit-activity/t/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/last-commit/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/issues/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/languages/top/msarnacki/voice_assistant"/>
    <img src="https://img.shields.io/github/repo-size/msarnacki/voice_assistant"/>
</p>

I made this program back in September 2019. Assistant is **based on keywords** (in fact on parts of keywords) and **speech recognition**. 
The language it is listening to is **Polish**, so it doesn't work well with English but it is easly changable by changing language argument in recognize_google function to "en-US".

Voice assistant is capable of telling the **actual weather in any city you want**, **adding events to your google calendar** or **reading out events for the upcoming week**.
To get it working you need to go to [Google API Console](console.developers.google.com), create new project, choose google calendar api and download credentials and put the file in the same directory as the project.
You also need openweathermap api working and put api-key in variable `weather_key` in the weather_api.py file in same directory as rest of the project.

During making the program I learned a lot about **using different APIs**. I also learned so much about working with **datetime**.

## How does it work?
To start assistant to work you need to say hello to him (in polish it is looking for "dzień dobry", "siema" or "cześć").
After that assistant asks what can it do for us. Here we can choose one from the options:
- check weather in chosen city (parts of keywords are: "pogod" or "temperat")
  - assistant asks for the city you want to check weather
- ask what time is it (parts of keywords are: "któr" or "godzin")
- create new event in your google calendar (parts of keywords are: "twórz", "tworz" or "doda")
  - assistant asks when event will happen
  - assistant asks how to name that event
- read out events that are planned for next 7 days (parts of keywords are: "plan" or "najbliższ")
- for the last 2 options there are also a possiblity to call it by "wydarzeni" or "kalendarz"
  - assistant asks if you want to add new event or get events for next 7 days (keywords like in points above)

## Technologies used:
- Python 3
- speech_recognition
- pyttsx3
- google-calendar-api
- openweathermap-api
- requests
- datetime
