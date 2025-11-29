import uuid
import json
import os
from pymongo import MongoClient
from inter import takeaudio
from gem import gem_res
from config import interContinue
from dotenv import load_dotenv, find_dotenv
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
cluster_name = os.getenv("cluster_name")
mongodb_uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.vspaxpf.mongodb.net/?appName={cluster_name}"
print("url is ",mongodb_uri, MONGO_USERNAME,MONGO_PASSWORD,cluster_name)

client = MongoClient(mongodb_uri)
print("Connected successfully!")

db = client["interview"]
collection = db["stud_inter"]


def checkId(interview_id):
    foundId = collection.find_one({"interview_id": interview_id})
    return foundId

# take user input and store to databases
def human(interview_id, inter_reply, resume, job_info):
    try:
        existing = checkId(interview_id)
        # (type(existing), existing)
        if not existing:
            interview_id = str(uuid.uuid4())
            collection.insert_one({
                "interview_id": interview_id,
                "stud_info": [{
                    "role": "user",
                    "parts": [
                            {"text": inter_reply}
                    ]
                }]

            })
            interContinue(interview_id)

        else:
            collection.update_one(
                {"interview_id": interview_id},
                {"$push":
                    {
                        "stud_info": {
                            "role": "user",
                            "parts": [
                                {"text": inter_reply}
                            ]
                        }
                    }
                 }
            )

        existing = checkId(interview_id)
        reply = gem_res(existing, resume, job_info)

        if reply or "Error is " not in reply:
            collection.update_one(
                {"interview_id": interview_id},
                {"$push":
                 {
                     "stud_info": {
                         "role": "model",
                         "parts": [
                             {"text": reply}
                         ]
                     }
                 }
                 }
            )
        return (reply)
    except Exception as e:
        print(f"error is {e}")


if __name__ == "__main__":
    interview_id = ""
    inter_reply = takeaudio()
    while inter_reply != "exit":
        interview = human(interview_id, inter_reply)
        # gem_reply(interview, inter_reply)
