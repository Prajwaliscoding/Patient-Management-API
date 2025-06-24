from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/patient/{patient_id}")
def patient_id(patient_id : str = Path(..., description = "ID of the patient.", example = "P001")):

    data = patients_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404 , detail = "Patient Not Found.")

@app.get("/sort_patient")
def sort_patient(sort_by : str = Query(...,description ="Sort on the basis of height or weight"),
                 order : str = Query("asc", description = "sort in asc or desc order")):
    
    data = patients_data()

    if sort_by not in ["height", "weight"]:
        raise HTTPException(status_code = 400 , detail = "Invalid field selection. Choose height or weight.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code = 400 , detail = "Invalid field selection. Choose asc or desc.")
   
    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key = lambda x:x.get( sort_by, 0 ) , reverse = sort_order)
    
    return sorted_data