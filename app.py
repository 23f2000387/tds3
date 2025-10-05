from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

# Load CSV data once at startup
students_data = []
with open("students.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert studentId to int
        students_data.append({"studentId": int(row["studentId"]), "class": row["class"]})

@app.get("/api")
async def get_students(class_: List[str] = Query(None, alias="class")):
    """
    Returns all students. If ?class=1A&class=1B is provided, filters by classes.
    """
    if class_:
        filtered = [s for s in students_data if s["class"] in class_]
        return {"students": filtered}
    return {"students": students_data}
