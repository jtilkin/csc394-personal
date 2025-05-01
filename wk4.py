from fastapi import FastAPI, HTTPException
import openai
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

api_key = "PUT_API_KEY_HERE"

# ---------- SQLite Setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./jobberwobber.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------- SQLAlchemy Model ----------
class UserDB(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

class EmployerDB(Base):
    __tablename__ = "employers"
    employer_id = Column(Integer, primary_key=True)
    employer_name = Column(String)
    username = Column(String)

class JobListingDB(Base):
    __tablename__ = "listings"
    listing_id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    type = Column(String)
    experience = Column(String)
    salary = Column(String)

## create tables if they don't exist
Base.metadata.create_all(bind=engine)

# ---------- Pydantic Models ----------
class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True

class Employer(BaseModel):
    employer_id: int
    employer_name: str
    username: str

    class Config:
        orm_mode = True

class JobListing(BaseModel):
    listing_id: int
    title: str
    location: str
    type: str
    experience: str
    salary: str

    class Config:
        orm_mode = True

# ---------- FastAPI App ----------
app = FastAPI()

# ---------- Routes ----------
@app.get("/users/", response_model=List[User])
def read_users():
    with SessionLocal() as session:
        users = session.query(UserDB).all()
        return users

@app.post("/users/", response_model=User)
def create_user(user: User):
    with SessionLocal() as session:
        db_user = UserDB(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    with SessionLocal() as session:
        user = session.query(UserDB).filter(UserDB.user_id == user_id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        session.delete(user)
        session.commit()
        return user



@app.get("/employers/", response_model=List[Employer])
def read_employers():
    with SessionLocal() as session:
        employers = session.query(EmployerDB).all()
        return employers

@app.post("/employers/", response_model=Employer)
def create_employer(employer: Employer):
    with SessionLocal() as session:
        db_employer = EmployerDB(**employer.dict())
        session.add(db_employer)
        session.commit()
        session.refresh(db_employer)
        return db_employer

@app.delete("/employers/{employer_id}", response_model=Employer)
def delete_employer(employer_id: int):
    with SessionLocal() as session:
        employer = session.query(EmployerDB).filter(EmployerDB.employer_id == employer_id)
        if not employer:
            raise HTTPException(status_code=404, detail="employer not found")
        session.delete(employer)
        session.commit()
        return employer



@app.get("/listings/", response_model=List[JobListing])
def read_listings():
    with SessionLocal() as session:
        listings = session.query(JobListingDB).all()
        return listings

@app.post("/listings/", response_model=JobListing)
def create_listing(listing: JobListing):
    with SessionLocal() as session:
        db_listing = JobListingDB(**listing.dict())
        session.add(db_listing)
        session.commit()
        session.refresh(db_listing)
        return db_listing

@app.delete("/listings/{listing_id}", response_model=JobListing)
def delete_listing(listing_id: int):
    with SessionLocal() as session:
        listing = session.query(JobListingDB).filter(JobListingDB.listing_id == listing_id)
        if not listing:
            raise HTTPException(status_code=404, detail="listing not found")
        session.delete(listing)
        session.commit()
        return listing
    


# ---------- HW3 Suggestions with OpenAPI ----------
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