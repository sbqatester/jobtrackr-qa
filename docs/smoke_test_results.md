# Smoke Test Results

Date: 2026-11-03
Tester: Your Name
Build: <commit hash from `git rev-parse --short HEAD`>
Environment: Windows 11, Chrome, uvicorn on http://localhost:8000, Docker Compose database

Result key: **Pass**, **Fail** (a bug, logged in docs/bug_reports/), or **Blocked** (feature not built yet, not a bug).

## Setup checks

| # | Flow | Steps | Expected | Result | Notes |
|---|---|---|---|---|---|
| 0a | Database running | Run `docker compose ps` | Database container is "running" or "Up" | | |
| 0b | Server running | Run `uvicorn app.backend.main:app --reload` | "Application startup complete" in terminal | | |

## Core smoke tests

| # | Flow | Steps | Expected | Result | Notes |
|---|---|---|---|---|---|
| 1 | Health check | Open http://localhost:8000/health | `"status": "ok"` and `"database": "connected"` | | |
| 2 | API docs load | Open http://localhost:8000/docs | Swagger page lists all endpoints | | |
| 3 | UI loads | Open http://localhost:8000/ui/ | Login form appears | | |
| 4 | UI console clean | Press F12, open the Console tab, reload /ui/ | No red errors | | |
| 5 | Register | Test `POST /auth/register` in /docs (Try it out, enter email and password, Execute) | 201 or success response, no error | | If not built: mark Blocked, note "POST /auth/register not implemented yet" |
| 6 | Login (valid) | Log in through the UI with the registered account | Application list appears | | |
| 7 | Login (wrong password) | Log in with the correct email and a wrong password | Red error message, no access | | |
| 8 | Login (unknown email) | Log in with an email that was never registered | Red error message, no access | | |
| 9 | Add application | Fill in company, role, status, and salary, then click Add | New row appears in the list | | |
| 10 | Refresh keeps data | Refresh the page after step 9 | The new row is still there | | |
| 11 | Edit application | Change the status and save | Change is shown in the list | | |
| 12 | Edit persists | Refresh the page after step 11 | Updated status is still shown | | |
| 13 | Delete application | Click Delete on a row | Row disappears | | |
| 14 | Delete persists | Refresh the page after step 13 | Row stays gone | | |
| 15 | Logout | Click Logout (or clear the token) and try to open the list | Redirected to login, no data shown | | |
| 16 | Protected API, no token | Call `GET /applications` in /docs without authorizing | 401 Unauthorized | | |
| 17 | Protected API, valid token | Authorize in /docs with the token, then call `GET /applications` | 200 OK with a list (may be empty) | | |

## Summary

- Total tests: 19 (plus setup checks)
- Pass:
- Fail:
- Blocked:

## Bugs found

| Bug ID | Test # | Short description |
|---|---|---|
| | | |
