# Test Cases – Internship Listing Portal

| Test ID | Scenario | Expected result |
|---|---|---|
| TC_INTERN_01 | Open home page | Internship cards are displayed |
| TC_INTERN_02 | Search for `design` | Only matching internships are displayed |
| TC_INTERN_03 | Filter location by `Chennai` | Chennai internships are displayed |
| TC_INTERN_04 | Select work mode `Remote` | Only remote internships are displayed |
| TC_INTERN_05 | Combine domain and work mode filters | Only records matching both filters are displayed |
| TC_INTERN_06 | Clear filters | All sample internships are displayed |
| TC_INTERN_07 | Open an internship details page | Correct title, company, stipend and deadline are displayed |
| TC_INTERN_08 | Submit application with valid details | Application is stored and confirmation page appears |
| TC_INTERN_09 | Submit with invalid email | Validation error is displayed; no application is saved |
| TC_INTERN_10 | Submit with invalid phone | Validation error is displayed; no application is saved |
| TC_INTERN_11 | Apply twice to the same internship with same email | Second attempt is blocked with a duplicate message |
| TC_INTERN_12 | Open an unknown internship ID | Not-found response is displayed without crashing |
| TC_INTERN_13 | Check `/health` | JSON response contains `status: ok` |

## Manual test data
- Name: Priya Sharma
- Email: priya@example.com
- Phone: 9876543210
- Resume link: https://example.com/priya-resume
- Cover note: I am interested in front-end development.
