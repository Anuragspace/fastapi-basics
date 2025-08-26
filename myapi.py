from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

students = {
    1:{
        "name":"anurag adarsh",
        "age" : 20,
        "year" : "year 26"
    },
    2:{
        "name":"mohit",
        "age" : 22,
        "year" : "year 26"
    }
}

class Student(BaseModel):
    name:str
    age:int
    year:str

class UpdateStudent(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    year: Optional[str]=None


@app.get("/")
def index():
    return {"name":"First Data"}

#path parameter
@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(..., description="The ID of the student you want to view" , gt=0, lt=4)
):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

#query paarmeter
@app.get("/get-by-name")
def get_student_by_name(*, name: Optional[str]=None, test : int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data" : "Not found"}


#combining path and query parameter
@app.get("/get-by-name/{student_id}")
def get_student_by_name_combine(*,student_id:int, name: Optional[str]=None, test : int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data" : "Not found"}

#post method
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if  student_id in students:
        return{"Error" : "Student exists"}

    students[student_id] = student.dict()
    return students[student_id] 

#put - update value
@app.put("/update-student/{student_id}")
def update_student(student_id: int,student: UpdateStudent):
    if student_id not in students:
        return {"Error" : "Students does not exits"}
    
    if student.name is not None:
        students[student_id]['name'] = student.name

    if student.age is not None:
        students[student_id]['age'] = student.age

    if student.year is not None:
        students[student_id]['year'] = student.year
    return students[student_id]

#delete
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"Error": "Student does not exists"}
    del students[student_id]
    return {"Message" : "Student deleted successfully"} 