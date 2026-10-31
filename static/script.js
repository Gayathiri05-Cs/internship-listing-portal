const list = document.getElementById("internshipList");
const params = () => {
  const p = new URLSearchParams();
  const values = {search: "search", location: "location", domain: "domain", work_mode: "workMode", duration: "duration", max_stipend: "stipend"};
  Object.entries(values).forEach(([key, id]) => {
    const value = document.getElementById(id).value.trim();
    if (value) p.set(key, value);
  });
  return p.toString();
};
const money = n => "₹" + Number(n).toLocaleString("en-IN") + " / month";
function card(item) {
  return `<article class="intern-card">
    <div class="card-top"><span class="company-mark">${item.company.charAt(0)}</span><span class="tag">${item.work_mode}</span></div>
    <p class="company">${item.company}</p><h3>${item.title}</h3>
    <div class="meta"><span>⌖ ${item.location}</span><span>◷ ${item.duration}</span></div>
    <div class="card-bottom"><strong>${money(item.stipend)}</strong><a href="/internship/${item.id}" class="detail-link">View details →</a></div>
  </article>`;
}
async function loadInternships() {
  list.innerHTML = '<p class="muted">Loading internships...</p>';
  try {
    const response = await fetch("/api/internships?" + params());
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not load internships.");
    document.getElementById("resultCount").textContent = `${data.length} opportunities found`;
    list.innerHTML = data.length ? data.map(card).join("") : '<div class="empty"><h3>No internships found</h3><p>Try changing or clearing your filters.</p></div>';
  } catch (error) { list.innerHTML = `<p class="error">${error.message}</p>`; }
}
document.getElementById("searchBtn").addEventListener("click", loadInternships);
document.getElementById("clearBtn").addEventListener("click", () => {
  ["search","location","domain","workMode","duration","stipend"].forEach(id => document.getElementById(id).value = "");
  loadInternships();
});
["search","location","domain","workMode","duration","stipend"].forEach(id => {
  document.getElementById(id).addEventListener("change", loadInternships);
});
document.getElementById("search").addEventListener("keydown", e => { if (e.key === "Enter") loadInternships(); });
loadInternships();