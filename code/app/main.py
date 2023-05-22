import json
from typing import Optional, List
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Persons FastApi")


app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        )

# ========== Model =============
class PersonInput(BaseModel):
    first_name: str
    last_name: str
    gender: str
    age: int
    email: str
    phone: str
    city: str
    address: str

class PersonOutput(PersonInput):
    id: int

# ======== Helpers =========

def load_db():
    with open("/home/keys4/app/dummy_db.json") as f:
        return [PersonOutput.parse_obj(el) for el in json.load(f)]

def save_db(persons: List[PersonInput]):
    with open("/home/keys4/app/dummy_db.json", "w") as f:
        json.dump([person.dict() for person in persons], f)


persons = load_db()


# ========= Routes =========

@app.get("/")
async def main():
    return "<h1>Root page: use /api/persons </h1>"


@app.get("/api/persons")
def get_persons(gender: Optional[str] = None, age: Optional[int] = None):
    res = persons
    if gender:
        res = [person for person in persons if person.gender == gender]
    if age:
        res = [person for person in persons if person.age >= age]
    return res


@app.get("/api/persons/{person_id}")
def get_person(person_id: int):
    res = [person for person in persons if person.id == person_id]
    if not len(res):
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Person not found"}
                )
    return res[0]


@app.post("/api/persons", response_model=PersonOutput)
def create_person(data = Body()):
    new_person = PersonOutput(
        id=len(persons)+1,
        first_name=data["first_name"],
        last_name=data["last_name"],
        gender=data["gender"],
        age=data["age"],
        email=data["email"],
        phone=data["phone"],
        city=data["city"],
        address=data["address"]
        )
    persons.append(new_person)
    save_db(persons)
    return new_person


@app.put("/api/persons/{person_id}", response_model=PersonOutput)
def edit_person(person_id: int, data = Body()):
    matches = [person for person in persons if person.id == person_id]
    if matches:
        person = matches[0]
        person.first_name = data["first_name"]
        person.last_name = data["last_name"]
        person.gender = data["gender"]
        person.age = data["age"]
        person.email = data["email"]
        person.phone = data["phone"]
        person.city = data["city"]
        person.address = data["address"]
        save_db(persons)
        return person
    else:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Person not found"}
                )


@app.delete("/api/persons/{person_id}", status_code=204)
def delete_person(person_id: int):
    matches = [person for person in persons if person.id == person_id]
    if matches:
        person = matches[0]
        persons.remove(person)
        save_db(persons)
    else:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Person not found"}
                )
