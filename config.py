# from app import inter
interConfigId=""
def interContinue(interview_id):
    global interConfigId
    interConfigId=interview_id
    return interConfigId

def retriveid():
    print("--->interconfigid",interConfigId)
    return interConfigId
