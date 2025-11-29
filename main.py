from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from inter import takeaudio,speak
from pydantic import BaseModel, ConfigDict, ValidationError
from fastapi.responses import FileResponse
from database import human
from config import retriveid

interview_id = ""
job_info="AI Developer"
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/user-input")
def readbot():
    inter_reply = takeaudio()
    return inter_reply

@app.get("/interviewId")
def getInterid():
    inter = retriveid()
    return inter

@app.get("/")
def readbot():
    return "I am bot"

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


class speakAudio(BaseModel):
    interviewerReply : str
    
@app.post("/speakAns")
async def speakAI(speakData : speakAudio):
    try:
        if speakData.interviewerReply!="":
            speak(speakData.interviewerReply)
        return "done"
    except Exception as e:
        return f"error in speakai {e}"


class interRequire(BaseModel):
    inter_reply : str
    resume : str
  
    
@app.post("/model-output")
async def aiInter(interData : interRequire):
    try:
        if retriveid()!="":
            global interview_id
            interview_id=retriveid()
            print("interview_id", interview_id)
        gem_res = human(interview_id, interData.inter_reply, interData.resume, job_info)
        
        if gem_res is None:
            raise ValueError("human() returned None")
        print("gem_res",gem_res)
        return gem_res
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))