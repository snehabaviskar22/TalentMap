# TalentMap – Employee Skill Gap Analysis & Training Recommendation System

A full-stack HR management web application developed using **Django**, **MongoDB Atlas**, and **Django REST Framework**. TalentMap enables HR administrators to manage employees, roles, and training courses while automatically identifying employee skill gaps and recommending relevant training programs based on role requirements.

---

# Live Demo

**Link:** https://talentmap-vtnx.onrender.com

---

# Objectives

The main objectives of this project are:

* Automate employee skill gap analysis.
* Help HR identify missing skills for each employee.
* Recommend relevant training courses based on missing skills.
* Centralize employee, role, and course management.
* Demonstrate Python programming concepts, Django development, MongoDB integration, and REST API development.

---

# Features

## HR Module

* HR Login & Logout
* Secure Authentication using Django Authentication System
* Dashboard with workforce statistics
* Manage Employees (Add, Edit, Delete, View)
* Manage Roles (Add, Edit, Delete)
* Manage Training Courses (Add, Edit, Delete)
* Search and Filter Employees
* Responsive Dashboard
* Cloud Deployment using Render

---

## Skill Gap Analysis

The system automatically compares employee skills with the required skills for their assigned role.

* Identifies missing skills
* Generates Skill Gap Reports
* Displays matched and missing skills
* Uses Python Set Operations for comparison

---

## Training Recommendation System

Based on the identified skill gaps, the system automatically recommends relevant training courses.

* Course recommendations based on missing skills
* Multiple recommendations for multiple missing skills
* Dynamic course management through MongoDB

---

# Technology Stack

## Backend

* Python 3
* Django 4
* Django REST Framework (DRF)

## Database

* MongoDB Atlas
* PyMongo
* SQLite (Authentication, Admin & Sessions)

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Font Awesome

## Deployment

* Render
* MongoDB Atlas
* GitHub

---

# Python Concepts Demonstrated

* Object-Oriented Programming (OOP)
* Sets
* Dictionaries
* List Comprehensions
* Regular Expressions (Regex)
* Exception Handling
* Threading
* Modular Programming

---

# Project Structure

```text
TalentMap/
│
├── hr/
├── talentmap/
├── templates/
├── static/
├── staticfiles/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Database Design

## MongoDB Collections

* Employees
* Roles
* Courses

## SQLite Tables

* Django Users
* Authentication
* Sessions
* Admin Data

## Relationships

* One Role → Multiple Employees
* One Course → One Skill
* One Employee → One Assigned Role
* One Role → Multiple Required Skills

---

# Authentication

* Django Authentication System
* Session-Based Authentication
* HR Login
* Protected Routes using `@login_required`
* Django Admin Support

---

# REST API Endpoints

## Employees

* GET `/api/employees/`
* GET `/api/employees/<id>/`
* POST `/api/employees/`
* PUT `/api/employees/<id>/`
* DELETE `/api/employees/<id>/`

## Roles

* GET `/api/roles/`
* POST `/api/roles/`
* PUT `/api/roles/<id>/`
* DELETE `/api/roles/<id>/`

## Courses

* GET `/api/courses/`
* POST `/api/courses/`
* PUT `/api/courses/<id>/`
* DELETE `/api/courses/<id>/`

---

# Setup Instructions

## Prerequisites

* Python 3.10+
* MongoDB Atlas (or MongoDB Community Server)
* Git

---

## Clone Repository

```bash
git clone https://github.com/snehabaviskar22/TalentMap.git
```

```bash
cd TalentMap
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file (or configure these variables on Render):

```env
DJANGO_SECRET_KEY=your_secret_key

DJANGO_DEBUG=True

MONGO_URI=your_mongodb_connection_string

MONGO_DB_NAME=TalentMap
```

---

## Database Setup

Apply Django migrations

```bash
python manage.py migrate
```

Create an HR administrator account

```bash
python manage.py createsuperuser
```

---

## Run the Project

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

Login using the HR administrator credentials created through `createsuperuser`.

---

# Screenshots

## Login Page

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/810d2146-ba5e-454e-9d0e-5f570d63cffe" />


---

## Dashboard

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9749b7b4-3db8-4658-a1fc-21a103151837" />


---

## Employee Management

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e3cf776d-03c6-4efd-9cf4-34cd96c3916d" />


---

## Role Management

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8c4bcea8-0025-4e4f-8ca2-c1b5fb1ef3dc" />


---

## Course Management

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/892f6d1d-da76-4653-80e4-944f49eeafff" />


---

## Skill Gap Report

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4d1e0671-517f-491e-9de6-ce3f5bc8046c" />


---

## Training Recommendations

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2e0fce6d-2ae3-499c-abac-9d00d84275c7" />


---

# Future Enhancements

* AI-Based Training Recommendations
* Resume Skill Extraction
* Employee Performance Analytics
* PDF Report Generation
* Email Notifications

---

# Author

**Sneha Baviskar**

MCA Student

Savitribai Phule Pune University

---

# License

This project is developed for academic and educational purposes.
