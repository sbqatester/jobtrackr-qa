# BUG-001: Registration accepts a one-character password

- **ID:** BUG-001
- **Title:** Registration accepts a one-character password
- **Severity:** Medium (Critical / High / Medium / Low)
- **Priority:** High (High / Medium / Low; how soon it should be fixed)
- **Status:** Open
- **Found by:** Your name
- **Date:** 2026-11-05

## Environment
- OS: Windows 11
- Browser: Chrome 130 (or your version)
- Backend: FastAPI, running locally at http://localhost:8000
- Database: PostgreSQL in Docker, port 5433
- Commit: (run `git rev-parse --short HEAD`)

## Preconditions
- The app is running and the database is up.
- No account exists for test@example.com.

## Steps to reproduce
1. Open http://localhost:8000/ui in the browser.
2. Go to the register form.
3. Enter email `test@example.com` and password `a`.
4. Click **Register**.

## Expected result
Registration is rejected with a message saying the password is too short (for example, minimum 8 characters).

## Actual result
The account is created and the API returns 201 with the user's id and email.

## Evidence
- Screenshot: `docs/bug_reports/screenshots/BUG-001.png` (optional)
- API response: paste the JSON here

## Notes
Related to `app/backend/main.py`, `UserCreate.password` (`Field(min_length=1)`).
