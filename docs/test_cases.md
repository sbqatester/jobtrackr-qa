# Manual Test Cases: JobTrackr

Environment: Windows 11, Chrome, uvicorn on http://localhost:8000, Docker Compose database
Tester: Your Name
Build: <commit hash from `git rev-parse --short HEAD`>

Each test can be run in the UI at http://localhost:8000/ui/ or in the API at http://localhost:8000/docs. Where the steps say "API", use /docs or Postman. Status values: Not run, Pass, Fail, Blocked.

---

## Authentication and Registration

### TC-001: Reject empty company name
- **Priority:** High
- **Preconditions:** User is logged in
- **Test data:** Company = "" (empty), Role = "Backend Developer", Status = "Applied", Salary = 80000
- **Steps:**
  1. Open the add-application form
  2. Leave Company empty
  3. Fill in Role, Status, and Salary with the test data
  4. Click Add
- **Expected result:** An error message appears under or near the Company field. No application is saved, and the list does not change. (API: 422 Unprocessable Entity.)
- **Status:** Not run

### TC-002: Reject salary of 0
- **Priority:** High
- **Preconditions:** User is logged in
- **Test data:** Company = "Acme Corp", Role = "QA Analyst", Status = "Applied", Salary = 0
- **Steps:**
  1. Open the add-application form
  2. Fill in all fields using the test data
  3. Click Add
- **Expected result:** The application is rejected with an error. Nothing is saved. (API: 422, because the model requires salary greater than 0.)
- **Status:** Not run

### TC-003: Reject negative salary
- **Priority:** High
- **Preconditions:** User is logged in
- **Test data:** Company = "Acme Corp", Role = "QA Analyst", Status = "Applied", Salary = -5000
- **Steps:**
  1. Open the add-application form
  2. Fill in all fields using the test data
  3. Click Add
- **Expected result:** The application is rejected with an error. Nothing is saved. (API: 422.)
- **Status:** Not run

### TC-004: Reject invalid status
- **Priority:** High
- **Preconditions:** User is logged in
- **Test data:** Company = "Acme Corp", Role = "QA Analyst", Status = "Maybe", Salary = 80000
- **Steps:**
  1. Open the add-application form
  2. Enter "Maybe" in the Status field. If the UI uses a dropdown, use the API instead and send the value directly.
  3. Click Add
- **Expected result:** The request is rejected with an error, and no application is saved. (API: 422. If the status is restricted to a fixed list, the value must be one of the allowed options.)
- **Status:** Not run

### TC-005: Reject duplicate registration email
- **Priority:** High
- **Preconditions:** An account with the email `qa.user1@example.com` already exists
- **Test data:** Email = `qa.user1@example.com`, Password = `Test12345!`
- **Steps:**
  1. Send `POST /auth/register` with the test data (API)
  2. Send the same request a second time
- **Expected result:** The first request succeeds (201). The second request is rejected with a clear error such as "Email already registered" (typically 400 or 409). No second account is created.
- **Status:** Not run

### TC-006: User A cannot view or change User B's application
- **Priority:** High
- **Preconditions:** Two accounts exist: `qa.user1@example.com` and `qa.user2@example.com`. User 1 has created at least one application and you have its ID.
- **Test data:** User 1's application ID (for example, 1). Use User 2's token.
- **Steps:**
  1. Log in as User 1 and note the ID of one of their applications
  2. Log out, then log in as User 2 and get User 2's token
  3. Send `GET /applications/{id}` with User 2's token, using User 1's ID (API)
  4. Send `PUT /applications/{id}` with User 2's token and a changed status
  5. Send `DELETE /applications/{id}` with User 2's token
  6. Log in as User 1 and check that the application is unchanged
- **Expected result:** Each request from User 2 is rejected with 404 (preferred, because it does not reveal that the record exists) or 403. User 2 never sees User 1's data. User 1's application is unchanged and not deleted.
- **Status:** Not run

### TC-007: Reject registration with an invalid email format
- **Priority:** Medium
- **Preconditions:** None (user is logged out)
- **Test data:** Email = "not-an-email", Password = `Test12345!`
- **Steps:**
  1. Send `POST /auth/register` with the test data (API), or use the register form if one exists
  2. Repeat with Email = "user@" and Email = "@example.com"
- **Expected result:** Each request is rejected with a 422 error or a clear message. No account is created.
- **Status:** Not run

### TC-008: Reject registration with an empty password
- **Priority:** High
- **Preconditions:** None (user is logged out)
- **Test data:** Email = `qa.empty.pw@example.com`, Password = "" (empty)
- **Steps:**
  1. Send `POST /auth/register` with the test data (API)
  2. Check the response
  3. Send `POST /auth/login` with the same email and an empty password
- **Expected result:** Registration is rejected with 422 or a clear error. No account is created, so the login attempt also fails.
- **Status:** Not run

### TC-009: Reject login with an unregistered email
- **Priority:** Medium
- **Preconditions:** `nobody@example.com` has never been registered
- **Test data:** Email = `nobody@example.com`, Password = `Test12345!`
- **Steps:**
  1. Open the UI at http://localhost:8000/ui/
  2. Enter the test data
  3. Click Log in
- **Expected result:** A red error message appears (for example, "Invalid email or password"). The user is not logged in, and no application list is shown. The message should not reveal whether the email exists.
- **Status:** Not run

### TC-010: Reject login with the wrong password
- **Priority:** High
- **Preconditions:** `qa.user1@example.com` is registered with password `Test12345!`
- **Test data:** Email = `qa.user1@example.com`, Password = `WrongPass999`
- **Steps:**
  1. Open the UI at http://localhost:8000/ui/
  2. Enter the test data
  3. Click Log in
  4. Log in again with the correct password to confirm the account still works
- **Expected result:** A red error message appears, and the user is not logged in. The correct password still works afterward.
- **Status:** Not run

### TC-011: Reject login with an empty password
- **Priority:** Medium
- **Preconditions:** `qa.user1@example.com` is registered
- **Test data:** Email = `qa.user1@example.com`, Password = "" (empty)
- **Steps:**
  1. Open the UI login form
  2. Enter the email and leave Password empty
  3. Click Log in
- **Expected result:** The request is rejected with an error. The user is not logged in.
- **Status:** Not run

---

## Application Form and Data Validation

### TC-012: Reject an application with a missing role
- **Priority:** High
- **Preconditions:** User is logged in
- **Test data:** Company = "Acme Corp", Role = "" (empty), Status = "Applied", Salary = 80000
- **Steps:**
  1. Open the add-application form
  2. Fill in Company, Status, and Salary, and leave Role empty
  3. Click Add
- **Expected result:** An error appears and no application is saved. (API: 422.)
- **Status:** Not run

### TC-013: Reject a non-numeric salary
- **Priority:** Medium
- **Preconditions:** User is logged in
- **Test data:** Company = "Acme Corp", Role = "QA Analyst", Status = "Applied", Salary = "eighty thousand" or "80k"
- **Steps:**
  1. Open the add-application form
  2. Enter the text value in the Salary field. If the browser blocks the text, use the API instead.
  3. Click Add
- **Expected result:** The request is rejected with an error, and nothing is saved. (API: 422, with a message that salary must be a valid integer.)
- **Status:** Not run

### TC-014: Company name length limit (150 characters)
- **Priority:** Medium
- **Preconditions:** User is logged in
- **Test data:**
  - Company with 150 characters (for example, the letter "A" repeated 150 times): should be accepted
  - Company with 151 characters: should be rejected
- **Steps:**
  1. Add an application with the 150-character company name and click Add
  2. Confirm the application appears in the list
  3. Add an application with the 151-character company name and click Add
- **Expected result:** The 150-character company is saved. The 151-character company is rejected with an error, and nothing new is saved.
- **Status:** Not run

### TC-015: Status defaults to "Applied" when left unchanged
- **Priority:** Medium
- **Preconditions:** User is logged in
- **Test data:** Company = "Default Status Co", Role = "Data Analyst", Salary = 65000. Leave Status at its default.
- **Steps:**
  1. Open the add-application form
  2. Fill in Company, Role, and Salary. Do not change Status
  3. Click Add
  4. Refresh the page and look at the new row
- **Expected result:** The new application is saved with status "Applied", and the status is still "Applied" after refresh.
- **Status:** Not run

---

## Editing and Deleting Applications

### TC-016: Edit an application's status
- **Priority:** High
- **Preconditions:** User is logged in and has one application with status "Applied"
- **Test data:** Change Status from "Applied" to "Interview"
- **Steps:**
  1. Find the application in the list and click Edit
  2. Change Status to "Interview"
  3. Click Save
  4. Refresh the page
- **Expected result:** The row shows "Interview" right after saving and still shows it after refresh. Other fields (company, role, salary) are unchanged. (API: `PUT /applications/{id}` returns 200.)
- **Status:** Not run

### TC-017: Delete an application
- **Priority:** High
- **Preconditions:** User is logged in and has at least one application
- **Test data:** Any application in the list
- **Steps:**
  1. Note the company and role of the application you will delete
  2. Click Delete on that row
  3. Confirm the deletion if a prompt appears
  4. Refresh the page
- **Expected result:** The row disappears immediately and stays gone after refresh. (API: `DELETE /applications/{id}` returns 200 or 204.)
- **Status:** Not run

### TC-018: Delete an application that does not exist
- **Priority:** Medium
- **Preconditions:** User is logged in. Use an ID that does not exist, such as 99999.
- **Test data:** Application ID = 99999
- **Steps:**
  1. Send `DELETE /applications/99999` with a valid token (API)
  2. Check the response
- **Expected result:** The API returns 404 Not Found with a message such as "Application not found". The server does not crash, and no other application is deleted.
- **Status:** Not run

---

## Authorization and Session

### TC-019: List applications with no token
- **Priority:** High
- **Preconditions:** None
- **Test data:** No Authorization header
- **Steps:**
  1. Open http://localhost:8000/docs
  2. Open `GET /applications` and click Try it out without clicking Authorize
  3. Click Execute
- **Expected result:** The API returns 401 Unauthorized. No application data is returned.
- **Status:** Not run

### TC-020: List applications with an invalid token
- **Priority:** High
- **Preconditions:** None
- **Test data:** Authorization: Bearer `abc.def.ghi` (a made-up token)
- **Steps:**
  1. Open http://localhost:8000/docs
  2. Click Authorize and enter `abc.def.ghi` as the token
  3. Open `GET /applications`, click Try it out, then Execute
  4. Also try a valid-looking token from a previous session with one character changed
- **Expected result:** Each request returns 401 Unauthorized. No application data is returned.
- **Status:** Not run

### TC-021: New user sees an empty application list
- **Priority:** Medium
- **Preconditions:** A brand-new account has been registered and has no applications
- **Test data:** Email = `qa.empty.list@example.com`, Password = `Test12345!`
- **Steps:**
  1. Log in as the new user through the UI
  2. Look at the application list
- **Expected result:** The list is empty, with no errors and no applications from other users. (API: `GET /applications` returns 200 and an empty array `[]`.)
- **Status:** Not run
