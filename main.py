from fastapi import FastAPI
import json

app = FastAPI()

def patients_data():
    with open("patients_data.json", "r") as p:
        data = json.load(p)
    return data

@app.get("/")
def main():
    return {"message" : "Patient Management System API"}

@app.get("/about")
def about():
    return {"message" : "This is a fully functional API to manage the doctors' patient records."}

@app.get("/view")
def view():
    data = patients_data()
    return data
