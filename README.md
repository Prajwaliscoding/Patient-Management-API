# 🏥 Patient Management System API

This is a FastAPI-based project for managing patient records including details like name, age, gender, height, weight, and city. It supports full CRUD operations and also includes BMI computation and patient verdicts.

## 🚀 Features

- Create, Read, Update, and Delete (CRUD) patient records
- Automatically calculates BMI and health verdict
- View all patients or sort by height or weight
- Simple JSON file-based storage (no external database required)

## 📦 Technologies Used

- FastAPI - Web framework
- Pydantic - Data validation and modeling
- JSON - Local file for persistent storage

## Project Structure

``` markdown
Patient-Management-API
├── main.py                             # FastAPI application
├── patients_data.json                  # Local database (must exist)
├── requirements.txt                    # Python dependencies
└── README.md                           # Project description
```

## Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Prajwaliscoding/Patient-Management-API.git
cd Patient-Management-API
```

### 2️⃣ (Optional) Create & Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # On macOS/Linux
# OR
venv\Scripts\activate        # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
uvicorn main:app --reload
```
### Now visit: http://127.0.0.1:8000/docs 

## 📚 API Endpoints

```markdown

|   Method   |     Endpoint                            |        Description                 |
|------------|-----------------------------------------|------------------------------------|
| GET        | /                                       | Home route                         |
| GET        | /about                                  | About the API                      |
| GET        | /view                                   | View all patients                  |
| GET        | /patient/{patient_id}                   | Get patient details                |
| GET        | /sort_patient?sort_by=height&order=asc  | Sort patients                      |
| POST       | /create                                 | Add a new patient                  |
| PUT        | /update/{patient_id}                    | Update an existing patient         |
| DELETE     | /delete/{patient_id}                    | Delete a patient                   |

```

## 🧮 Computed Fields
Each patient automatically has:

- BMI (computed_bmi)
- Health verdict (computed_verdict)

## 🧾 Sample Patient JSON
```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "Dallas",
  "age": 29,
  "gender": "male",
  "height": 1.75,
  "weight": 70.5
}
```







