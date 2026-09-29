let a=null,i="experience";const o=document.getElementById("app"),s=document.getElementById("saveBtn");async function c(){try{a=await(await fetch("/api/portfolio")).json(),l()}catch(e){o.innerHTML=`<div class="error">Error loading data: ${e.message}</div>`}}async function d(){if(a){s.textContent="Saving...";try{(await fetch("/api/portfolio",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(a)})).ok?alert("Saved successfully!"):alert("Error saving data")}catch{alert("Error saving data")}finally{s.textContent="Save Changes"}}}function l(){a&&(o.innerHTML=`
        <div class="admin-grid">
           <nav class="sidebar">
              <button class="${i==="profile"?"active":""}" onclick="switchTab('profile')">Profile & Vision</button>
              <button class="${i==="experience"?"active":""}" onclick="switchTab('experience')">Experience</button>
              <button class="${i==="skills"?"active":""}" onclick="switchTab('skills')">Skills & Categories</button>
           </nav>
           <div class="content-area">
              ${p()}
           </div>
        </div>
      `)}function p(){if(i==="profile")return u();if(i==="experience")return v();if(i==="skills")return g()}function u(){return`
        <div class="card">
          <h2>Profile & Vision</h2>
          <div class="form-group">
            <label>Full Name</label>
            <input type="text" value="${a.profile.name}" onchange="updateProfile('name', this.value)">
          </div>
          <div class="form-group">
            <label>Title</label>
            <input type="text" value="${a.profile.title}" onchange="updateProfile('title', this.value)">
          </div>
          <div class="form-group">
            <label>Professional Vision</label>
            <textarea rows="4" onchange="updateProfile('vision', this.value)">${a.profile.vision}</textarea>
            <button class="ai-btn" onclick="alert('AI Integration coming soon!')">✨ Ask AI to improve</button>
          </div>
        </div>
      `}function v(){return`
        <div class="card">
          <div class="flex-between">
            <h2>Experience</h2>
            <button class="btn-small" onclick="addExperience()">+ Add Role</button>
          </div>
          <div class="list">
            ${a.experience.map((e,t)=>`
              <div class="list-item">
                <div class="item-header">
                   <strong>${e.company}</strong> - ${e.title}
                   <button class="btn-danger" onclick="deleteExperience(${t})">Delete</button>
                </div>
                <div class="form-grid">
                   <label>Company: <input value="${e.company}" onchange="updateExp(${t}, 'company', this.value)"></label>
                   <label>Title: <input value="${e.title}" onchange="updateExp(${t}, 'title', this.value)"></label>
                   <label>Start: <input value="${e.dateStart}" onchange="updateExp(${t}, 'dateStart', this.value)"></label>
                   <label>End: <input value="${e.dateEnd}" onchange="updateExp(${t}, 'dateEnd', this.value)"></label>
                </div>
                <details>
                  <summary>Details & Tags</summary>
                  <div class="form-group">
                     <label>Description</label>
                     <textarea rows="2" onchange="updateExp(${t}, 'description', this.value)">${e.description}</textarea>
                  </div>
                  <div class="form-group">
                     <label>Tags (comma separated)</label>
                     <input value="${e.tags?.join(", ")}" onchange="updateExpTags(${t}, 'tags', this.value)">
                  </div>
                  <div class="form-group">
                     <label><input type="checkbox" ${e.highlight?"checked":""} onchange="updateExp(${t}, 'highlight', this.checked)"> Featured (flagged role)</label>
                  </div>
                </details>
              </div>
            `).join("")}
          </div>
        </div>
      `}function g(){return'<div class="card"><h2>Skills Management (Coming Soon)</h2><p>Here you will be able to drag-and-drop skills and edit categories.</p></div>'}window.switchTab=e=>{i=e,l()};window.updateProfile=(e,t)=>{a.profile[e]=t};window.updateExp=(e,t,n)=>{a.experience[e][t]=n};window.updateExpTags=(e,t,n)=>{a.experience[e][t]=n.split(",").map(r=>r.trim()).filter(r=>r)};window.addExperience=()=>{a.experience.unshift({id:"new-"+Date.now(),company:"New Company",title:"New Role",dateStart:"Jan 2024",dateEnd:"Present",tags:[],details:[]}),l(),alert("New role added! Soft skills regeneration logic to be triggered.")};window.deleteExperience=e=>{confirm("Delete this role?")&&(a.experience.splice(e,1),l())};c();s.onclick=d;
