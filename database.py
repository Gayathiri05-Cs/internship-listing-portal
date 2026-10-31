import sqlite3
from flask import g

DATABASE = "database/internships.db"

SAMPLE_INTERNSHIPS = [
    ("Frontend Development Intern", "BrightApps Technologies", "Chennai", "Web Development", "Hybrid", "3 months", 10000, "Build responsive web pages using HTML, CSS and JavaScript. Work with a mentor and contribute to real product features.", "2026-12-15"),
    ("Python Developer Intern", "CodeNest Solutions", "Bengaluru", "Software Development", "Remote", "2 months", 8000, "Assist in building Python applications, writing APIs and testing backend features.", "2026-12-20"),
    ("UI/UX Design Intern", "PixelCraft Studio", "Chennai", "Design", "Onsite", "3 months", 7000, "Create wireframes, prototypes and user-friendly interface designs with feedback from the design team.", "2026-12-10"),
    ("Data Analytics Intern", "InsightWorks", "Hyderabad", "Data Science", "Remote", "6 months", 12000, "Work with spreadsheets and Python to clean, explore and visualize sample business datasets.", "2026-12-25"),
    ("Java Backend Intern", "NextGen Systems", "Coimbatore", "Software Development", "Hybrid", "3 months", 9000, "Learn backend development, database integration and REST API development using Java.", "2026-12-18"),
    ("Digital Marketing Intern", "BrandOrbit", "Mumbai", "Marketing", "Remote", "2 months", 5000, "Support content planning, campaign research and basic performance reporting.", "2026-12-22"),
    ("React Developer Intern", "WebSpring Labs", "Pune", "Web Development", "Hybrid", "3 months", 11000, "Develop reusable React components and connect frontend pages to REST APIs.", "2026-12-28"),
    ("Machine Learning Intern", "AI Harbor", "Bengaluru", "Data Science", "Onsite", "6 months", 15000, "Explore datasets, prepare model experiments and document machine learning results.", "2026-12-30"),
    ("Cloud Support Intern", "CloudBridge", "Chennai", "Cloud", "Hybrid", "3 months", 10000, "Assist with cloud deployment basics, monitoring and technical documentation.", "2026-12-12"),
    ("Content Writing Intern", "WriteWell Media", "Remote", "Content", "Remote", "1 month", 4000, "Research topics and write clear articles, product descriptions and short-form content.", "2026-12-08")
]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    import os
    os.makedirs("database", exist_ok=True)
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            domain TEXT NOT NULL,
            work_mode TEXT NOT NULL,
            duration TEXT NOT NULL,
            stipend INTEGER NOT NULL,
            description TEXT NOT NULL,
            deadline TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            internship_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            resume_link TEXT,
            cover_note TEXT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (internship_id) REFERENCES internships(id)
        )
    """)
    count = db.execute("SELECT COUNT(*) FROM internships").fetchone()[0]
    if count == 0:
        db.executemany("""
            INSERT INTO internships
            (title, company, location, domain, work_mode, duration, stipend, description, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, SAMPLE_INTERNSHIPS)
    db.commit()
    db.close()
