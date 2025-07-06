from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the Patient", examples=['P001', 'P003'])]
    name: Annotated[str, Field(..., description="Name of the Patient", examples=['John Doe'])]
    city: Annotated[str, Field(..., description="City where the Patient lives")]
    age: Annotated[int, Field(..., gt =0 , lt = 120, description="Age of the Patient")]
    gender: Annotated[Literal['male','female','other'], Field(..., description="Gender of the patient")] 
    height: Annotated[float, Field(..., gt=0, description="Height of the Patient", examples=['1.72', '1.65'])]
    weight: Annotated[float, Field(..., gt=0,  description="Weight of the Patient", examples=['72.3', '65'])]


    @computed_field
    @property
    def computed_bmi(self) -> float:                            
        bmi = round(self.weight / (self.height**2),2)           
        return bmi
    
    @computed_field
    @property
    def computed_verdict(self) -> str:
        if self.computed_bmi < 18.5:
            return "Underweight"
        elif self.computed_bmi < 25:
            return "Normal"
        elif self.computed_bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default = None)]
    city: Annotated[Optional[str], Field(default = None)]
    age: Annotated[Optional[int], Field(default = None, gt=0)]
    gender: Annotated[Optional[Literal['male','female','other']], Field(default = None)]
    height: Annotated[Optional[float], Field(default = None,gt=0)]
    weight: Annotated[Optional[float], Field(default = None,gt=0)]

app = FastAPI()

def patients_data():
    with open("patients_data.json", "r") as p:       
        data = json.load(p)
    return data

def save_data(data):                                 
    with open("patients_data.json", "w") as p:
        json.dump(data, p)


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
def patient_id(patient_id : str = Path(..., description = "ID of the patient.", examples = ["P001"])):

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


@app.post("/create")
def create_patient(patient : Patient):  

    data = patients_data()

    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude = {'id'})   

    save_data(data)  
    return JSONResponse(status_code=201, content={'message':'Patient created successfully.'})    


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_info_to_update: PatientUpdate):   
    data = patients_data()                                         
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    patient_info_before_update = data[patient_id]       
    

    patient_info_for_update = patient_info_to_update.model_dump(exclude_unset = True)           
    for i,j in patient_info_for_update.items():   
        patient_info_before_update[i]=j           
    

    patient_info_json = Patient(**patient_info_before_update)  
 
    patient_info_dict = patient_info_json.model_dump(exclude={'id'})  

    data[patient_id] = patient_info_dict       
    return JSONResponse(status_code=200 , content={'message':"Updated successfully."})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str = Path(example='P002')):
    data = patients_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Deleted the Patient Successfully'})
