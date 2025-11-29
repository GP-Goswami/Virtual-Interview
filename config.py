# from app import inter
interConfigId=""
def interContinue(interview_id):
    global interConfigId
    interConfigId=interview_id
    return interConfigId

def retriveid():
    return interConfigId
