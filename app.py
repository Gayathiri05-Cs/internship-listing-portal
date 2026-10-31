import os
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from database import init_db, get_db
from validators import validate_application

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB upload limit
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)

with app.app_context():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/internship/<int:internship_id>")
def internship_detail_page(internship_id):
    return render_template("detail.html", internship_id=internship_id)

@app.route("/success.html")
def success_page():
    return render_template("success.html")

@app.route("/apply/<int:internship_id>")
def apply_page(internship_id):
    return render_template("apply.html", internship_id=internship_id)

@app.get("/api/internships")
def get_internships():
    search = request.args.get("search", "").strip()
    location = request.args.get("location", "").strip()
    domain = request.args.get("domain", "").strip()
    work_mode = request.args.get("work_mode", "").strip()
    duration = request.args.get("duration", "").strip()
    max_stipend = request.args.get("max_stipend", "").strip()

    query = "SELECT * FROM internships WHERE 1=1"
    params = []

    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(company) LIKE ? OR LOWER(domain) LIKE ?)"
        term = f"%{search.lower()}%"
        params.extend([term, term, term])
    if location:
        query += " AND LOWER(location) LIKE ?"
        params.append(f"%{location.lower()}%")
    if domain:
        query += " AND LOWER(domain) = ?"
        params.append(domain.lower())
    if work_mode:
        query += " AND LOWER(work_mode) = ?"
        params.append(work_mode.lower())
    if duration:
        query += " AND duration = ?"
        params.append(duration)
    if max_stipend:
        try:
            query += " AND stipend <= ?"
            params.append(int(max_stipend))
        except ValueError:
            return jsonify({"error": "Maximum stipend must be a number."}), 400

    query += " ORDER BY id DESC"
    db = get_db()
    rows = db.execute(query, params).fetchall()
    return jsonify([dict(row) for row in rows])

@app.get("/api/internships/<int:internship_id>")
def get_internship(internship_id):
    row = get_db().execute(
        "SELECT * FROM internships WHERE id = ?", (internship_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Internship not found"}), 404
    return jsonify(dict(row))

@app.post("/api/applications")
def create_application():
    data = request.get_json(silent=True) or request.form.to_dict()
    uploaded_file = request.files.get("resume_file")
    if uploaded_file and uploaded_file.filename:
        allowed_extensions = {"pdf", "doc", "docx"}
        extension = uploaded_file.filename.rsplit(".", 1)[-1].lower() if "." in uploaded_file.filename else ""
        if extension not in allowed_extensions:
            return jsonify({"error": "Resume must be a PDF, DOC or DOCX file."}), 400
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        safe_name = secure_filename(uploaded_file.filename)
        stored_name = f"{data.get('internship_id', 'application')}_{safe_name}"
        uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], stored_name))
        data["resume_link"] = f"/uploads/{stored_name}"
    error = validate_application(data)
    if error:
        return jsonify({"error": error}), 400

    db = get_db()
    internship = db.execute(
        "SELECT id FROM internships WHERE id = ?", (data.get("internship_id"),)
    ).fetchone()
    if internship is None:
        return jsonify({"error": "Internship not found"}), 404

    duplicate = db.execute(
        "SELECT id FROM applications WHERE internship_id = ? AND LOWER(email) = LOWER(?)",
        (data["internship_id"], data["email"].strip())
    ).fetchone()
    if duplicate:
        return jsonify({"error": "You have already applied to this internship using this email."}), 409

    cursor = db.execute("""
        INSERT INTO applications
        (internship_id, name, email, phone, resume_link, cover_note)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(data["internship_id"]), data["name"].strip(), data["email"].strip(),
        data["phone"].strip(), data.get("resume_link", "").strip(),
        data.get("cover_note", "").strip()
    ))
    db.commit()
    return jsonify({
        "message": "Application submitted successfully!",
        "application_id": cursor.lastrowid
    }), 201

@app.get("/api/applications")
def list_applications():
    """Development/testing endpoint. In production, protect this endpoint with admin login."""
    rows = get_db().execute("""
        SELECT applications.*, internships.title AS internship_title
        FROM applications
        JOIN internships ON internships.id = applications.internship_id
        ORDER BY applications.id DESC
    """).fetchall()
    return jsonify([dict(row) for row in rows])

@app.get("/uploads/<path:filename>")
def uploaded_resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
