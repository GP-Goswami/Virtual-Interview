from google import genai
import os
import json
from google.genai import types
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gem_res(stud_data , resume, job_info):
    try:
        stud = stud_data
        if stud:
            his = stud["stud_info"]

            gem_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=his,
                config=types.GenerateContentConfig(
                    system_instruction=f"""role: You are a Interviewer of candidates. You have to take it on the basis per resume and 
                    company need.
                    working: you have to take resume and read it and ask question related to resume and requirement
                    for requirement i will provide you link of company. You have read web and find out requirement
                    
                    instruction:- you have only 5 turn to complete interview you have to complete interview in this 5 chance.
                    at first time always ask about candidate introduction then proceed next
                    inputs: {resume}, company {job_info}"""
                )
            )
            
            res = gem_response.candidates[0].content.parts[0].text
            return (res)
        else:
            print("Nothing is found here")
    except Exception as e:
        return f"Error is {e}"
