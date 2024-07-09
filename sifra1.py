import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
import wikipedia
from requests import get
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import time
import pyautogui
import PyPDF2
import operator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
from bs4 import BeautifulSoup
import psutil
import speedtest
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from sifra import Ui_SifraGUI
from PyQt5.QtCore import QThread

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if hour >= 0 and hour < 12:
        speak(f"Good morning! It's {tt}")
    elif hour >= 12 and hour < 18:
        speak(f"Good afternoon! It's {tt}")
    else:
        speak(f"Good evening! It's {tt}")
    speak("I am Sifra, ma'am. Please tell me how I can help you.")

def send_mail(to, subject, content, file_path=None):
    email = "bhavya.anand27@gmail.com"
    password = "27082004bA@"
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        if file_path:
            filename = os.path.basename(file_path)
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to, text)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("I am not able to send this email.")
        print(e)

def pdf_reader():
    try:
        book_path = input("Enter the path to the PDF: ")
        book = open(book_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(book)
        pages = pdf_reader.numPages
        speak(f"Total number of pages are {pages}")
        speak("Enter the page number from where I have to read")
        pg = int(input("Please enter the page number: "))
        if 0 <= pg < pages:
            page = pdf_reader.getPage(pg)
            text = page.extractText()
            speak(text)
        else:
            speak("Invalid page number.")
    except Exception as e:
        speak("An error occurred while reading the PDF.")
        print(e)

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
    }[op]

def eval_binary_expr(op1, oper, op2):
    op1, op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)

def get_weather(city):
    search = f"temperature in {city}"
    url1 = f"https://www.google.com/search?q={search}"
    r = requests.get(url1)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"Current temperature in {city} is {temp}")

def check_battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"The system has {percentage} percent battery remaining")

def check_internet_speed():
    st = speedtest.Speedtest()
    dl = st.download() / 1_000_000  # Convert to Mbps
    up = st.upload() / 1_000_000    # Convert to Mbps
    speak(f"Ma'am, we have {dl:.2f} Mbps download speed and {up:.2f} Mbps upload speed.")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    def run(self):
        self.main_task()
    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source, timeout=1, phrase_time_limit=30)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except Exception as e:
            speak("Say that again please...")
            return 'none'
        return query.lower()

    def main_task(self):
        wish()
        while True:
            self.query = self.take_command()
            
            if "open notepad" in self.query:
                path = r"C:\Windows\System32\notepad.exe"
                os.startfile(path)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "play music" in self.query:
                music_dir = "E:\\music"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "ip address" in self.query:
                ip = get("https://api.ipify.org").text
                speak(f"Your IP address is: {ip}")

            elif "wikipedia" in self.query:
                speak("Searching Wikipedia...")
                speak("what should I search on wikipedia?")
                s = self.take_command().lower()
                query = query.replace("wikipedia", s)
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There were multiple results for your query. Please be more specific.")
                except wikipedia.exceptions.PageError as e:
                    speak("I couldn't find a page matching your query.")
                except wikipedia.exceptions.WikipediaException as e:
                    speak("An error occurred while fetching information from Wikipedia.")
                except Exception as e:
                    speak("An unexpected error occurred.")
                    print(e)

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open chat GPT" in self.query:
                webbrowser.open("chatGPT.com")

            elif "open google" in self.query:
                speak("What should I search on Google?")
                cm = self.take_command().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")

            elif "send message" in self.query:
                speak("What is the message?")
                cm = self.take_command().lower()
                speak("tell at what hour")
                hr = self.take_command().lower()
                speak("tell at what minute")
                min = self.take_command().lower()
                kit.sendwhatmsg("+9899218749", cm, int(hr), int(min))
                time.sleep(5)
                speak("Message has been sent.")

            elif "play songs on youtube" in self.query:
                speak("what song should I play")
                cm = self.take_command().lower()
                kit.playonyt(cm)

            elif "email" in self.query:
                try:
                    speak("What should be the subject?")
                    subject = self.take_command().lower()
                    speak("What should I say?")
                    content = self.take_command().lower()
                    speak("Do you want to attach any file? Say yes or no.")
                    attach = self.take_command().lower()
                    file_path = None
                    if "yes" in attach:
                        speak("Enter the path to the file")
                        file_path = input("Path: ")

                    send_mail("anandbhavya027@gmail.com", subject, content, file_path)
                except Exception as e:
                    speak("Sorry, I couldn't send the email.")
                    print(e)

            elif "no thanks" in self.query or "no thank you" in self.query:
                speak("Have a good day!")
                sys.exit()

            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("tell me if you want to hide or make file visible to everyone")
                cond = self.take_command().lower()
                if "hide" in cond:
                    os.system("attrib +h /s /d")
                    speak("all files are hidden now")
                elif "visible" in cond:
                    os.system("attrib -h /s /d")
                elif "leave it" in cond:
                    speak("ok mam")
            
            elif "close notepad" in self.query:
                speak("Closing notepad.")
                os.system("taskkill /f /im notepad.exe")

            elif "set alarm" in self.query:
                speak("Please enter the time in HH:MM format:")
                alarm_time = input("Enter the time in HH:MM format: ")
                current_time = datetime.datetime.now().strftime("%H:%M")
                while current_time != alarm_time:
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    time.sleep(1)
                speak("Wake up! It's time!")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "volume up" in self.query:
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                pyautogui.press("volumedown")

            elif "mute" in self.query:
                pyautogui.press("volumemute")

            elif "unmute" in self.query:
                pyautogui.press("volumeunmute")

            elif "screenshot" in self.query:
                screenshot = pyautogui.screenshot()
                screenshot.save("screenshot.png")
                speak("Screenshot taken.")

            elif "cpu usage" in self.query:
                cpu_usage = psutil.cpu_percent()
                speak(f"Current CPU usage is {cpu_usage}%")

            elif "memory usage" in self.query:
                memory_info = psutil.virtual_memory()
                speak(f"Current memory usage is {memory_info.percent}%")

            elif "search on google" in self.query:
                speak("What should I search on Google?")
                query = self.take_command().lower()
                webbrowser.open(f"https://www.google.com/search?q={query}")

            elif "search on youtube" in self.query:
                speak("What should I search on YouTube?")
                query = self.take_command().lower()
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

            elif "news" in self.query:
                webbrowser.open("https://www.bbc.com/news")

            elif "weather" in self.query:
                speak("Please tell the city name.")
                city = self.take_command().lower()
                get_weather(city)

            elif "shutdown" in self.query:
                speak("Are you sure you want to shut down the computer?")
                confirmation = self.take_command().lower()
                if "yes" in confirmation:
                    os.system("shutdown /s /t 1")

            elif "restart" in self.query:
                speak("Are you sure you want to restart the computer?")
                confirmation = self.take_command().lower()
                if "yes" in confirmation:
                    os.system("shutdown /r /t 1")

            elif "log off" in self.query:
                speak("Are you sure you want to log off the computer?")
                confirmation = self.take_command().lower()
                if "yes" in confirmation:
                    os.system("shutdown /l")

            elif "battery status" in self.query:
                check_battery()

            elif "internet speed" in self.query:
                check_internet_speed()

startExecution = MainThread()

class SifraUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SifraGUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QMovie("C:\\Users\\Bhavya Anand\\Downloads\\7kmF.gif")
        self.ui.label.setMovie(self.ui.movie)  # Assuming label is correctly named in Ui_SifraGUI
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
sifra = SifraUI()
sifra.show()
exit(app.exec_())
