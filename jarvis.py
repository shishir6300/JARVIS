import json
import os
import time
import webbrowser
from difflib import get_close_matches
from ppadb.client import Client as AdbClient
import AppOpener as ap
import cv2
import maskpass
import mediapipe as mp
import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import randfacts
import requests
import speech_recognition as sr
from bs4 import BeautifulSoup
from googlesearch import search

from greeting import greet

s=pyttsx3.init()

def load_knowledge_base(file_path:str)->dict:
    with open(file_path,'r') as file:
        data:dict = json.load(file)
    return data
def save_knowledge_base(file_path:str,data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)
def find_best_match(user_question:str,questions:list[str])->str| None:
    matches: list=get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None
def get_answer_for_question(question: str,knowledge_base: dict)-> str| None:
    for q in knowledge_base['questions']:
        if q['question']== question:
            return q['answer']
def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    while True:
        rec = sr.Recognizer()
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, duration=0.2)
                audio = rec.listen(mic)
                text= rec.recognize_google(audio)
                text = text.lower()
                print('YOU: ',text)
        except:
            print('BALU: speak properly')
            chat_bot()
        text=rec.recognize_google(audio)
        user_input=text
        if 'search' in user_input:
            f=user_input.replace('search','')
            url = f'https://www.google.com/search?q={f}'
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            mysearch = (soup.find('div', class_='BNeawe')).text
            print(f'BALU:{mysearch}')
            s=pyttsx3.init()
            s.say(mysearch)
            s.runAndWait()
            for j in search(f, 5):
                print(j)
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'joke' in user_input:
            res = pyjokes.get_joke(language='en', category='all')
            s = pyttsx3.init()
            print(f'BALU:{res}')
            s.say(res)
            s.runAndWait()
            chat_bot()
            x=input('Press enter for next command: ')
            if x=='':
                chat_bot()
        if 'play song' in user_input:
            d = user_input.split()
            x = ' '.join(d[2:])
            webbrowser.open(f'https://open.spotify.com/search/{x}')
            time.sleep(8)
            pyautogui.moveTo(x=1166, y=665)
            time.sleep(2)
            pyautogui.click(x=1166, y=665)
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'temperature' in user_input:
            city = "hyderabad"
            url = "https://google.com/search?q=weather+in+" + city
            request_result = requests.get(url)
            soup = BeautifulSoup(request_result.text, "html.parser")
            temp = soup.find("div", class_='BNeawe').text
            print(temp)
            s=pyttsx3.init()
            s.say(temp)
            s.runAndWait()
            x=input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'switch window' in user_input:
            pyautogui.hotkey('alt','tab')
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'random fact' in user_input or 'fact' in user_input:
            x = randfacts.get_fact()
            print(x)
            s=pyttsx3.init()
            s.say(x)
            s.runAndWait()
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'alarm' in user_input:
            s=pyttsx3.init()
            s.say('sure! can u specify the time')
            s.runAndWait()
            print("input time example:- 10,10,10")
            a = input("Please tell the time :- ")
            alarm(a)
            s.say("Done")
            s.runAndWait()
            x=input('Press enter for next command: ')
            if x=='':
                chat_bot()
        if 'message' in user_input:
            s = pyttsx3.init()
            s.say('enter the number')
            s.runAndWait()
            w1 = input('enter the number: ')
            s.say('enter your message')
            s.runAndWait()
            w2 = input('enter message: ')
            s.say('enter time')
            s.runAndWait()
            w3 = int(input('enter hour: '))
            w4 = int(input('enter minutes: '))
            pywhatkit.sendwhatmsg('+91' + w1, w2, w3, w4)
            print("Successfully Sent!")
            x=input('Press enter for next command: ')
            if x=='':
                chat_bot()

        if 'open youtube' in user_input:
            webbrowser.open('https://www.youtube.com/results?search_query={d}')
            x=input('Press enter for next command: ')
            if x=='':
                chat_bot()
        if 'open' in user_input:
            a=user_input.split()
            ap.open(' '.join(a[1:]))
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'close' in user_input:
            a=user_input.split()
            ap.close(' '.join(a[1:]))
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'battery percentage' in user_input or 'battery' in user_input:
            b = psutil.sensors_battery()
            k = b.percent
            print(k)
            s=pyttsx3.init()
            s.say(f'your battery percentage is {k}')
            s.runAndWait()
            x=input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'shutdown' in user_input or 'shut down' in user_input:
            s=pyttsx3.init()
            s.say('do you really want me to shutdown the pc')
            s.runAndWait()
            d=input('yes/no: ')
            e=d.lower()
            if e=='yes':
                s.say('your pc will shutdown in 5 seconds')
                pywhatkit.shutdown(time=5)
            else:
                chat_bot()
        if user_input=='exit':
            s=pyttsx3.init()
            s.say('thank you for using me, you can call me anytime')
            s.runAndWait()
            exit()
        if 'any games' in user_input:
            s=pyttsx3.init()
            s.say('yeah! i have a snake game which is super interesting , do you want to play?')
            s.runAndWait()
            c=input('yes/no: ')
            c.lower()
            if c=='yes':
                os.startfile('characters.py')
            else:

                chat_bot()
            x=input('Press enter for next command: ')
            if x=='':
                chat_bot()
        if 'screenshot' in user_input:
            t = pyautogui.screenshot()
            t.save('t.png')
            s=pyttsx3.init()
            s.say('screenshot taken')
            s.runAndWait()
            x = input('Press enter for next command: ')
            if x == '':
                chat_bot()
        if 'connect to my phone' in user_input:
            client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
            devices = client.devices()
            device = devices[0]
            s=pyttsx3.init()
            s.say('connected to phone')
            s.runAndWait()
            s.say('how can i help you')
            s.runAndWait()
            while True:
                rec = sr.Recognizer()
                try:
                    with sr.Microphone() as mic:
                        rec.adjust_for_ambient_noise(mic, duration=0.2)
                        audio = rec.listen(mic)
                        text = rec.recognize_google(audio)
                        text = text.lower()
                        print('YOU: ', text)
                except:
                    print('BALU: speak properly')
                text = rec.recognize_google(audio)
                text = text.lower()
                if 'call' in text:
                    alpha = {'a': (110, 1860), 'b': (666, 2032), 'c': (453, 2034), 'd': (335, 1905), 'e': (270, 1748),
                             'f': (440, 1899),
                             'g': (527, 1886), 'h': (626, 1888),
                             'i': (807, 1723), 'j': (740, 1883), 'k': (847, 1888), 'l': (950, 1861), 'm': (845, 2026),
                             'n': (741, 2045),
                             'o': (896, 1725), 'p': (1006, 1734),
                             'q': (50, 1725), 'r': (384, 1741), 's': (208, 1885), 't': (481, 1762), 'u': (698, 1738),
                             'v': (531, 2016),
                             'w': (170, 1736), 'x': (326, 2045),
                             'y': (601, 1740), 'z': (223, 2040), ' ': (572, 2181)}
                    text=text.replace('call','')
                    device.shell('input tap 166 2138')
                    time.sleep(2)
                    device.shell('input tap 459 235')
                    time.sleep(2)
                    for digit in text:
                        device.shell(f"input tap {alpha[digit][0]} {alpha[digit][1]}")
                    time.sleep(2)
                    device.shell('input tap 976 556')
                    y=input('press enter for next command')
                    if y=='':
                        chat_bot()

        if 'volume' in user_input or 'hand gesture' in user_input:
            cap = cv2.VideoCapture(0)
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)
            mp_drawing = mp.solutions.drawing_utils
            while 1:
                try:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                            if index_finger_y < thumb_y:
                                hand_gesture = 'pointing up'
                            elif index_finger_y > thumb_y:
                                hand_gesture = 'pointing down'
                            else:
                                hand_gesture = 'other'
                            if hand_gesture == 'pointing up':
                                pyautogui.press('volumeup')
                            elif hand_gesture == 'pointing down':
                                pyautogui.press('volumedown')
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                except KeyboardInterrupt:
                    chat_bot()


        best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])
        if best_match:
            answer:str=get_answer_for_question(best_match,knowledge_base)
            print(f'BALU:{answer}')
            s=pyttsx3.init()
            s.say(answer)
            s.runAndWait()
        else:
            try:
                s=pyttsx3.init()
                print('BALU: I do not know the answer. Can you teach me?')
                s.say(' I do not know the answer. Can you teach me?')
                s.runAndWait()
                new_answer=input('Type the answer or "skip" to skip:')
                if new_answer.lower()!= 'skip':
                    knowledge_base['questions'].append({'question':user_input,'answer':new_answer})
                    save_knowledge_base('knowledge_base.json',knowledge_base)
                    print('BALU: Thank You! I learned a new response!')
                    s.say(' Thank You! I learned a new response!')
                    s.runAndWait()
            except:
                chat_bot()

s=pyttsx3.init()
s.say('hello! i am Jarvis , your personal AI , to gain my access enter the password')
s.runAndWait()
u=maskpass.askpass('enter password: ','*')
p='6300221726'
if u==p:
    greet()
    chat_bot()
else:
    s.say('sorry the entered password is wrong')
    s.runAndWait()

