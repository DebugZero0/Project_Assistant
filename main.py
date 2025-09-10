import speech_recognition as sr
import webbrowser 
import pyttsx3
import time
import musicLib
import google.generativeai as genai 
import os 

genai.configure(api_key="AIzaSyDhFVgb1y0R_f1c9TVwGQznWch26RXLlgw") 

def aiPrompt(c):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(c)
    print("AI Response:", response.text)
    return response.text  


def process_command(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "play" in c.lower():
        song =c.lower().split(" ")[1]
        link=musicLib.music[song] 
        webbrowser.open(link)
    else:
        output=aiPrompt(c)
        speak(output)



def speak(text):
    """
    Speak the given text reliably by initializing a new engine each time.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        engine.say(text) 
        engine.runAndWait()
        engine.stop()  # ensure engine is released
    except Exception as e:
        print("TTS Error:", e)
    time.sleep(0.1)  # small pause to avoid overlap 
 
if __name__ == "__main__":
    speak(" Initializing Jarvis") 
    while True:    
        r = sr.Recognizer()
        # Recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=7,phrase_time_limit=5)  
                word = r.recognize_google(audio) 
                if word.lower() in ["exit", "quit", "stop"]:
                    print("Exiting...") 
                    speak("Goodbye") 
                    break
                if(word.lower() == "jarvis"): 
                    print("Jarvis Activated: ") 
                    speak("Yes")
                    # Listen for the command
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        speak("Listening for command...")
                        audio = r.listen(source,timeout=7,phrase_time_limit=5) 
                        try:
                            command = r.recognize_google(audio)
                            if command.lower() in ["exit", "quit", "stop"]:
                                speak("Goodbye!")
                                break
                            print("Command received:", command)
                            process_command(command)  # Uncomment and define if needed
                        except Exception as e:
                            print("Could not recognize command:", e)
                            speak("Sorry, I did not catch that.")

        except Exception as e: 
            print("No prompt was given".format(e))  


