// CYBER-VAULT Client Controller (Biswajeet Shadangi Edition)
document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const cinematicHud = document.getElementById('cinematic-hud');
  const hudProgressBar = document.getElementById('hud-progress-bar');
  const hudLogLine = document.getElementById('hud-log-line');
  const hudTypingTitle = document.getElementById('hud-typing-title');
  
  const authGate = document.getElementById('auth-gate');
  const dashboardView = document.getElementById('dashboard-view');
  
  // Auth Form Elements
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const loginCard = document.getElementById('login-card-container');
  const registerCard = document.getElementById('register-card-container');
  const showRegisterLink = document.getElementById('show-register-btn');
  const showLoginLink = document.getElementById('show-login-btn');
  const authAlert = document.getElementById('auth-alert');
  const regAlert = document.getElementById('reg-alert');

  // User Header elements
  const activeUsernameEl = document.getElementById('active-username');
  const activeRoleEl = document.getElementById('active-role');
  const logoutBtn = document.getElementById('logout-btn');

  // Quick Demo Buttons
  const btnFastAdmin = document.getElementById('btn-fast-admin');
  const btnFastGuest = document.getElementById('btn-fast-guest');

  // Tabs
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content-panel');

  // OSINT & Dossier Elements
  const btnRescan = document.getElementById('btn-rescan-osint');
  const scanStatusText = document.getElementById('scan-status-text');
  const footprintListContainer = document.getElementById('footprint-list-container');
  const repoGridContainer = document.getElementById('repo-grid-container');
  const sectionsContainer = document.getElementById('sections-container');

  // AI Chat Elements
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send-btn');
  const promptChips = document.querySelectorAll('.prompt-chip');

  // State
  let currentUser = null;
  let dossierData = null;

  // Run Cinematic Intro on start
  runCinematicBootSequence(() => {
    checkAuth();
  });

  // --- CINEMATIC HUD BOOT SEQUENCE ---
  function runCinematicBootSequence(onComplete) {
    const steps = [
      { progress: 20, log: "Mounting dual-isolated database schemas (users_auth.db & dossier_data.db)..." },
      { progress: 45, log: "Verifying subject identity: BISWAJEET SHADANGI (B.Tech CSE 2nd Yr)..." },
      { progress: 70, log: "Loading verified OSINT nodes: LinkedIn, GitHub, Instagram, Direct Telecom (+91 7847881225)..." },
      { progress: 90, log: "Synthesizing YOLOv8 Safety Model & OmniRoute AI telemetry..." },
      { progress: 100, log: "CYBER-VAULT ONLINE // SECURITY PROTOCOLS ENGAGED" }
    ];

    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < steps.length) {
        const s = steps[currentStep];
        if (hudProgressBar) hudProgressBar.style.width = `${s.progress}%`;
        if (hudLogLine) hudLogLine.textContent = s.log;
        currentStep++;
      } else {
        clearInterval(interval);
        setTimeout(() => {
          if (cinematicHud) {
            cinematicHud.style.opacity = '0';
            cinematicHud.style.visibility = 'hidden';
            setTimeout(() => {
              cinematicHud.style.display = 'none';
              if (onComplete) onComplete();
            }, 250);
          } else {
            if (onComplete) onComplete();
          }
        }, 200);
      }
    }, 140);
  }

  // --- AUTH CHECK ---
  async function checkAuth() {
    try {
      const res = await fetch('/api/auth/me');
      if (res.ok) {
        const data = await res.json();
        currentUser = data.user;
        showDashboard();
      } else {
        showAuthGate();
      }
    } catch (err) {
      showAuthGate();
    }
  }

  function showAuthGate() {
    authGate.style.display = 'flex';
    dashboardView.style.display = 'none';
  }

  function showDashboard() {
    authGate.style.display = 'none';
    dashboardView.style.display = 'block';
    if (currentUser) {
      activeUsernameEl.textContent = currentUser.username;
      activeRoleEl.textContent = currentUser.role;
    }
    loadDossierData();
    loadSystemTelemetry();
  }

  // --- AUTH FORMS SWITCHING ---
  if (showRegisterLink) {
    showRegisterLink.addEventListener('click', (e) => {
      e.preventDefault();
      loginCard.style.display = 'none';
      registerCard.style.display = 'block';
    });
  }

  if (showLoginLink) {
    showLoginLink.addEventListener('click', (e) => {
      e.preventDefault();
      registerCard.style.display = 'none';
      loginCard.style.display = 'block';
    });
  }

  // Fast Demo Fill
  if (btnFastAdmin) {
    btnFastAdmin.addEventListener('click', () => {
      document.getElementById('login-username').value = 'biswa';
      document.getElementById('login-password').value = 'Biswa@2026';
    });
  }

  if (btnFastGuest) {
    btnFastGuest.addEventListener('click', () => {
      document.getElementById('login-username').value = 'guest';
      document.getElementById('login-password').value = 'Guest@2026';
    });
  }

  // Submit Login
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      authAlert.style.display = 'none';
      const u = document.getElementById('login-username').value.trim();
      const p = document.getElementById('login-password').value;

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: u, password: p })
        });
        const data = await res.json();

        if (res.ok) {
          currentUser = data.user;
          showDashboard();
        } else {
          authAlert.textContent = data.detail || 'Access Denied: Invalid Credentials';
          authAlert.className = 'alert-box alert-danger';
          authAlert.style.display = 'block';
        }
      } catch (err) {
        authAlert.textContent = 'Server connection failed.';
        authAlert.className = 'alert-box alert-danger';
        authAlert.style.display = 'block';
      }
    });
  }

  // Submit Register
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      regAlert.style.display = 'none';
      const u = document.getElementById('reg-username').value.trim();
      const em = document.getElementById('reg-email').value.trim();
      const p = document.getElementById('reg-password').value;

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: u, email: em, password: p })
        });
        const data = await res.json();

        if (res.ok) {
          regAlert.textContent = 'Account created in Database 1! You can now sign in.';
          regAlert.className = 'alert-box alert-success';
          regAlert.style.display = 'block';
          setTimeout(() => {
            registerCard.style.display = 'none';
            loginCard.style.display = 'block';
            document.getElementById('login-username').value = u;
            document.getElementById('login-password').value = p;
          }, 1400);
        } else {
          regAlert.textContent = data.detail || 'Registration failed.';
          regAlert.className = 'alert-box alert-danger';
          regAlert.style.display = 'block';
        }
      } catch (err) {
        regAlert.textContent = 'Error contacting authentication server.';
        regAlert.className = 'alert-box alert-danger';
        regAlert.style.display = 'block';
      }
    });
  }

  // Logout
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        await fetch('/api/auth/logout', { method: 'POST' });
      } catch (err) {}
      currentUser = null;
      showAuthGate();
    });
  }

  // --- TABS LOGIC ---
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.style.display = 'none');

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.style.display = 'block';
      }
    });
  });

  // --- LOAD DOSSIER DATA ---
  async function loadDossierData() {
    try {
      const res = await fetch('/api/dossier/all');
      if (!res.ok) {
        if (res.status === 401) showAuthGate();
        return;
      }
      const json = await res.json();
      dossierData = json.dossier;
      renderDossierView(dossierData);
    } catch (err) {
      console.error("Dossier load error:", err);
    }
  }

  function renderDossierView(data) {
    if (!data) return;
    const { profile, footprints, repositories, sections } = data;

    // Profile Identity (Guaranteed BISWAJEET SHADANGI)
    if (profile) {
      document.getElementById('hero-fullname').textContent = profile.full_name || 'BISWAJEET SHADANGI';
      document.getElementById('hero-alias').textContent = `@${profile.alias || 'Pshypher-Techie'}`;
      document.getElementById('hero-email').textContent = profile.email || 'biswajeetshadangi98@gmail.com';
      document.getElementById('hero-phone').textContent = profile.phone || '+91 7847881225';
      document.getElementById('hero-location').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${profile.location || 'Koraput, Odisha, India'}`;
      document.getElementById('hero-bio').textContent = profile.bio || '';
      document.getElementById('hero-academic').textContent = `${profile.qualification || 'B.Tech CSE (2nd Yr)'} • ${profile.college || 'VITAM'} / ${profile.university || 'BPUT'}`;
      if (profile.avatar_url) {
        document.getElementById('hero-avatar').src = profile.avatar_url;
      }

      // Update social links
      if (profile.linkedin_url) document.getElementById('link-linkedin').href = profile.linkedin_url;
      if (profile.instagram_url) document.getElementById('link-instagram').href = profile.instagram_url;
      if (profile.twitter_url) document.getElementById('link-twitter').href = profile.twitter_url;
      if (profile.phone) document.getElementById('link-phone').href = `tel:${profile.phone.replace(/\s+/g, '')}`;
    }

    // Counters
    animateCount('counter-repos', repositories ? repositories.length : 0);
    animateCount('counter-footprints', footprints ? footprints.length : 0);
    animateCount('counter-confidence', 100, '%');

    // Footprints
    if (footprints && footprintListContainer) {
      footprintListContainer.innerHTML = '';
      footprints.forEach(fp => {
        const item = document.createElement('div');
        item.className = 'footprint-item';
        item.innerHTML = `
          <div class="footprint-left">
            <div class="footprint-icon">
              <i class="fas fa-satellite-dish"></i>
            </div>
            <div>
              <div class="footprint-title">${escapeHtml(fp.platform)} <span class="meta-tag" style="padding: 2px 8px; font-size: 10px;">${escapeHtml(fp.category || 'OSINT')}</span></div>
              <div class="footprint-desc">${escapeHtml(fp.summary || '')}</div>
              <div style="font-family: var(--font-mono); font-size: 11px; color: var(--teal-accent); margin-top: 4px;">
                <a href="${escapeHtml(fp.url)}" target="_blank" style="color: var(--teal-primary); text-decoration: none;">
                  <i class="fas fa-external-link-alt"></i> ${escapeHtml(fp.identifier)}
                </a>
              </div>
            </div>
          </div>
          <div style="text-align: right; min-width: 100px;">
            <div style="font-size: 12px; font-weight: 700; color: #34d399;">
              <i class="fas fa-check-circle"></i> ${fp.verified ? 'VERIFIED' : 'INDEXED'}
            </div>
            <div class="confidence-bar">
              <div class="confidence-fill" style="width: ${fp.confidence}%;"></div>
            </div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 4px; font-family: var(--font-mono);">${fp.confidence}% Match</div>
          </div>
        `;
        footprintListContainer.appendChild(item);
      });
    }

    // 7 Sections Render (tab-sections)
    if (sections && sectionsContainer) {
      sectionsContainer.innerHTML = '';
      sections.forEach(sec => {
        const card = document.createElement('div');
        card.className = 'topic-card';

        let innerHTML = `
          <div class="topic-header">
            <i class="fas ${sec.icon}"></i>
            <span>${escapeHtml(sec.title)}</span>
          </div>
        `;

        const c = sec.content;
        if (sec.section_key === 'qualifications') {
          innerHTML += `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; font-family: var(--font-mono); font-size: 13px;">
              <div style="background: rgba(3,10,13,0.7); padding: 14px; border-radius: 8px; border-left: 3px solid var(--teal-primary);">
                <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">Degree & Year</div>
                <strong style="color: #fff; font-size: 15px;">${escapeHtml(c.degree)}</strong>
                <div style="color: var(--teal-accent);">${escapeHtml(c.year_status)}</div>
              </div>
              <div style="background: rgba(3,10,13,0.7); padding: 14px; border-radius: 8px; border-left: 3px solid var(--emerald-accent);">
                <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">College & Affiliation</div>
                <strong style="color: #fff; font-size: 14px;">${escapeHtml(c.institution)}</strong>
                <div style="color: #94a3b8;">${escapeHtml(c.affiliation)}</div>
              </div>
            </div>
          `;
        } else if (sec.section_key === 'contacts') {
          innerHTML += `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; font-family: var(--font-mono); font-size: 13px;">
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: var(--teal-primary);"><i class="fas fa-phone"></i> Phone:</span> <a href="tel:${c.phone}" style="color: #fff; text-decoration: none;">${c.phone}</a>
              </div>
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: var(--teal-secondary);"><i class="fas fa-envelope"></i> Email:</span> <a href="mailto:${c.email}" style="color: #fff; text-decoration: none;">${c.email}</a>
              </div>
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: var(--emerald-accent);"><i class="fas fa-map-marker-alt"></i> Location:</span> ${c.location}
              </div>
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: #0077b5;"><i class="fab fa-linkedin"></i> LinkedIn:</span> <a href="${c.linkedin}" target="_blank" style="color: var(--teal-primary);">Profile &rarr;</a>
              </div>
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: #e1306c;"><i class="fab fa-instagram"></i> Instagram:</span> <a href="${c.instagram}" target="_blank" style="color: var(--teal-primary);">@_pshypher_12_ &rarr;</a>
              </div>
              <div style="background: rgba(3,10,13,0.6); padding: 10px; border-radius: 6px;">
                <span style="color: #fff;"><i class="fab fa-x-twitter"></i> X / Twitter:</span> <a href="${c.twitter}" target="_blank" style="color: var(--teal-primary);">@BISWAJEET140222 &rarr;</a>
              </div>
            </div>
          `;
        } else if (sec.section_key === 'skills') {
          innerHTML += `
            <div style="margin-bottom: 12px; font-family: var(--font-mono); font-size: 13px; color: var(--teal-primary);">
              <i class="fas fa-location-arrow"></i> Origin Base: <strong>${escapeHtml(c.comes_from)}</strong>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px;">
              ${c.core_skills.map(s => `<span class="meta-tag"><i class="fas fa-check"></i> ${escapeHtml(s)}</span>`).join('')}
            </div>
            <div style="font-size: 12px; color: #94a3b8; font-family: var(--font-mono);">
              <strong>Core Languages:</strong> ${c.languages.join(' &bull; ')}
            </div>
          `;
        } else if (sec.section_key === 'awards') {
          innerHTML += `
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 13px; color: #cbd5e1;">
              ${c.highlights.map(h => `<li><i class="fas fa-star" style="color: #fbbf24; margin-right: 8px;"></i>${escapeHtml(h)}</li>`).join('')}
            </ul>
          `;
        } else if (sec.section_key === 'fields_of_interest') {
          innerHTML += `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
              ${c.interests.map(item => `
                <div style="background: rgba(3,10,13,0.6); padding: 14px; border-radius: 8px; border-left: 2px solid var(--teal-primary);">
                  <div style="color: #fff; font-weight: 700; font-size: 14px; margin-bottom: 4px;">${escapeHtml(item.title)}</div>
                  <div style="font-size: 12px; color: #94a3b8;">${escapeHtml(item.desc)}</div>
                </div>
              `).join('')}
            </div>
          `;
        } else if (sec.section_key === 'personal_about') {
          innerHTML += `
            <p style="font-size: 14px; color: #cbd5e1; line-height: 1.6; margin-bottom: 12px;">${escapeHtml(c.origin_roots)}</p>
            <blockquote style="border-left: 3px solid var(--teal-primary); padding-left: 12px; color: var(--teal-primary); font-style: italic; margin-bottom: 14px; font-size: 13px;">
              "${escapeHtml(c.motto)}"
            </blockquote>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
              ${c.hobbies.map(hob => `<span class="meta-tag" style="font-size: 11px;"><i class="fas fa-heart" style="color: #f43f5e;"></i> ${escapeHtml(hob)}</span>`).join('')}
            </div>
          `;
        } else if (sec.section_key === 'internships') {
          innerHTML += `
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${c.projects_experience.map(exp => `
                <div style="background: rgba(3,10,13,0.6); padding: 14px; border-radius: 8px; border-left: 3px solid var(--emerald-accent);">
                  <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                    <strong style="color: #fff; font-size: 14px;">${escapeHtml(exp.role)}</strong>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--emerald-accent);">${escapeHtml(exp.period)}</span>
                  </div>
                  <div style="color: var(--teal-accent); font-size: 12px; margin-bottom: 6px;">${escapeHtml(exp.org)}</div>
                  <div style="color: #94a3b8; font-size: 12px;">${escapeHtml(exp.desc)}</div>
                </div>
              `).join('')}
            </div>
          `;
        }

        card.innerHTML = innerHTML;
        sectionsContainer.appendChild(card);
      });
    }

    // Repositories Grid Render
    if (repositories && repoGridContainer) {
      repoGridContainer.innerHTML = '';
      repositories.forEach(r => {
        const card = document.createElement('div');
        card.className = 'repo-card';
        card.innerHTML = `
          <div>
            <div class="repo-title">
              <span><i class="fas fa-code-branch" style="color: var(--teal-primary); margin-right: 6px;"></i>${escapeHtml(r.name)}</span>
              ${r.is_fork ? '<span class="meta-tag" style="font-size: 10px; padding: 2px 6px;">FORK/CONTRIB</span>' : '<span class="meta-tag" style="font-size: 10px; padding: 2px 6px;">AUTHOR</span>'}
            </div>
            <p class="repo-desc">${escapeHtml(r.description || 'Open-source software component.')}</p>
          </div>
          <div>
            <div style="margin-bottom: 12px; font-size: 11px; color: var(--teal-muted); background: rgba(0,245,212,0.06); padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(0,245,212,0.15);">
              <i class="fas fa-microchip" style="margin-right: 4px;"></i>${escapeHtml(r.ai_summary || 'Analyzed code asset')}
            </div>
            <div class="repo-footer">
              <span><i class="fas fa-code"></i> ${escapeHtml(r.language || 'Multi')}</span>
              <span><i class="fas fa-star" style="color: #fbbf24;"></i> ${r.stars || 0}</span>
              <a href="${escapeHtml(r.url)}" target="_blank" class="btn-cyber" style="padding: 4px 10px; font-size: 11px;">
                Inspect <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>
        `;
        repoGridContainer.appendChild(card);
      });
    }
  }

  // --- RUN LIVE OSINT RESCAN ---
  if (btnRescan) {
    btnRescan.addEventListener('click', async () => {
      btnRescan.disabled = true;
      btnRescan.innerHTML = '<i class="fas fa-sync fa-spin"></i> Live Scanning Internet...';
      scanStatusText.textContent = 'Contacting GitHub API & OSINT federations...';

      try {
        const res = await fetch('/api/dossier/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ handle: 'Pshypher-Techie' })
        });
        const result = await res.json();
        if (res.ok) {
          scanStatusText.textContent = `Completed at ${new Date().toLocaleTimeString()}! Refreshed ${result.result.github.repositories_found} repos.`;
          renderDossierView(result.refreshed_data);
          loadSystemTelemetry();
        } else {
          scanStatusText.textContent = 'Scan failed: ' + (result.detail || 'Error');
        }
      } catch (err) {
        scanStatusText.textContent = 'Network error during rescan.';
      } finally {
        btnRescan.disabled = false;
        btnRescan.innerHTML = '<i class="fas fa-satellite"></i> Trigger Live Internet Rescan';
      }
    });
  }

  // --- LOAD SYSTEM TELEMETRY (DUAL DATABASES) ---
  async function loadSystemTelemetry() {
    try {
      const res = await fetch('/api/system/stats');
      if (!res.ok) return;
      const data = await res.json();

      document.getElementById('db1-users-count').textContent = data.databases.database_1.stats.total_registered_users;
      document.getElementById('db1-audits-count').textContent = data.databases.database_1.stats.total_audit_events;
      
      document.getElementById('db2-repos-count').textContent = data.databases.database_2.stats.total_repositories;
      document.getElementById('db2-verified-count').textContent = data.databases.database_2.stats.verified_footprint_sources;
      document.getElementById('db2-facts-count').textContent = data.databases.database_2.stats.ai_knowledge_facts;

      const auditTableBody = document.getElementById('audit-table-body');
      if (auditTableBody && data.audit_feed) {
        auditTableBody.innerHTML = '';
        data.audit_feed.forEach(log => {
          const tr = document.createElement('tr');
          let badgeClass = 'action-badge action-view';
          if (log.action.includes('LOGIN')) badgeClass = 'action-badge action-login';
          if (log.action.includes('FAIL')) badgeClass = 'action-badge action-fail';
          if (log.action.includes('AI')) badgeClass = 'action-badge action-query';

          tr.innerHTML = `
            <td><span class="${badgeClass}">${escapeHtml(log.action)}</span></td>
            <td><strong>${escapeHtml(log.username || 'Anonymous')}</strong></td>
            <td>${escapeHtml(log.details || '-')}</td>
            <td style="color: var(--teal-muted);">${escapeHtml(log.ip_address || '127.0.0.1')}</td>
            <td style="color: #64748b; font-size: 11px;">${new Date(log.timestamp).toLocaleTimeString()}</td>
          `;
          auditTableBody.appendChild(tr);
        });
      }
    } catch (err) {
      console.error("Telemetry error:", err);
    }
  }

  // --- AI INTELLIGENCE CHAT ---
  async function sendAiMessage(query) {
    if (!query || !query.trim()) return;
    const cleanQ = query.trim();

    appendChatMessage('user', cleanQ);
    chatInput.value = '';
    chatInput.focus();

    const thinkingBubble = appendChatMessage('ai', '<i class="fas fa-circle-notch fa-spin"></i> Consulting BISWAJEET SHADANGI Intelligence Dossier...');

    try {
      const res = await fetch('/api/ai/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: cleanQ })
      });
      const json = await res.json();

      if (res.ok && json.success) {
        const formatted = formatMarkdown(json.data.response);
        thinkingBubble.innerHTML = formatted;
        loadSystemTelemetry();
      } else {
        thinkingBubble.innerHTML = `<span style="color: #fca5a5;">${escapeHtml(json.detail || 'AI query error')}</span>`;
      }
    } catch (err) {
      thinkingBubble.innerHTML = '<span style="color: #fca5a5;">Failed to reach AI Engine.</span>';
    }
  }

  function appendChatMessage(sender, htmlContent) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.innerHTML = htmlContent;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return bubble;
  }

  if (chatSendBtn) {
    chatSendBtn.addEventListener('click', () => sendAiMessage(chatInput.value));
  }

  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendAiMessage(chatInput.value);
      }
    });
  }

  promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const q = chip.getAttribute('data-prompt');
      if (q) sendAiMessage(q);
    });
  });

  // --- HELPER UTILITIES ---
  function animateCount(elementId, targetValue, suffix = '') {
    const el = document.getElementById(elementId);
    if (!el) return;
    let current = 0;
    const duration = 1200;
    const stepTime = 30;
    const steps = duration / stepTime;
    const increment = targetValue / steps;

    const timer = setInterval(() => {
      current += increment;
      if (current >= targetValue) {
        current = targetValue;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current) + suffix;
    }, stepTime);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatMarkdown(text) {
    if (!text) return '';
    let parsed = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/`(.*?)`/g, '<code style="background: rgba(0,245,212,0.1); color: var(--teal-primary); padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color: var(--teal-primary); text-decoration: underline;">$1</a>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/• /g, '&bull; ');
    return parsed;
  }
});
