from fastapi import FastAPI, HTTPException
import openai
from openai import OpenAI
from pydantic import BaseModel

api_key = "PUT_API_KEY_HERE"

app = FastAPI()

applications = {
    1: [["Software Engineer", "Google"], ["Software Engineer", "Apple"], ["Software Engineer", "Microsoft"]],
    2: [["Software Engineer", "Apple"], ["Data Scientist", "Spotify"], ["Data Scientist", "Netflix"]],
    3: [["Cloud Engineer", "Amazon"], ["Cloud Engineer", "Google"], ["Cloud Engineer", "Microsoft"]]
}

@app.get("/suggestions")
async def get_suggestions(index: int = 0):
    if index <= 0 or index > len(applications):
        raise HTTPException(status_code = 404, detail = "User not found")
    else:
        try:
            prompt = build_prompt(index)
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"suggestion": response.choices[0].message.content}
        except Exception as e:
            raise HTTPException(status_code = 500, detail = str(e))

def build_prompt(user_id):
    user_applications = applications[user_id]
    user_applications_joined = "; ".join([f"Job Title: {job[0]}, Company: {job[1]}" for job in user_applications])
    prompt = """Give a suggestion for a job title and company to apply to given the job titles and 
                company names a user has had on their past applications. Give only the job title and company name. """ + user_applications_joined
    print(prompt)
    return prompt

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
        
user_list: list[User] = []

@app.get("/users")
async def get_users():
    return {"users": user_list}

@app.post("/users")
async def add_user(user: User):
    user_list.append(user)
    return {"users": user_list}

@app.delete("/users")
async def delete_user(index: int = 0):
    user_list.pop(index)
    return {"users": user_list}



class Employer(BaseModel):
    employer_name: str
    username: str
        
employer_list: list[Employer] = []

@app.get("/employers")
async def get_employers():
    return {"employers": employer_list}

@app.post("/employers")
async def add_employer(employer: Employer):
    employer_list.append(employer)
    return {"employers": employer_list}

@app.delete("/employers")
async def delete_employer(index: int = 0):
    employer_list.pop(index)
    return {"employers": employer_list}



class JobListing(BaseModel):
    title: str
    location: str
    type: str
    experience: str
    salary: str
        
listing_list: list[JobListing] = []

@app.get("/listings")
async def get_listings():
    return {"listings": listing_list}

@app.post("/listings")
async def add_listing(listing: JobListing):
    listing_list.append(listing)
    return {"listings": listing_list}

@app.delete("/listings")
async def delete_listing(index: int = 0):
    listing_list.pop(index)
    return {"listings": listing_list}