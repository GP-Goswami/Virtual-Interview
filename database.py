import uuid
import json
from pymongo import MongoClient
from inter import takeaudio
from gem import gem_res
from config import interContinue

client = MongoClient("mongodb://localhost:27017/")
print("Connected successfully!")

db = client["interview"]
collection = db["stud_inter"]


# prompt="you are a Interviewer of the student you have to take interview based on student resume"

# take user input and store to databases
def human(interview_id, inter_reply, resume, job_info):
    try:
        existing = collection.find_one({"interview_id": interview_id})
        # print(type(existing), existing)
        if not existing:
            interview_id = str(uuid.uuid4())
            print("existing", interview_id)
            collection.insert_one({
                "interview_id": interview_id,
                "stud_info": [{
                    "role": "user",
                    "parts": [
                            {"text": inter_reply}
                            # {"text": "Hii my name is Gautam Goswami"}
                    ]
                }]

            })
            # existing = collection.find_one({"interview_id": interview_id})
            interContinue(interview_id)

        else:
            print("yes")
            collection.update_one(
                {"interview_id": interview_id},
                {"$push":
                    {
                        "stud_info": {
                            "role": "user",
                            "parts": [
                                {"text": inter_reply}
                                # {"text": "hii how are you"}
                            ]
                        }
                    }
                 }
            )

        existing = collection.find_one({"interview_id": interview_id})
        print(existing)
        reply = gem_res(existing, resume, job_info)
        print("reS1---->",reply)

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
        # return (inter_reply, reply)
        return (reply)
    except Exception as e:
        print(f"error is {e}")


if __name__ == "__main__":
    interview_id = "2c6bd84f-8971-459c-bf1b-c7e699b5066f"
    inter_reply = takeaudio()
    while inter_reply != "exit":
        interview = human(interview_id, inter_reply)
        # gem_reply(interview, inter_reply)
