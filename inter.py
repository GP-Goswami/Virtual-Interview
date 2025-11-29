import speech_recognition as sr
import pyttsx3

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()




def speak(audio):

    engine = pyttsx3.init('sapi5')  # create fresh instance
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate", 170)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()
# Reading Microphone as source
# listening the speech and store in audio_text variable
def takeaudio():
    # return "hii,how are you"
    with sr.Microphone() as source:
        print("Lestening...")
        r.pause_threshold = 1
        r.energy_threshold = 600 
        audio_text = r.listen(source)
        print("Time over, thanks")
        
        
        try:
            # using google speech recognition
            Inter_res=r.recognize_google(audio_text, language="en-IN")
            print("Text: "+ Inter_res)
            r.recognize_google(audio_text, language="en-IN")
            return Inter_res
        except:
            print("Sorry, I did not get that")
            return "interview is over"
         
if __name__=="__main__" :

    speak("Welcome in AI interview")
    student=takeaudio()