# Project Report: Feedback Survey

## 1. What is this project?

This is a small web app that asks users for feedback. The user fills a form
with 3 steps. Then the app saves the answers in a database. The owner can
log in and see all the answers later.

The project has two main parts:

- **A web page** that shows the form to the user.
- **A server** that takes the answers and saves them.

## 2. What does it do?

The user can:

1. Open the form in a web browser.
2. Type their name and email.
3. Pick their age group.
4. Give a star rating from 1 to 5.
5. Choose what they liked (design, speed, features, etc.).
6. Write extra comments.
7. Click **Submit**.

After they click Submit, the app shows a "Thank you" message. The answer is
saved in a database file on the server.

The owner of the app can:

- Open a special admin page.
- Log in with a username and password.
- See a list of all the answers.
- Search, filter, and edit answers.
- See simple stats like the total number of answers and the average rating.

## 3. What did I build?

I built three things:

### a) The form (frontend)

A single HTML file called `survey_form.html`. It uses:

- **HTML** to make the structure (boxes, labels, buttons).
- **CSS** to make it look nice (colors, spacing, rounded corners).
- **JavaScript** to make it work step by step. JavaScript also checks if
  the user filled the fields correctly before sending.

The form has 3 steps and a progress bar at the top. The user goes step by
step. If they make a mistake (like an empty name), the form shows a red
error message under that field.

### b) The server (backend)

A Django project. Django is a Python tool for making web servers. The
server does these jobs:

- Show the form when someone visits the main page.
- Take the answers when the user clicks Submit.
- Check the answers are valid (name not empty, email looks like an email,
  rating is between 1 and 5).
- Save the answers in a database.
- Show stats when asked.
- Give the owner an admin page to look at the data.

### c) The database

I used **SQLite**. SQLite is a small database that lives in one file
(`db.sqlite3`). I did not need to set up a big database server. Django
made the database file for me.

The database has one table called `SurveyResponse`. Each row has:

- name
- email
- age group
- satisfaction (1 to 5)
- likes (a list)
- comments
- contact_me (yes or no)
- submitted_at (the time the answer came in)

## 4. Tools and technologies

| Tool | Why I used it |
|------|---------------|
| HTML | To make the form on the page |
| CSS | To make the form look nice |
| JavaScript | To check the form and send data to the server |
| Python 3.14 | The language for the server |
| Django 5.2 | The framework that runs the server |
| SQLite | To save the answers |
| Git | To save versions of my code |
| GitHub | To share the code online |

## 5. Project folder structure

The whole project is in one folder called `survey_backend`. Inside, the
important parts are:

```
survey_backend/
├── README.md              -> Short notes for other people
├── REPORT.md              -> This report
├── .gitignore             -> List of files Git should ignore
├── requirements.txt       -> List of Python tools needed
├── manage.py              -> Django's main command file
├── db.sqlite3             -> The database file (not on GitHub)
├── survey_form.html       -> The frontend (form)
│
├── backend/               -> Django project settings
│   ├── settings.py        -> Main settings
│   ├── urls.py            -> Main URL list
│   └── ...
│
├── survey/                -> The "survey" app (the main logic)
│   ├── models.py          -> What a survey answer looks like (DB table)
│   ├── views.py           -> Code that handles requests
│   ├── urls.py            -> URLs for the survey
│   ├── admin.py           -> Settings for the admin page
│   └── migrations/        -> Database setup files
│
└── venv/                  -> Virtual environment (not on GitHub)
```

## 6. How it all works together

Here is the flow when a user fills the form:

1. The user opens **http://127.0.0.1:8000/** in a browser.
2. Django reads `survey_form.html` and sends it to the browser.
3. The user fills the form step by step.
4. The user clicks **Submit**.
5. JavaScript sends the answers as JSON to `/api/submit/`.
6. Django checks the data.
7. If the data is good, Django saves it to the database.
8. Django sends back "Thanks for your feedback!"
9. JavaScript shows the success screen to the user.

If the data is bad (for example, no name), Django sends back an error.
JavaScript shows the error to the user.

## 7. The API (server endpoints)

The server has 4 URLs (also called endpoints):

| URL | What it does |
|-----|--------------|
| `/` | Shows the form |
| `/api/submit/` | Takes a new survey answer (POST request) |
| `/api/stats/` | Returns total answers and average rating (GET) |
| `/admin/` | The Django admin page for the owner |

An "endpoint" is just an address where the server listens. The server does
something different at each address.

## 8. How to run the project

These are the steps to run the project on a new computer:

```powershell
# 1. Go into the project folder
cd survey_backend

# 2. Make a virtual environment (a clean Python space)
py -m venv venv

# 3. Turn on the virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install Django
pip install -r requirements.txt

# 5. Set up the database
python manage.py migrate

# 6. Make an admin user
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in a browser.

## 9. Problems I had and how I fixed them

### Problem 1: Django 4.2 did not work with Python 3.14

When I first tried the admin page, I got an error:
`'super' object has no attribute 'dicts'`. This happened because Django
4.2 was made before Python 3.14 came out. Some Python rules changed.

**Fix:** I updated Django to version 5.2. Version 5.2 works with Python
3.14.

### Problem 2: The home folder was already a Git repo

The folder `C:\Users\HABAYIMANA Vincent` is itself a Git repo for another
project. So my project was inside another repo.

**Fix:** I ran `git init` inside the `survey_backend` folder. This made it
its own repo. The parent repo just sees `survey_backend` as an untracked
folder, so the two repos do not mix.

### Problem 3: CORS (web security)

If the user opens the HTML file from their hard drive (not through the
server), the browser blocks the form from sending data to the server. This
is a security rule called CORS.

**Fix:** I added special headers in the server code to allow this. The
form works both ways: opened from a file, or served by Django.

## 10. What is on GitHub

The code is at: **https://github.com/Vincent-HABAYIMANA/feedback-survey**

What I pushed:

- All Python code
- The HTML form
- The README and this report
- A list of needed tools (`requirements.txt`)

What I did NOT push (and why):

- `venv/` — too big, anyone can make a new one with `pip install`.
- `db.sqlite3` — has test data, each person should make their own.

## 11. What I could add next

The project works, but it could be better. Ideas for the future:

- **Email notifications.** Send an email to the admin when a new answer
  arrives.
- **Charts.** Show the ratings in a bar chart on a stats page.
- **Export.** A button to download all answers as a CSV file.
- **Login for users.** So people cannot send fake answers many times.
- **Better security.** Turn off `DEBUG` mode and use a strong secret key
  for real use on the internet.
- **Deploy online.** Put the app on a service like Render, Railway, or
  PythonAnywhere so anyone can use it.

## 12. Summary

In this project I built a full small web app from start to finish. The
user side is a clean form with steps and stars. The server side is a
Django app that saves answers and shows them in an admin page. The whole
thing is in one folder. It uses a virtual environment so it stays clean.
The code is on GitHub.

I learned how to:

- Make a multi-step form with HTML, CSS, and JavaScript.
- Make a Django project with an app, a model, and views.
- Save data in a database with Django.
- Use the Django admin page.
- Use a virtual environment.
- Use Git and GitHub.
- Fix version problems between Python and Django.
