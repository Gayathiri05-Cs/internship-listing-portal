# InternConnect – Internship Listing Portal (Week 3)

A beginner-friendly full-stack internship listing and application portal built with HTML, CSS, JavaScript, Python Flask and SQLite.

## Features
- Internship cards with company, location, duration, work mode and stipend.
- Search by title, company, domain and location.
- Filters for domain, work mode, duration and maximum stipend.
- Internship details page and Apply Now flow.
- Application form with browser and backend validation.
- SQLite storage for internships and applications.
- Duplicate application prevention for the same internship and email.
- Responsive layout for desktop, tablet and mobile.
- JSON REST API endpoints and a health-check endpoint.

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows (PowerShell)
1. Extract the ZIP file.
2. Open the `Internship_Listing_Portal_Week3` folder in VS Code.
3. Open Terminal in VS Code and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks virtual-environment activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

4. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically at `database/internships.db` and sample internship records are inserted on first run.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/internships` | List internships; supports search and filters |
| GET | `/api/internships/<id>` | View one internship |
| POST | `/api/applications` | Submit an application |
| GET | `/api/applications` | View saved applications (development/testing only) |
| GET | `/health` | Check server status |

### Example application JSON
```json
{
  "internship_id": 1,
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "phone": "9876543210",
  "resume_link": "https://example.com/resume.pdf",
  "cover_note": "I am interested in this opportunity."
}
```

## Test the project
Run:
```powershell
python -m unittest discover -s tests -v
```
Or follow `test_cases.md` manually in the browser.

## Project structure
```text
Internship_Listing_Portal_Week3/
├── app.py
├── database.py
├── validators.py
├── requirements.txt
├── README.md
├── test_cases.md
├── templates/
│   ├── index.html
│   ├── detail.html
│   ├── apply.html
│   └── success.html
├── static/
│   ├── style.css
│   ├── script.js
│   ├── detail.js
│   └── apply.js
├── database/
│   └── .gitkeep
└── tests/
    └── test_app.py
```

## Notes
- The included internship data is sample/demo data.
- Resume can be supplied as a URL or uploaded as a PDF, DOC or DOCX file (maximum 5 MB). Uploaded files are saved in the local `uploads/` folder.
- The applications listing endpoint is intended only for local development and testing. Add authentication and authorization before deploying publicly.
