import re

def validate_application(data):
    required = ["internship_id", "name", "email", "phone"]
    if any(not str(data.get(field, "")).strip() for field in required):
        return "Please fill in all required fields."
    try:
        int(data["internship_id"])
    except (TypeError, ValueError):
        return "Invalid internship ID."
    email = str(data["email"]).strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return "Please enter a valid email address."
    phone = re.sub(r"[\s+\-()]", "", str(data["phone"]))
    if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
        return "Please enter a valid phone number (10 to 15 digits)."
    resume = str(data.get("resume_link", "")).strip()
    if resume and not (resume.startswith("https://") or resume.startswith("http://") or resume.startswith("/uploads/")):
        return "Resume link must start with http:// or https://."
    if len(str(data.get("cover_note", ""))) > 1000:
        return "Cover note must be 1000 characters or fewer."
    return None
