# CYBER-VAULT // AI-Powered Personal Intelligence Dossier

> A secure, AI-powered digital intelligence platform and portfolio dashboard in a bluish-green cyber aesthetic, displaying public internet footprint, verified engineering artifacts, and grounded AI assistant interactions.

---

## 🌐 Live URLs

- **Public Live HTTPS URL**: [https://murray-wto-pct-cassette.trycloudflare.com](https://murray-wto-pct-cassette.trycloudflare.com)
- **Local Development URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔑 Login Credentials

All personal details, code repositories, and AI chat endpoints are strictly guarded behind a cryptographic gate. Access is only granted after authenticating:

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Admin** | `biswa` | `Biswa@2026` | Full Access + System Telemetry + Live Rescan |
| **Demo Viewer** | `guest` | `Guest@2026` | Viewer Access to Dossier & AI Assistant |

*Visitors can also register their own new viewer accounts directly on the login screen.*

---

## 🛡️ Strict Dual-Database Architecture

In compliance with strict data segregation requirements, viewer/user information is stored in a **physically separate database** from the personal dossier records:

1. **Database 1: `data/users_auth.db` (User Security & Auditing)**
   - `users`: User accounts, emails, PBKDF2 HMAC-SHA256 password hashes, unique salts, and roles.
   - `sessions`: Cryptographic JWT bearer tokens, client IPs, user-agents, and expiration timestamps.
   - `audit_logs`: Immutable security audit trail recording logins, failed attempts, dossier queries, and AI interactions.

2. **Database 2: `data/dossier_data.db` (Internet Dossier & AI Knowledge Base)**
   - `profile_info`: Verified identity (Biswajeet Shadangi, alias: `Pshypher-Techie`, email: `biswajeetshadangi98@gmail.com`).
   - `footprint_sources`: Verified internet footprint (GitHub, Gravatar, BPUT Academic Records, YOLOv8 vision AI, OmniRoute).
   - `repositories`: Live synchronized public repos (`OmniRoute`, `safety-gear-compliance-detector`, `safety-gear-detection-ai`, `worker-safety-ai`, `todo-list-app`).
   - `ai_knowledge`: Contextual RAG knowledge base powering the AI assistant.
   - `scan_logs`: Automated OSINT rescan history and diffs.

---

## 🎨 Theme & Aesthetic: Cyber Bluish-Green

- **Palette**:
  - Primary Neon Aquamarine: `#00f5d4`
  - Electric Cyan: `#06b6d4`
  - Deep Teal: `#14b8a6`
  - Vivid Emerald: `#10b981`
  - Dark Slate Cyber Navy: `#050d10`, `#0a1a20`
- **Animations**:
  - Interactive HTML5 canvas particle constellation responding to mouse repulsion.
  - Pulsing radar scanner with target detection blips.
  - Number increment counting animations for metrics.
  - Glassmorphism frosted panels with 1px luminous neon borders.
  - Streaming AI response feedback.

---

## 🚀 One-Click Launch

To restart the application locally and live at any time:
- **Live Internet**: Double-click `start_live.bat`
- **Local Only**: Double-click `start_local.bat`

