# Planner App

A simple Django web app to keep your tasks and plans organized.


This project started as a simple idea: to organize tasks and plans in one place.  
What began as a learning exercise grew into a personal journey of patience, focus, and growth.  

Built with **Django**, it helps manage categories, plans, and tasks—all while learning the joys and frustrations of coding.  

Every feature in this app reminds me that even small steps lead to progress, in projects and in life.


## Features

- Add categories, plans, and tasks
- Mark tasks as done
- Delete tasks, plans, or categories
- Dashboard to see everything at a glance

## Tech

- Django 6.0, Python 3.12
- SQLite database
- HTML + Bootstrap 5

## Quick Start

```bash
git clone https://github.com/sunitachaulagain/planner-app.git
cd planner-app
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your browser and start planning your day!
