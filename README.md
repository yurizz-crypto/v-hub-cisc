# CISC Virtual Hub (V-Hub)

**College of Information Sciences and Computing Virtual Hub System**  
ITSD81 Desktop Application Development Project  
Information Technology Department  
Central Mindanao University  
1st Semester, S.Y. 2025 - 2026

## Introduction

The College of Information Sciences and Computing (CISC) lacks a centralized student information and communication platform. Students and faculty often rely on social media for updates, leading to inconsistent information and distractions. The CISC Virtual Hub (V-Hub) is designed to provide a comprehensive digital hub for students and faculty, enhancing connectivity and interactivity within the college.

V-Hub aims to centralize academic schedules, organization events, house activities, and communication, supporting student progress tracking, bulletin publishing, project showcasing, and more. This project is developed by ITSD81 students as a semester-long laboratory project.

## Objectives

- Establish a centralized student information platform for CISC faculty and students.
- Facilitate collaborative, modular desktop application development.
- Enable faculty to distribute classroom content and monitor academic records internally.
- Centralize academic schedules, events, and activities for improved coordination.
- Streamline student progress tracking, communication, and bulletin publishing.
- Support project showcasing and capstone management within the college.

## System Overview

CISC V-Hub is a desktop application acting as an academic organizer, communication center, and gamification hub for CISC. It is intended for students, faculty, and staff, with future versions planned for mobile and web platforms.

## Architecture

- **Backend (`backend/`)**:  
	Built with Django, the backend provides RESTful APIs, business logic, and data management. It includes modular apps for each feature (Academics, Announcements, Appointments, etc.), a config configuration, shared utilities, middleware, and API permissions.
- **Frontend (`frontend/`)**:  
	Developed using PyQt6, the desktop frontend interacts with the backend via APIs and provides a rich user interface. Qt Designer is used for GUI layouts.
- **Database**:  
	PostgreSQL is the main production database for scalability and robustness. SQLite3 is used for local development and testing.
- **Virtual Environment (`venv/`)**:  
	All dependencies are managed in a Python virtual environment for consistency and isolation.

### Key Backend Folders

- `apps/`: Modular Django apps for each system feature.
- `config/`: Project configuration, settings, URL routing, and server entry points (`asgi.py`, `wsgi.py`).
- `common/`: Shared constants, exceptions, services, and utilities.
- `middleware/`: Custom middleware for request/response processing (e.g., logging, authentication).
- `tests/`: Project-wide and app-specific tests.
- `manage.py`: Django’s command-line utility for running the server, migrations, and other tasks.

## System Modules

Below are the modules included in the CISC Virtual Hub. Modules are grouped according to their business logic to help organize the system and make it easier to understand for all contributors.
- Academics
  - Faculty-Classroom System (Internal LMS)
  - Academic Progress Tracker
  - Academic Schedule & Organizer
- Announcements
  - Announcement Board & News Feed
- Appointments
  - Faculty Appointment & Consultation Scheduler
- Calendar
  - CISC Calendar System
- Dashboard
  - Admin Insights Dashboard
- Documents
  - Document Vault & Form Repository
- Feedback
  - Suggestion, Complaint, & Feedback Box
- House
  - House Management & Points System
- Links
  - Student Services & External Link Directory
- Messaging
  - Internal Messaging & Inquiry Center
- Organizations
  - Student Organization Directory & Membership
  - Organization Event Lifecycle & Attendance
- Showcase
  - Project & Competition Showcase
- Users
  - User Profile & Resume

## Tools and Technologies

- **Python 3.11.9**: Main programming language for backend and desktop frontend.
- **Django 5.2.5**: Backend framework for APIs and logic.
- **Django REST Framework 3.16.1**: For building RESTful APIs.
- **PyQt6 6.9.1**: Desktop GUI framework.
- **PyQt6-Qt6 6.9.1**: Qt6 bindings for PyQt6.
- **PyQt6_sip 13.10.2**: SIP bindings for PyQt6.
- **psycopg2-binary 2.9.10**: PostgreSQL database adapter for Python.
- **requests 2.32.5**: HTTP library for API communication.
- **Qt Designer**: For designing GUI layouts.
- **PostgreSQL**: Main production database.
- **SQLite3**: Local development database.
- **Other Libraries**: Matplotlib (visualization), python virtual environment etc.

## Contributors
**Backend**
- Pulmones, Jan Marc
- Endino, Michaela RJ Kate
- Campomanes, Ethan
- Montecillo, Jopur Jay
- Ruaya, Jairuz
- Bongo, Seth Laurence
- Velasco, Kurt Vincent
- Cervantes, Aaron Clyde
- Magdaraog, Emanuel
- Cuarteros, Dionne James
- Sanchez, Jan Eduard
- Lauretto, Christian Edward
- Gonzaga, Krismar
- Balindong, Salman
- Brigoli, Boon Jefferson

**Frontend**
- Importante, Mark
- Velasco, Shauntie
- Villarino, Victory Kyle
- Gulmatico, John Renz
- Salise, Yuri
- Araneta, Gabriel
- Montecillo, Dale Zurich
- Bontuyan, Earlryd
- Dulay, Andre Louie
- Manangkila, Khent
- Nacua, Sebastian
- Jumao-as, Sertin Jay
- Cutillar, Rod Andro

**Design**
- Castro, Carlos
- Jugos, King Jan Paul
- Jacobe, Roshan
- Sosobrado, Marc Christian
- Salapang, Earl
- Oinal, Babylyn
- Belandres, Jogn Harley
- Pinatacan, John Rio
- Gonzales, Kian Mark

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:  
	 `pip install -r requirements.txt`
4. Run migrations:  
	 `python backend/manage.py migrate`
5. Start the server:  
	 `python backend/manage.py runserver`

