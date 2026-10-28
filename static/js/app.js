// CYBER-VAULT Client Controller
document.addEventListener('DOMContentLoaded', () => {
  // Elements
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

  // AI Chat Elements
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send-btn');
  const promptChips = document.querySelectorAll('.prompt-chip');

  // State
  let currentUser = null;
  let dossierData = null;

  // Initialize
  checkAuth();

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
    const { profile, footprints, repositories } = data;

    // Profile Identity
    if (profile) {
      document.getElementById('hero-fullname').textContent = profile.full_name || 'Biswajeet Shadangi';
      document.getElementById('hero-alias').textContent = `@${profile.alias || 'Pshypher-Techie'}`;
      document.getElementById('hero-email').textContent = profile.email || 'biswajeetshadangi98@gmail.com';
      document.getElementById('hero-location').textContent = profile.location || 'Odisha, India';
      document.getElementById('hero-headline').textContent = profile.headline || 'AI & Computer Vision Engineer';
      document.getElementById('hero-bio').textContent = profile.bio || '';
      document.getElementById('hero-academic').textContent = profile.academic_background || 'BPUT Technical Programs';
      if (profile.avatar_url) {
        document.getElementById('hero-avatar').src = profile.avatar_url;
      }
    }

    // Numbers & Telemetry Counters
    animateCount('counter-repos', repositories ? repositories.length : 0);
    animateCount('counter-footprints', footprints ? footprints.length : 0);
    animateCount('counter-confidence', 99, '%');
    
    // Footprint List Render
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

      // Database 1 Metrics
      document.getElementById('db1-users-count').textContent = data.databases.database_1.stats.total_registered_users;
      document.getElementById('db1-audits-count').textContent = data.databases.database_1.stats.total_audit_events;
      
      // Database 2 Metrics
      document.getElementById('db2-repos-count').textContent = data.databases.database_2.stats.total_repositories;
      document.getElementById('db2-verified-count').textContent = data.databases.database_2.stats.verified_footprint_sources;
      document.getElementById('db2-facts-count').textContent = data.databases.database_2.stats.ai_knowledge_facts;

      // Audit Logs Table
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

    // Append User Bubble
    appendChatMessage('user', cleanQ);
    chatInput.value = '';
    chatInput.focus();

    // Append Thinking AI bubble
    const thinkingBubble = appendChatMessage('ai', '<i class="fas fa-circle-notch fa-spin"></i> Consulting Biswajeet Intelligence Dossier...');

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

