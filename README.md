# TalentMap

## Employee Skill Gap Analysis & Training Recommendation System

TalentMap is a web-based HR application developed using **Django** and **MongoDB** to help organizations identify employee skill gaps and recommend relevant training courses. The system compares an employee's existing skills with the required skills for their role and generates a detailed skill gap analysis along with personalized course recommendations.

This project was developed as part of the **Master of Computer Applications (MCA)** curriculum to demonstrate the application of Python programming concepts, Django web development, MongoDB integration, and REST API development.

---

## Features

- HR Authentication (Login/Logout)
- Dashboard with workforce overview
- Employee Management (Add, Edit, Delete, View)
- Role Management
- Course Management
- Skill Gap Analysis
- Course Recommendation System
- Search and Filter Employees
- MongoDB CRUD Operations
- Django REST Framework (DRF) API support

---

## Technologies Used

### Backend
- Python 3
- Django
- Django REST Framework (DRF)

### Database
- MongoDB
- PyMongo

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Font Awesome

### Python Concepts Demonstrated
- Object-Oriented Programming (OOP)
- Sets
- Dictionaries
- List Comprehensions
- Regular Expressions (Regex)
- Exception Handling
- Threading
- Modular Programming

---

## Project Structure

```text
TalentMap/
│── manage.py
│── requirements.txt
│── README.md
│── .gitignore
│
├── talentmap/
├── hr/
├── api/
├── templates/
└── static/
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/TalentMap.git
```

### 2. Navigate to the Project

```bash
cd TalentMap
```

### 3. Create a Virtual Environment

Windows

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## Database Setup

This project uses:

- MongoDB (Employee, Role and Course data)
- SQLite (Django Authentication and Sessions)

### Apply Django Migrations

```bash
python manage.py migrate
```

### Create HR Login

```bash
python manage.py createsuperuser
```

Follow the prompts to create your username and password.

---

## Running the Project

Start the Django development server.

```bash
python manage.py runserver
```

Open your browser and visit

```
http://127.0.0.1:8000/
```

Login using the HR credentials created with `createsuperuser`.

---

## Core Modules

- Employee Management
- Role Management
- Course Management
- Skill Gap Analysis
- Course Recommendation Engine
- HR Dashboard
- REST API

---

## Python Concepts Used

### Unit 1
- Sets for skill comparison
- Dictionaries for role-skill mapping
- List Comprehensions

### Unit 2
- Custom Modules
- Exception Handling

### Unit 3
- Object-Oriented Programming
- Regular Expressions
- Threading

### Unit 4
- MongoDB CRUD Operations

### Unit 5
- Django Web Framework
- Django REST Framework (DRF)

---

## Future Enhancements

- AI-based training recommendations
- Resume skill extraction
- Email notifications
- Employee performance analytics
- Charts and dashboard analytics
- PDF report generation
- JWT Authentication
- Docker deployment

---

## Author

**Sneha Baviskar**

Master of Computer Applications (MCA)

---

## License

This project is developed for educational and learning purposes.
