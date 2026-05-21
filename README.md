# Feedback Survey

A multi-step HTML feedback form backed by a Django API. Submissions are stored in SQLite and viewable in the Django admin.

## Structure

```
survey_backend/
├── backend/            # Django project settings + root URLconf
├── survey/             # Django app: model, views, admin, API routes
├── survey_form.html    # Frontend (multi-step form, star rating, validation)
├── manage.py
├── requirements.txt
└── venv/               # virtual environment (not committed)
```

## Setup

```powershell
cd survey_backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # for /admin/
python manage.py runserver
```

If PowerShell blocks activation, run once:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## URLs

| Path             | Purpose                                |
|------------------|----------------------------------------|
| `/`              | Renders the survey form                |
| `/api/submit/`   | POST JSON to save a response           |
| `/api/stats/`    | GET total responses + average rating   |
| `/admin/`        | Django admin — browse/edit responses   |

## API example

```bash
curl -X POST http://127.0.0.1:8000/api/submit/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","satisfaction":5,"likes":["Design"]}'
```
