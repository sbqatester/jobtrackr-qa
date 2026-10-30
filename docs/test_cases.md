# JobTrackr Test Cases

## 1. Conventions

- **ID format:** `TC-[LEVEL]-[NNN]`, matching `docs/traceability.md`
- **Priority:** High (core flow or security), Medium, Low
- **Base URL:** `http://localhost:8000`
- **Endpoint paths** (for example, `/auth/register`) are assumed. Update them to match your routes in `app/backend`.
- **Status codes** come from `docs/requirements.md`. Verify each one in Swagger (`/docs`) and fix whichever side is wrong (risk R3).

## 2. Test Data

- **Email:** unique per test run, for example `qa_<timestamp>@example.com`, so tests don't collide.
- **Valid password:** `ValidPass123` (at least 8 characters).
- **Isolation:** each test creates its own user and does not rely on data from other tests.

---

## 3. API Test Cases: US-01 Register an Account

### TC-API-001: Register with valid data
- **Traces to:** US-01 AC1
- **Priority:** High
- **Preconditions:** API is running. The email is not registered.
- **Steps:**
  1. `POST /auth/register` with `{"email": "<unique email>", "password": "ValidPass123"}`.
- **Expected result:**
  - HTTP **201**.
  - Response includes an `id` and the `email`.
  - One new row exists in `users` for that email.

### TC-API-002: Register with a duplicate email
- **Traces to:** US-01 AC2
- **Priority:** High
- **Preconditions:** A user with the email already exists (create it with TC-API-001).
- **Steps:**
  1. `POST /auth/register` with the same email and a valid password.
- **Expected result:**
  - HTTP **409** (or the code your API returns, updated in the requirements).
  - Response includes a clear error message.
  - Only one row exists in `users` for that email.

### TC-API-003: Register with invalid input
- **Traces to:** US-01 AC3 (and the 8-character minimum in AC1)
- **Priority:** High
- **Test data (one request per row):**

  | Input | Email | Password |
  |---|---|---|
  | Invalid email, no domain | `user@` | `ValidPass123` |
  | Invalid email, no @ | `plainaddress` | `ValidPass123` |
  | Password too short | `<unique email>` | `Short1` (7 characters) |

- **Expected result:**
  - HTTP **422** with a validation error that names the failing field.
  - No row is created in `users`.

### TC-API-004: Password is never returned or stored in plain text
- **Traces to:** US-01 AC4
- **Priority:** High
- **Preconditions:** Registration with `ValidPass123` succeeds.
- **Steps:**
  1. Register a user and read the response body.
  2. Query the database: `SELECT * FROM users WHERE email = '<email>';` (confirm the column names in `db/schema.sql`).
- **Expected result:**
  - The response body does not contain `ValidPass123` or any hash.
  - No column in the `users` row contains `ValidPass123`.
  - The password column contains a hash (for example, a string starting with `$2b$` if bcrypt is used).

---

## 4. API Test Cases: US-02 Log In

### TC-API-005: Log in with valid credentials
- **Traces to:** US-02 AC1
- **Priority:** High
- **Preconditions:** A registered user exists.
- **Steps:**
  1. `POST /auth/login` with the user's email and password (confirm whether your API expects JSON or form data).
- **Expected result:**
  - HTTP **200**.
  - Response includes a non-empty `access_token` string and `token_type` of `bearer`.

### TC-API-006: Log in with invalid credentials
- **Traces to:** US-02 AC2
- **Priority:** High
- **Test data (one request per row):**

  | Case | Email | Password |
  |---|---|---|
  | Wrong password | Registered email | `WrongPass999` |
  | Unknown email | `nobody_<timestamp>@example.com` | `ValidPass123` |

- **Expected result:**
  - HTTP **401** for both cases.
  - Both cases return the **same** generic message, so the response does not reveal whether the email exists.
  - No `access_token` is returned.

### TC-API-007: Login token is accepted by a protected endpoint
- **Traces to:** US-02 AC1 and AC3 (the dashboard display for AC3 is covered by TC-UI-002)
- **Priority:** High
- **Preconditions:** A registered user exists.
- **Steps:**
  1. Log in with TC-API-005 and copy the `access_token`.
  2. `GET /applications` with the header `Authorization: Bearer <access_token>`.
- **Expected result:**
  - HTTP **200**.
  - Response is a JSON array (empty for a new user).

---

## 5. API Test Cases: US-03 Protect Private Data

### TC-API-008: Requests without a token are rejected
- **Traces to:** US-03 AC1
- **Priority:** High
- **Steps:**
  1. `GET /applications` with no `Authorization` header.
  2. `POST /applications` with no `Authorization` header and a valid body.
- **Expected result:**
  - Both return HTTP **401**.
  - No record is created by the POST.

### TC-API-009: Requests with an invalid or malformed token are rejected
- **Traces to:** US-03 AC2
- **Priority:** High
- **Test data (header values for `GET /applications`):**

  | Case | Authorization header |
  |---|---|
  | Random string | `Bearer not-a-real-token` |
  | Tampered token | A valid token with its last 5 characters changed |
  | Empty bearer value | `Bearer ` |
  | Wrong scheme | `Token <valid token>` |

- **Expected result:** HTTP **401** for every case.

### TC-API-010: Requests with a valid token are processed
- **Traces to:** US-03 AC3
- **Priority:** High
- **Preconditions:** A valid token from TC-API-005.
- **Steps:**
  1. `GET /applications` with `Authorization: Bearer <valid token>`.
- **Expected result:** HTTP **200** with a JSON array. The request is not blocked by authentication.

---

## 6. Summary

| ID | Title | Story / AC | Priority | Status |
|---|---|---|---|---|
| TC-API-001 | Register with valid data | US-01 AC1 | High | Not run |
| TC-API-002 | Register with duplicate email | US-01 AC2 | High | Not run |
| TC-API-003 | Register with invalid input | US-01 AC3 | High | Not run |
| TC-API-004 | Password never returned or stored in plain text | US-01 AC4 | High | Not run |
| TC-API-005 | Log in with valid credentials | US-02 AC1 | High | Not run |
| TC-API-006 | Log in with invalid credentials | US-02 AC2 | High | Not run |
| TC-API-007 | Login token accepted by protected endpoint | US-02 AC1, AC3 | High | Not run |
| TC-API-008 | Requests without a token rejected | US-03 AC1 | High | Not run |
| TC-API-009 | Invalid or malformed token rejected | US-03 AC2 | High | Not run |
| TC-API-010 | Valid token processed | US-03 AC3 | High | Not run |

Status values: Not run, Pass, Fail, Blocked. Record the actual status code for each failure in your bug report.

---

## 7. Next Test Cases

TC-API-011 onward covers US-04 to US-12 and is added in the same format.
