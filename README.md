# InternHub – AI Internship Matching Engine

An AI-powered backend service for an internship platform that evaluates how well a student matches an internship role, identifies skill gaps, generates a tailored resume, and produces an ATS-style confidence score.

This project was built as part of **InternHub Track 2 – AI Assignment**.

---

## What This Project Does

This system takes:

* A **student profile** (skills, interests, projects, resume)
* An **internship job description**

and produces:

* A **match summary**
* A **skill gap analysis**
* A **recommendation on whether to apply**
* A **new resume customized for the job**
* A **confidence / ATS score**

The output is generated using a large language model (Gemini 2.0 Flash) and returned through a REST API.

---

## How It Works

1. **Admin adds data**

   * Student profiles and internship descriptions are created using Django Admin.

2. **AI matching is triggered**

   * An API call is made to:

     ```
     POST /api/match-results/
     ```

     with:

     ```json
     {
       "student": "Student Name",
       "internship": "Company - Role"
     }
     ```

3. **Data is prepared**

   * Student skills, interests, projects and resume are collected.
   * Internship job description and required skills are collected.

4. **AI reasoning**

   * Both are sent to Gemini-2.0-Flash using a structured prompt.
   * The model evaluates fit, identifies gaps, rewrites the resume, and assigns an ATS score.

5. **Results are saved**

   * The output is stored in the database as a `MatchResult`.
   * Each run is versioned so users can see historical results.

6. **Results are returned**

   * The API returns a clean JSON response containing the AI-generated analysis.

---

## Tech Stack

**Backend**

* Django
* Django REST Framework

**AI**

* Google Gemini 2.0 Flash

**Database**

* SQLite (can be replaced with PostgreSQL)

**Admin Interface**

* Django Admin
* Jazzmin (for modern admin UI)

**Other**

* PyPDF2 and python-docx for resume file parsing
* Custom DRF Renderer for standardized API responses

---

## Key Features

* AI-based internship matching
* Resume upload or text input
* Resume rewriting using LLM
* Skill gap detection
* ATS-style confidence score
* Versioned match history
* Clean REST API
* Admin dashboard for managing data and reviewing AI output

---

## Assumptions Made

* Student and internship data are managed by an internal admin user.
* Authentication and public user interfaces are out of scope for this assignment.
* AI output quality depends on the quality of the provided resume and job description.
* ATS score is an AI-estimated confidence score, not a real ATS engine.
* One internship match request runs one AI inference and stores a new versioned result.

---

## Why This Design

The goal was to simulate how a real internship platform would integrate AI into its hiring workflow:

* Profiles and job listings are stored in a database
* AI is used only when matching is requested
* Results are saved and can be reviewed later
* The system is modular and can be extended into a full product

This makes the project both simple and realistic, matching InternHub’s requirements.

