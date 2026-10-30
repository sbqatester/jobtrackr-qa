# JobTrackr Requirements

## Personas

- **Job Seeker:** a person actively applying for jobs and tracking their progress
- **Returning User:** a registered user who logs in regularly to update applications

## Status Pipeline

Applied → Screening → Interview → Offer → Rejected

New applications default to `Applied`. Any status can be changed to any other allowed status.

---

## Authentication

### US-01: Register an account
As a **job seeker**, I want to **register with my email and password** so that **my applications are saved privately to my account**.

**Acceptance Criteria**
- AC1: Registration succeeds with a valid, unused email and a password of at least 8 characters, and returns HTTP 201.
- AC2: Registration with an email that already exists is rejected with an error and no new user is created.
- AC3: Registration with an invalid email format (for example, `user@` or `plainaddress`) is rejected with a validation error.
- AC4: The password is stored as a hash in the database. The plain-text password never appears in the `users` table.

### US-02: Log in
As a **returning user**, I want to **log in with my email and password** so that **I can access my saved applications**.

**Acceptance Criteria**
- AC1: Valid credentials return a JWT access token with HTTP 200.
- AC2: Wrong password or unknown email returns HTTP 401 with a generic message that does not reveal which field was wrong.
- AC3: After a successful login in the UI, the dashboard is displayed.

### US-03: Protect private data
As a **job seeker**, I want **every application endpoint to require a valid login** so that **nobody can view or change my data without signing in**.

**Acceptance Criteria**
- AC1: Requests to `/applications` endpoints without a token return HTTP 401.
- AC2: Requests with an invalid or malformed token return HTTP 401.
- AC3: Requests with a valid token are processed normally.

---

## Application Management

### US-04: Add a job application
As a **job seeker**, I want to **add a job application with company, role, and details** so that **I can track every opportunity I'm pursuing**.

**Acceptance Criteria**
- AC1: A valid submission returns HTTP 201 and the new record includes an `id` and `created_at` timestamp.
- AC2: The new application appears in the list view without a manual page refresh.
- AC3: The application is linked to the logged-in user's account (`user_id` matches the token owner).

### US-05: Required fields for an application
As a **job seeker**, I want the system to **require company and role** so that **every application is identifiable in my list**.

**Acceptance Criteria**
- AC1: Submitting without `company` is rejected with a validation error and no record is created.
- AC2: Submitting without `role` is rejected with a validation error and no record is created.
- AC3: Whitespace-only values for `company` or `role` are rejected.

### US-06: Salary must be a positive number
As a **job seeker**, I want the system to **accept salary only as a positive number when I provide it** so that **my salary data is meaningful for comparison**.

**Acceptance Criteria**
- AC1: A positive salary (for example, `85000`) is accepted and saved.
- AC2: A zero or negative salary (for example, `0` or `-100`) is rejected with a validation error.
- AC3: Leaving salary empty is accepted, and the field is stored as empty (NULL).

### US-07: View my applications
As a **returning user**, I want to **see a list of all my applications** so that **I can review where each one stands**.

**Acceptance Criteria**
- AC1: The list shows company, role, status, and date for every application belonging to the user.
- AC2: A user with no applications sees an empty-state message, not an error.
- AC3: `GET /applications` returns HTTP 200 with a JSON array.

### US-08: Edit an application
As a **returning user**, I want to **edit the details of an application** so that **my records stay accurate as I learn more**.

**Acceptance Criteria**
- AC1: Changing company, role, or salary and saving returns HTTP 200 and the list shows the new values.
- AC2: Editing with invalid data (for example, a negative salary) is rejected and the original values remain unchanged.
- AC3: Editing an application that belongs to another user returns HTTP 404 or 403, and the data is not changed.

### US-09: Update application status
As a **returning user**, I want to **move an application through the status pipeline** so that **I always know my current stage in the hiring process**.

**Acceptance Criteria**
- AC1: The status can be changed to any of the five allowed values: Applied, Screening, Interview, Offer, Rejected.
- AC2: A value outside the five allowed values (for example, `Hired`) is rejected, and the stored status does not change.
- AC3: The updated status is visible in the list view after the change.

### US-10: Track status history
As a **returning user**, I want **every status change recorded with its timestamp** so that **I can see how an application progressed over time**.

**Acceptance Criteria**
- AC1: Each status change creates one row in `status_history` with the old status, new status, and timestamp.
- AC2: Creating an application writes an initial history entry with status `Applied`.
- AC3: A failed status update does not create a history row.

### US-11: Delete an application
As a **returning user**, I want to **delete an application** so that **I can remove opportunities I no longer want to track**.

**Acceptance Criteria**
- AC1: Deleting an application returns HTTP 204 (or 200) and the record no longer appears in the list.
- AC2: The application's `status_history` rows are removed with it.
- AC3: Deleting an application that does not exist returns HTTP 404.

### US-12: Data isolation between users
As a **job seeker**, I want **my applications hidden from other users** so that **my job search stays private**.

**Acceptance Criteria**
- AC1: User A cannot see User B's applications in the list or through `GET /applications/{id}`.
- AC2: User A cannot update or delete User B's applications.
- AC3: Each user's list contains only records where `user_id` matches their own account.

---

## Usability

### US-13: Simple web interface
As a **job seeker**, I want a **simple web page to manage my applications** so that **I can use the app without knowing the API**.

**Acceptance Criteria**
- AC1: All CRUD actions (add, view, edit, delete) can be completed from the browser.
- AC2: Error messages from the API are displayed to the user in readable text.
- AC3: The page works in the latest version of Google Chrome.
