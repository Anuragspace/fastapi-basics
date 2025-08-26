# 🚀 FastAPI Student Management System

A comprehensive guide to building REST APIs with FastAPI, demonstrated through a simple Student Management System. This project covers everything from basic setup to advanced features.

## 📋 Table of Contents

- [🌟 What is FastAPI?](#-what-is-fastapi)
- [🛠️ Setup & Installation](#️-setup--installation)
- [🏗️ Project Structure](#️-project-structure)
- [🔧 Basic Concepts](#-basic-concepts)
- [📡 API Endpoints](#-api-endpoints)
- [🎯 Parameter Types](#-parameter-types)
- [📝 Request/Response Models](#-requestresponse-models)
- [🧪 Testing Your API](#-testing-your-api)
- [❓ Common Use Cases & FAQ](#-common-use-cases--faq)
- [📚 Additional Resources](#-additional-resources)

## 🌟 What is FastAPI?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It's designed to be:

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase development speed by 200% to 300%
- **Fewer bugs**: Reduce human-induced errors by 40%
- **Intuitive**: Great editor support with auto-completion
- **Easy**: Designed to be easy to use and learn
- **Standards-based**: Based on OpenAPI and JSON Schema

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv fastapi-env

# Activate virtual environment
# On Windows:
fastapi-env\Scripts\activate
# On macOS/Linux:
source fastapi-env/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn[standard]

# Or install from requirements.txt
pip install -r requirements.txt
```

### Step 3: Create requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
```

### Step 4: Run the Application

```bash
# Run with auto-reload for development
uvicorn main:app --reload

# Run on specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Your API will be available at:
- **API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

## 🏗️ Project Structure

```
fastapi-student-management/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── models/                # Data models (optional)
│   └── student.py
├── routes/                # Route handlers (optional)
│   └── students.py
└── tests/                 # Test files (optional)
    └── test_main.py
```

## 🔧 Basic Concepts

### 1. FastAPI App Instance

```python
from fastapi import FastAPI

app = FastAPI(
    title="Student Management API",
    description="A simple API for managing students",
    version="1.0.0"
)
```

### 2. HTTP Methods

FastAPI supports all standard HTTP methods:

```python
@app.get("/")          # GET request
@app.post("/")         # POST request
@app.put("/")          # PUT request
@app.delete("/")       # DELETE request
@app.patch("/")        # PATCH request
@app.options("/")      # OPTIONS request
@app.head("/")         # HEAD request
```

### 3. Data Models with Pydantic

```python
from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None
```

## 📡 API Endpoints

### 🏠 Root Endpoint

**GET /** - Welcome message

```python
@app.get("/")
def index():
    return {"name": "First Data"}
```

**Example Response:**
```json
{
  "name": "First Data"
}
```

### 👤 Get Student by ID

**GET /get-student/{student_id}** - Retrieve a specific student

```python
@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=4)
):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]
```

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/get-student/1"
```

**Example Response:**
```json
{
  "name": "anurag adarsh",
  "age": 20,
  "year": "year 26"
}
```

### 🔍 Get Student by Name

**GET /get-by-name** - Search student by name

```python
@app.get("/get-by-name")
def get_student_by_name(*, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}
```

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/get-by-name?name=anurag%20adarsh&test=1"
```

### 🔄 Combined Path and Query Parameters

**GET /get-by-name/{student_id}** - Get student with both path and query params

```python
@app.get("/get-by-name/{student_id}")
def get_student_by_name_combine(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}
```

### ➕ Create New Student

**POST /create-student/{student_id}** - Add a new student

```python
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student.dict()
    return students[student_id]
```

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/create-student/3" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john doe",
    "age": 21,
    "year": "year 27"
  }'
```

### ✏️ Update Student

**PUT /update-student/{student_id}** - Update existing student

```python
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name is not None:
        students[student_id]['name'] = student.name
    if student.age is not None:
        students[student_id]['age'] = student.age
    if student.year is not None:
        students[student_id]['year'] = student.year
    
    return students[student_id]
```

**Example Request:**
```bash
curl -X PUT "http://127.0.0.1:8000/update-student/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "anurag adarsh updated",
    "age": 21
  }'
```

### 🗑️ Delete Student

**DELETE /delete-student/{student_id}** - Remove a student

```python
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}
```

**Example Request:**
```bash
curl -X DELETE "http://127.0.0.1:8000/delete-student/1"
```

## 🎯 Parameter Types

### 1. Path Parameters

Used to capture values from the URL path:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return students.get(student_id)
```

### 2. Query Parameters

Used to capture values from URL query string:

```python
@app.get("/students/")
def get_students(skip: int = 0, limit: int = 10):
    return list(students.values())[skip:skip + limit]
```

### 3. Request Body

Used to receive data in request body:

```python
@app.post("/students/")
def create_student(student: Student):
    # Process student data
    return student
```

### 4. Path Parameter Validation

Add validation constraints to path parameters:

```python
from fastapi import Path

@app.get("/students/{student_id}")
def get_student(
    student_id: int = Path(
        ..., 
        title="Student ID",
        description="The ID of the student to retrieve",
        gt=0,  # Greater than 0
        le=1000  # Less than or equal to 1000
    )
):
    return students.get(student_id)
```

### 5. Query Parameter Validation

Add validation to query parameters:

```python
from fastapi import Query

@app.get("/students/")
def get_students(
    q: Optional[str] = Query(
        None, 
        min_length=3, 
        max_length=50,
        regex="^[a-zA-Z\s]+$"
    )
):
    # Search students by query
    pass
```

## 📝 Request/Response Models

### Advanced Pydantic Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class YearEnum(str, Enum):
    FIRST = "year 1"
    SECOND = "year 2"
    THIRD = "year 3"
    FOURTH = "year 4"

class Student(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., gt=0, le=150)
    year: YearEnum
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 20,
                "year": "year 2",
                "email": "john.doe@example.com"
            }
        }

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    year: str
    created_at: datetime
    
class StudentsListResponse(BaseModel):
    students: List[StudentResponse]
    total: int
    page: int
    per_page: int
```

## 🧪 Testing Your API

### 1. Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### 2. Using curl

```bash
# Test GET endpoint
curl -X GET "http://127.0.0.1:8000/get-student/1"

# Test POST endpoint
curl -X POST "http://127.0.0.1:8000/create-student/3" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 22, "year": "year 3"}'

# Test PUT endpoint
curl -X PUT "http://127.0.0.1:8000/update-student/1" \
  -H "Content-Type: application/json" \
  -d '{"age": 21}'

# Test DELETE endpoint
curl -X DELETE "http://127.0.0.1:8000/delete-student/1"
```

### 3. Python Requests

```python
import requests

# GET request
response = requests.get("http://127.0.0.1:8000/get-student/1")
print(response.json())

# POST request
student_data = {"name": "Bob", "age": 23, "year": "year 4"}
response = requests.post("http://127.0.0.1:8000/create-student/4", json=student_data)
print(response.json())
```

### 4. Unit Testing with pytest

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": "First Data"}

def test_create_student():
    response = client.post(
        "/create-student/10",
        json={"name": "Test Student", "age": 20, "year": "year 1"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"

def test_get_student():
    response = client.get("/get-student/1")
    assert response.status_code == 200
    assert "name" in response.json()
```

## ❓ Common Use Cases & FAQ

### Q: How do I handle errors and exceptions?

```python
from fastapi import HTTPException

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404, 
            detail=f"Student with id {student_id} not found"
        )
    return students[student_id]
```

### Q: How do I add CORS support?

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
```

### Q: How do I add authentication?

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Verify token logic here
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

@app.get("/protected")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "This is a protected route"}
```

### Q: How do I connect to a database?

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students/")
def get_students(db: Session = Depends(get_db)):
    # Database operations here
    pass
```

### Q: How do I add request/response logging?

```python
import logging
from fastapi import Request
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s"
    )
    return response
```

### Q: How do I handle file uploads?

```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process file contents
    return {"filename": file.filename, "size": len(contents)}
```

### Q: How do I add background tasks?

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification/")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification sent"}
```

## 🚀 Advanced Features

### 1. Dependency Injection

```python
from fastapi import Depends

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### 2. Custom Response Models

```python
from fastapi import status
from fastapi.responses import JSONResponse

@app.post("/students/", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    # Create student logic
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Student created successfully", "student": student.dict()}
    )
```

### 3. API Versioning

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/students/")
def get_students_v1():
    return {"version": "1.0", "students": list(students.values())}

@v2_router.get("/students/")
def get_students_v2():
    return {"version": "2.0", "data": {"students": list(students.values())}}

app.include_router(v1_router)
app.include_router(v2_router)
```

## 📚 Additional Resources

### 📖 Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Starlette Documentation](https://www.starlette.io/)

### 🎥 Video Tutorials
- [FastAPI Course for Beginners](https://www.youtube.com/watch?v=7t2alSnE2-I)
- [FastAPI Full Course](https://www.youtube.com/watch?v=0sOvCWFmrtA)

### 📚 Books
- "FastAPI Modern Python Web Development" by Bill Lubanovic
- "Building Python Web APIs with FastAPI" by Abdulazeez Abdulazeez Adeshina

### 🔧 Useful Tools
- **Postman**: API testing tool
- **Insomnia**: REST client
- **HTTPie**: Command-line HTTP client
- **Swagger Editor**: API design tool

### 🌟 Best Practices
1. **Use type hints** everywhere for better IDE support
2. **Organize code** into separate modules as your project grows
3. **Add comprehensive tests** for all endpoints
4. **Use environment variables** for configuration
5. **Implement proper error handling** and logging
6. **Follow REST conventions** for endpoint naming
7. **Add API documentation** with examples
8. **Use dependency injection** for common functionality
9. **Implement authentication and authorization** for production
10. **Monitor and log** API performance and errors

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Happy Coding with FastAPI!** ⭐

If you found this helpful, please give it a star! 🌟
