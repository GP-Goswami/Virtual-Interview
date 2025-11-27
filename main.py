from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from inter import takeaudio,speak
from pydantic import BaseModel, ConfigDict, ValidationError
from fastapi.responses import FileResponse
from database import human


interview_id = ""
job_info="AI Developer"
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/user-input")
def readbot():
    inter_reply = takeaudio()
    return inter_reply

@app.get("/")
def readbot():
    return "I am bot"

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


class interRequire(BaseModel):
    interview_id    : str
    inter_reply : str
    resume : str
    # model_config = ConfigDict(extra='forbid')
    
# class ChatResponse(BaseModel):
#     reply: str
    
@app.post("/model-output")
async def aiInter(interData : interRequire):
    try:
        # inter_reply = takeaudio()
        # speak(inter_reply)
        gem_res = human(interData.interview_id, interData.inter_reply, interData.resume, job_info)
        
        if gem_res is None:
            raise ValueError("human() returned None")
        print("gem_res",gem_res)
        # speak(gem_res)
        # return ChatResponse(reply=gem_res)
        return gem_res
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))