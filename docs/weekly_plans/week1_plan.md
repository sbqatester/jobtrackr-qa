Week 1: Setup and Foundation
Goal for this week: Have a running application backend, a PostgreSQL database in Docker, a simple
frontend, project structure on GitHub, and initial QA artifacts (requirements, test plan, manual test cases,
Postman collection, and a few bug reports). Expect about 2–3 hours per day.
Part 1: Tools and IDEs to Install
Required tools and why you need them
• Git — version control
• GitHub account — host repo, CI/CD, and Pages
• Python 3.12+ — main language for app, tests, and ETL
• VS Code — primary IDE
• Docker Desktop — run PostgreSQL, warehouse, and Selenium Grid
• DBeaver Community — visual database client for PostgreSQL
• Postman — manual API exploration and collections
• Google Chrome — browser for Selenium tests
VS Code extensions to install
• Python and Pylance (Microsoft)
• Docker (Microsoft)
• Ruff (linting and formatting)
• GitLens (Git history)
• Thunder Client (lightweight API testing inside VS Code) — optional alternative to Postman
• SQLTools with PostgreSQL driver (optional if not using DBeaver)
• GitHub Copilot (optional)
• Markdown All in One and YAML support
Optional but useful tools
• PyCharm Community (if you prefer a heavier Python IDE)
• Node.js LTS (only if you later build a React frontend)
• Windows users: WSL2 (Ubuntu) to replicate Linux-like environment
• Ollama or local LLM runner (for AI features in later weeks)
• An AI chat assistant (ChatGPT, Claude, Gemini) for learning and code explanation
Verify your installs
git --version
python --version
pip --version
docker --version
docker compose version
code --version
Part 2: Day-by-Day Plan (detailed)
Day 1: Environment and Repo Setup (2–3 hrs)
1. Install the required tools from Part 1 and run the version checks.
Page 1
2. Create a GitHub repository named jobtrackr-qa (public). Add a README and a Python .gitignore
file.
3. Clone the repo locally and open it in VS Code.
4. Create the initial folder structure.
5. Create and activate a Python virtual environment.
6. Make your first commit and push to GitHub.
Suggested folder structure (create these directories and placeholder files):
jobtrackr-qa/
├── app/
│ ├── backend/ # FastAPI app
│ └── frontend/ # static HTML/JS pages
├── db/ # schema and seed SQL
├── etl/ # pipeline code (Week 4)
├── tests/
│ ├── ui/
│ ├── api/
│ ├── db/
│ ├── dwh/
│ └── e2e/
├── docs/ # test plan, requirements, bug reports
├── docker-compose.yml
├── requirements.txt
└── README.md
Virtual environment commands
cd jobtrackr-qa
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
Day 2: Requirements and Test Thinking (2 hrs)
1. Create docs/requirements.md and write 10–15 user stories using the template: As a [persona], I
want [feature] so that [benefit].
2. For each user story, add 2–4 acceptance criteria (clear, testable).
3. Create docs/test_plan.md with scope, in-scope/out-of-scope, test levels (UI, API, DB, DWH), tools,
entry/exit criteria, and risks.
4. Create a traceability matrix (spreadsheet or markdown table) mapping requirements to planned test
cases.
Day 3: Database Schema (2–3 hrs)
Create docker-compose.yml to run PostgreSQL and a schema initialization file. Start the database and
confirm tables with DBeaver or psql.
docker-compose.yml (example):
Page 2
services:
db:
image: postgres:16
container_name: jobtrackr_db
environment:
POSTGRES_USER: jobtrackr
POSTGRES_PASSWORD: jobtrackr_pw
POSTGRES_DB: jobtrackr
ports:
- "5432:5432"
volumes:
- pgdata:/var/lib/postgresql/data
- ./db/schema.sql:/docker-entrypoint-initdb.d/schema.sql
volumes:
pgdata:
db/schema.sql (core tables):
CREATE TABLE users (
id SERIAL PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
password_hash VARCHAR(255) NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE applications (
id SERIAL PRIMARY KEY,
user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
company VARCHAR(150) NOT NULL,
role VARCHAR(150) NOT NULL,
status VARCHAR(20) NOT NULL DEFAULT 'Applied' CHECK (status IN
('Applied','Screening','Interview','Offer','Rejected')),
salary NUMERIC(10,2) CHECK (salary IS NULL OR salary > 0),
source VARCHAR(50),
applied_on DATE NOT NULL DEFAULT CURRENT_DATE,
updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE status_history (
id SERIAL PRIMARY KEY,
application_id INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
old_status VARCHAR(20),
new_status VARCHAR(20) NOT NULL,
changed_at TIMESTAMP NOT NULL DEFAULT NOW()
);
Start the database with: docker compose up -d. Then connect with DBeaver or psql and confirm that
users, applications, and status_history exist.
Page 3
Day 4: Backend API (3 hrs)
Create a minimal FastAPI backend, install dependencies, and verify the health endpoint and automatic
OpenAPI docs.
requirements.txt (starter):
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
passlib[bcrypt]
python-jose[cryptography]
pydantic[email]
pytest
requests
app/backend/main.py (health check example):
from fastapi import FastAPI
from sqlalchemy import create_engine, text
DATABASE_URL = "postgresql+psycopg2://jobtrackr:jobtrackr_pw@localhost:5432/
jobtrackr"
engine = create_engine(DATABASE_URL)
app = FastAPI(title="JobTrackr QA API", version="0.1.0")
@app.get("/health")
def health():
with engine.connect() as conn:
conn.execute(text("SELECT 1"))
return {"status": "ok", "database": "connected"}
Run the server with: uvicorn app.backend.main:app --reload. Open http://localhost:8000/health and
http://localhost:8000/docs to confirm.
Build these endpoints over the week: POST /auth/register, POST /auth/login (JWT), GET/POST/PUT/
DELETE /applications. Test them via /docs or Postman as you implement.
Day 5: Basic Frontend (2–3 hrs)
Create a very simple static frontend (index.html) that uses fetch() to call your API. The UI should provide:
login form, application list, and an add-application form.
QA requirement: assign stable id or data-testid attributes to every interactive element now (for Selenium
later). Example ids: email, password, login-btn, add-company, add-role, add-submit.
Day 6: Manual Smoke Testing and First QA Artifacts (2–3 hrs)
1. Perform manual smoke tests for main flows in the browser and record results.
2. Create 15–20 manual test cases and store them in docs/test_cases.md. Include ID, title,
preconditions, steps, expected result, and priority.
3. Create a Postman collection and environment variables (base_url, token). Add register, login, and
CRUD requests.
Page 4
4. Log at least 2 bug reports in docs/bug_reports/. Use a simple template: ID, title, severity, priority,
steps to reproduce, expected, actual, environment.
Sample manual test cases to include: empty company name, salary 0 or negative, invalid status, duplicate
registration email, unauthorized access to another user's applications.
Day 7: Commit, Review, and Buffer (1–2 hrs)
1. Update README with project description, quick setup steps, and current status (Week 1 complete).
2. Commit and push all changes with clear messages.
3. Review the Week 1 checklist and finish any remaining items.
4. Write a short retrospective in docs/weekly_log.md: what went well, what was hard, and action
items for Week 2.
Week 1 Checklist
• All required tools installed and verified
• GitHub repo created with project folder structure
• Python virtual environment created and activated
• PostgreSQL running in Docker with schema loaded
• FastAPI running with /health and /docs
• Auth and at least basic applications CRUD endpoints implemented
• Simple frontend with stable element IDs
• 10–15 user stories and acceptance criteria
• Test plan draft
• 15+ manual test cases
• Postman collection created
• 2+ bug reports logged
• README updated and everything pushed to GitHub
Helpful Commands and Notes
Start DB:
docker compose up -d
Run FastAPI dev server:
uvicorn app.backend.main:app --reload
Install requirements:
pip install -r requirements.txt
Activate venv (Mac/Linux):
source .venv/bin/activate
Activate venv (Windows):
.venv\Scripts\activate
Page 5
Tips for Success in Week 1
• Focus on shipping a working, slightly rough app rather than perfection. The goal is a stable target
you can test and expand.
• As a senior QA, apply your manual testing experience to define crisp acceptance criteria and
meaningful test cases.
• Use stable element IDs for the frontend now to avoid brittle Selenium selectors later.
• Commit frequently with descriptive messages to show progress in your repo history.
• Use AI assistants to explain errors or suggest patterns, but run and validate every suggestion
yourself.
What I will help you with after Week 1
After you finish Week 1, tell me what is running (show the repo link or paste errors). I will provide: a
detailed Week 2 plan for API automation with pytest and contract testing, starter pytest fixtures,
Postman-to-pytest conversion tips, and example tests you can copy into the tests/api folder. If you prefer,
I can also generate sample code files to paste into your project.
Finished: This document contains a complete, executable Week 1 plan. When you are ready, share the
GitHub repo link or a short status update and I will prepare Week 2 materials and starter test code.
Page 6