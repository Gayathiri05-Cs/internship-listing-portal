const form = document.getElementById("applicationForm");
const message = document.getElementById("formMessage");
fetch(`/api/internships/${INTERNSHIP_ID}`).then(async r => {
  const d = await r.json(); if (!r.ok) throw new Error(d.error);
  document.getElementById("jobTitle").textContent = `${d.title} at ${d.company}`;
}).catch(e => document.getElementById("jobTitle").textContent = e.message);
form.addEventListener("submit", async event => {
  event.preventDefault(); message.textContent = "Submitting..."; message.className = "muted";
  const payload = new FormData();
  payload.append("internship_id", document.getElementById("internshipId").value);
  payload.append("name", document.getElementById("name").value);
  payload.append("email", document.getElementById("email").value);
  payload.append("phone", document.getElementById("phone").value);
  payload.append("resume_link", document.getElementById("resume").value);
  payload.append("cover_note", document.getElementById("cover").value);
  const resumeFile = document.getElementById("resumeFile").files[0];
  if (resumeFile) payload.append("resume_file", resumeFile);
  try {
    const response = await fetch("/api/applications", {method:"POST", body:payload});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not submit application.");
    window.location.href = `/success.html?id=${data.application_id}`;
  } catch (e) { message.textContent = e.message; message.className = "error"; }
});