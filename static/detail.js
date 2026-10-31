const root = document.getElementById("detail");
fetch(`/api/internships/${INTERNSHIP_ID}`).then(async r => {
  const data = await r.json(); if (!r.ok) throw new Error(data.error);
  document.title = `${data.title} | InternConnect`;
  root.innerHTML = `<span class="tag">${data.domain}</span><p class="company">${data.company}</p><h1>${data.title}</h1>
  <div class="detail-meta"><span>⌖ ${data.location}</span><span>${data.work_mode}</span><span>${data.duration}</span></div>
  <h3>About this internship</h3><p class="description">${data.description}</p>
  <div class="detail-facts"><div><small>Monthly stipend</small><strong>₹${Number(data.stipend).toLocaleString("en-IN")}</strong></div><div><small>Application deadline</small><strong>${data.deadline}</strong></div></div>
  <a class="primary-btn button-link" href="/apply/${data.id}">Apply Now</a>`;
}).catch(e => root.innerHTML = `<p class="error">${e.message}</p>`);