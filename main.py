from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from inter import takeaudio,speak
from pydantic import BaseModel, ConfigDict, ValidationError
from fastapi.responses import FileResponse
from database import human

interview_id = ""
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/user-input")
def readbot():
    inter_reply = takeaudio()
    
    return "hii bot"

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


class Model(BaseModel):
    interview_id    : str
    # model_config = ConfigDict(extra='forbid')
    
# class ChatResponse(BaseModel):
#     reply: str
    
@app.get("/model-output")
async def aiInter(interview_id:Model):
    try:
        inter_reply = takeaudio()
        # speak(inter_reply)
        gem_res = human(interview_id.interview_id, inter_reply)
        
        if gem_res is None:
            raise ValueError("human() returned None")
        print("gem_res",gem_res)
        # speak(gem_res)
        # return ChatResponse(reply=gem_res)
        return gem_res
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))