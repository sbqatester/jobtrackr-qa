# JobTrackr Traceability Matrix

| Story | Requirement | Acceptance Criteria | Test Level(s) | Planned Test Case IDs | Week |
|---|---|---|---|---|---|
| US-01 | Register an account | AC1 to AC4 | API, DB, UI | TC-API-001 to TC-API-004, TC-DB-001, TC-UI-001 | 2, 3, 4 |
| US-02 | Log in | AC1 to AC3 | API, UI | TC-API-005 to TC-API-007, TC-UI-002 | 2, 3 |
| US-03 | Protect private data | AC1 to AC3 | API | TC-API-008 to TC-API-010 | 2 |
| US-04 | Add a job application | AC1 to AC3 | API, UI, DB | TC-API-011 to TC-API-013, TC-UI-003, TC-DB-002 | 2, 3, 4 |
| US-05 | Required fields | AC1 to AC3 | API, UI, DB | TC-API-014 to TC-API-016, TC-UI-004, TC-DB-003 | 2, 3, 4 |
| US-06 | Salary must be positive | AC1 to AC3 | API, DB | TC-API-017 to TC-API-019, TC-DB-004 | 2, 4 |
| US-07 | View my applications | AC1 to AC3 | API, UI | TC-API-020 to TC-API-022, TC-UI-005 | 2, 3 |
| US-08 | Edit an application | AC1 to AC3 | API, UI | TC-API-023 to TC-API-025, TC-UI-006 | 2, 3 |
| US-09 | Update application status | AC1 to AC3 | API, UI, DB | TC-API-026 to TC-API-028, TC-UI-007, TC-DB-005 | 2, 3, 4 |
| US-10 | Track status history | AC1 to AC3 | DB, API | TC-DB-006 to TC-DB-008, TC-API-029 | 4, 2 |
| US-11 | Delete an application | AC1 to AC3 | API, UI, DB | TC-API-030 to TC-API-032, TC-UI-008, TC-DB-009 | 2, 3, 4 |
| US-12 | Data isolation | AC1 to AC3 | API, DB | TC-API-033 to TC-API-035, TC-DB-010 | 2, 4 |
| US-13 | Simple web interface | AC1 to AC3 | UI, Manual | TC-UI-009 to TC-UI-011, TC-MAN-001 | 3, Ongoing |
| Week 4 | Data warehouse load | ETL output matches OLTP | DWH | TC-DWH-001 to TC-DWH-004 | 4 |
| Week 5 | Full user journey | Register to delete across all layers | E2E | TC-E2E-001 to TC-E2E-002 | 5 |

## Coverage Check

Before marking Week 2 complete, confirm:
- Every acceptance criterion in `requirements.md` appears in at least one row of `test_cases.md`.
- Every test case in `test_cases.md` maps back to a story in this matrix.
- Any story without a test is listed as a gap with a planned date.
