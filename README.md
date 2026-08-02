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

*(Add Screenshot)*

---

## Dashboard

*(Add Screenshot)*

---

## Employee Management

*(Add Screenshot)*

---

## Role Management

*(Add Screenshot)*

---

## Course Management

*(Add Screenshot)*

---

## Skill Gap Report

*(Add Screenshot)*

---

## Training Recommendations

*(Add Screenshot)*

---

# Future Enhancements

* AI-Based Training Recommendations
* Resume Skill Extraction
* Employee Performance Analytics
* Interactive Dashboard Charts
* PDF Report Generation
* JWT Authentication
* Docker Deployment
* Email Notifications

---

# Author

**Sneha Baviskar**

MCA Student

Savitribai Phule Pune University

---

# License

This project is developed for academic and educational purposes.
