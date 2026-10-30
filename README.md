# JobTrackr QA

A job application tracker built as a full testing showcase. The app tracks job applications through each stage of the hiring process. Around it, the project includes a multi-layer test automation framework covering UI, API, database, and data warehouse testing, with AI features added in later phases.

## Project Status

**Week 1 complete:** Environment setup, requirements, database schema, backend API, basic frontend, and first QA artifacts.

**Upcoming:**
- Week 2: API test automation (pytest, contract testing)
- Week 3: UI test automation (Selenium, Page Object Model)
- Week 4: Database testing and data warehouse (ETL, star schema)
- Week 5: End-to-end tests, CI/CD, Docker
- Week 6: Reporting, documentation, deployment

## Features

- User registration and login with JWT authentication
- Add, view, edit, and delete job applications (CRUD)
- Status pipeline: Applied, Screening, Interview, Offer, Rejected
- Status history tracking in the database
- Basic web interface for managing applications

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python, FastAPI, SQLAlchemy |
| Database (OLTP) | PostgreSQL 16 (Docker) |
| Frontend | HTML, JavaScript (fetch API) |
| Testing (planned) | pytest, Selenium, requests, Postman, Great Expectations / dbt |
| Infrastructure | Docker, Docker Compose, GitHub Actions (planned) |

## Project Structure
jobtrackr-qa/ ├── app/ │ ├── backend/ # FastAPI application │ └── frontend/ # HTML/JavaScript pages ├── db/ # Database schema and seed SQL ├── etl/ # ETL pipeline (Week 4) ├── tests/ │ ├── ui/ # Selenium tests (Week 3) │ ├── api/ # API tests (Week 2) │ ├── db/ # Database tests (Week 4) │ ├── dwh/ # Data warehouse tests (Week 4) │ └── e2e/ # Cross-layer tests (Week 5) ├── docs/ # Requirements, test plan, test cases, bug reports ├── docker-compose.yml ├── requirements.txt └── README.md

## Prerequisites

- Git
- Python 3.12 or later
- Docker Desktop
- A modern browser (Google Chrome recommended)
- Optional: Postman, DBeaver, VS Code

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sbqatester/jobtrackr-qa.git
cd jobtrackr-qa
```
2. Start the database
```bash
docker compose up -d
```
This starts PostgreSQL on localhost:5432 and loads the schema from db/schema.sql.
3. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```
4. Install dependencies
   ```bash
    pip install -r requirements.txt```
5. Run the API
```bash
   uvicorn app.backend.main:app --reload
```
Health check:  http://localhost:8000/health 
Interactive API docs (Swagger):  http://localhost:8000/docs
6. Open the frontend
Open app/frontend/index.html in your browser while the API is running.

Database
The schema has three tables:

users: account credentials (email unique, hashed password)
applications: job applications, with status constrained to the five allowed values and salary required to be positive when provided
status_history: an audit trail of status changes
Foreign keys use ON DELETE CASCADE, so deleting a user removes their applications and history.

To reset the database (this deletes all data and reruns the schema):

bash


docker compose down -v
docker compose up -d
Manual Testing Artifacts
docs/requirements.md: user stories and acceptance criteria
docs/test_plan.md: test strategy and scope
docs/test_cases.md: manual test cases
docs/bug_reports/: logged defects
postman/: Postman collection and environment
Security Note
This project uses local development credentials in docker-compose.yml and the application config. Do not reuse them in production. Move secrets to environment variables before deploying.

Author
Sourav Bhattacharya: QA professional with 20 years of experience, transitioning into test automation, AI-assisted testing, and data quality engineering.

LinkedIn: (https://www.linkedin.com/in/sourav-bhattacharya-05622a33/)
Email: iamqasourav@gmail.com
License
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


