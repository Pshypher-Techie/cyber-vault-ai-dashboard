import sqlite3
import json
from datetime import datetime, timezone
from app.config import (
    DOSSIER_DB_PATH, SUBJECT_NAME, SUBJECT_HANDLE, SUBJECT_EMAIL,
    SUBJECT_PHONE, SUBJECT_LOCATION, SUBJECT_COLLEGE, SUBJECT_UNIVERSITY,
    SUBJECT_QUALIFICATION, LINKEDIN_URL, INSTAGRAM_URL, TWITTER_URL, GITHUB_URL
)

def get_dossier_db_connection():
    conn = sqlite3.connect(DOSSIER_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_dossier_db():
    conn = get_dossier_db_connection()
    cursor = conn.cursor()

    # Table 1: Core Profile Info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        alias TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        location TEXT,
        headline TEXT,
        bio TEXT,
        specialization TEXT,
        academic_background TEXT,
        qualification TEXT,
        college TEXT,
        university TEXT,
        origin TEXT,
        linkedin_url TEXT,
        instagram_url TEXT,
        twitter_url TEXT,
        github_url TEXT,
        avatar_url TEXT,
        updated_at TEXT NOT NULL
    )
    """)

    # Check and add new columns if upgrading existing table
    cursor.execute("PRAGMA table_info(profile_info)")
    columns = [row[1] for row in cursor.fetchall()]
    new_cols = {
        "phone": "TEXT",
        "qualification": "TEXT",
        "college": "TEXT",
        "university": "TEXT",
        "origin": "TEXT",
        "linkedin_url": "TEXT",
        "instagram_url": "TEXT",
        "twitter_url": "TEXT",
        "github_url": "TEXT"
    }
    for col, col_type in new_cols.items():
        if col not in columns:
            cursor.execute(f"ALTER TABLE profile_info ADD COLUMN {col} {col_type}")

    # Table 2: Online Footprint Sources & OSINT Evidence
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS footprint_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        identifier TEXT NOT NULL,
        url TEXT,
        verified INTEGER DEFAULT 0,
        confidence INTEGER DEFAULT 0,
        category TEXT,
        summary TEXT,
        last_checked TEXT NOT NULL
    )
    """)

    # Table 3: Repositories & Engineering Artifacts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        url TEXT NOT NULL,
        language TEXT,
        stars INTEGER DEFAULT 0,
        is_fork INTEGER DEFAULT 0,
        updated_at TEXT,
        ai_summary TEXT
    )
    """)

    # Table 4: Section Details (Qualifications, Skills, Awards, Fields of Interest, Internships, Personal Abouts)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dossier_sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_key TEXT NOT NULL,
        title TEXT NOT NULL,
        icon TEXT NOT NULL,
        content_json TEXT NOT NULL,
        order_index INTEGER DEFAULT 0
    )
    """)

    # Table 5: AI Dossier Knowledge Base & Intelligence Facts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        fact_content TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)

    # Table 6: Scan logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_time TEXT NOT NULL,
        status TEXT NOT NULL,
        sources_found INTEGER NOT NULL,
        details TEXT
    )
    """)
    conn.commit()

    # Re-seed or update core Profile to guarantee exact details
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("DELETE FROM profile_info")
    cursor.execute("""
    INSERT INTO profile_info (
        full_name, alias, email, phone, location, origin,
        headline, bio, specialization, academic_background,
        qualification, college, university,
        linkedin_url, instagram_url, twitter_url, github_url,
        avatar_url, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        SUBJECT_NAME,
        SUBJECT_HANDLE,
        SUBJECT_EMAIL,
        SUBJECT_PHONE,
        SUBJECT_LOCATION,
        "Koraput, Odisha, India",
        "AI & Computer Vision Engineer | YOLOv8 Safety Systems Specialist | Open-Source AI Gateway Contributor",
        "Enthusiastic 2nd-year B.Tech CSE engineer from Koraput, Odisha, studying at VITAM under BPUT. Passionate about real-time Computer Vision (YOLOv8 industrial safety gear detection), deep neural networks, and scalable AI gateways.",
        "Computer Vision, Deep Learning (YOLOv8/PyTorch), Multi-Provider AI Gateways, Python Engineering, Worker Safety Automation",
        "B.Tech in Computer Science & Engineering (2nd Year) at VITAM under BPUT Odisha",
        SUBJECT_QUALIFICATION,
        SUBJECT_COLLEGE,
        SUBJECT_UNIVERSITY,
        LINKEDIN_URL,
        INSTAGRAM_URL,
        TWITTER_URL,
        GITHUB_URL,
        "https://avatars.githubusercontent.com/u/328466102?v=4",
        now
    ))

    # Update or insert Verified Footprint Sources
    cursor.execute("DELETE FROM footprint_sources")
    footprint_items = [
        ("LinkedIn Official", "biswajeet-shadangi-701590447", LINKEDIN_URL, 1, 100, "Professional Network", "Official LinkedIn profile: Engineering student at VITAM, BPUT", now),
        ("GitHub Core Profile", "Pshypher-Techie", GITHUB_URL, 1, 100, "Code Intelligence", "Primary GitHub identity hosting computer vision models and AI gateway repos", now),
        ("Instagram Social", "@_pshypher_12_", INSTAGRAM_URL, 1, 98, "Social Verification", "Verified Instagram identity connected to Pshypher moniker", now),
        ("X / Twitter", "@BISWAJEET140222", TWITTER_URL, 1, 98, "Social & Tech Intel", "Official X account for technical and industry discussions", now),
        ("Direct Telephony & Signal", "+91 7847881225", "tel:+917847881225", 1, 100, "Contact Telemetry", "Direct telecommunications verified line (Koraput, Odisha)", now),
        ("Academic Verification", "VITAM // BPUT Odisha", "https://www.bput.ac.in", 1, 95, "Academic Credential", "Registered B.Tech CSE (2nd Year) student at VITAM, BPUT", now),
        ("Industrial Vision AI", "safety-gear-compliance-detector", "https://github.com/Pshypher-Techie/safety-gear-compliance-detector", 1, 99, "Computer Vision", "YOLOv8 deep learning prototype for electrical hazard & PPE worker compliance", now),
        ("AI Inference Gateway", "OmniRoute Contributor", "https://github.com/Pshypher-Techie/OmniRoute", 1, 95, "Open-Source AI", "Active fork & testing of universal multi-provider (375+ LLMs) gateway", now)
    ]
    cursor.executemany("""
    INSERT INTO footprint_sources (platform, identifier, url, verified, confidence, category, summary, last_checked)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, footprint_items)

    # Populate 7 Dedicated Dossier Sections
    cursor.execute("DELETE FROM dossier_sections")
    sections = [
        ("qualifications", "1. Qualifications & Academic Pedigree", "fa-graduation-cap", json.dumps({
            "degree": "B.Tech in Computer Science & Engineering (CSE)",
            "year_status": "2nd Year (Sophomore)",
            "institution": "Vignan Institute of Technology and Management (VITAM), Berhampur",
            "affiliation": "Biju Patnaik University of Technology (BPUT), Odisha",
            "curriculum_focus": ["Data Structures & Algorithms", "Object-Oriented Programming (Python, C++)", "Database Management Systems", "Artificial Intelligence & Vision"]
        }), 1),
        ("contacts", "2. Verified Direct Contacts & Social Matrix", "fa-address-book", json.dumps({
            "phone": "+91 7847881225",
            "email": "biswajeetshadangi98@gmail.com",
            "location": "Koraput, Odisha, India",
            "linkedin": LINKEDIN_URL,
            "instagram": INSTAGRAM_URL,
            "twitter": TWITTER_URL,
            "github": GITHUB_URL
        }), 2),
        ("skills", "3. Technical Competencies & Origins", "fa-microchip", json.dumps({
            "comes_from": "Koraput, Odisha, India",
            "core_skills": ["Computer Vision (YOLOv8, OpenCV, Image Segmentation)", "Deep Learning (PyTorch, Object Detection, Transfer Learning)", "Python Full-Stack (FastAPI, Flask, AsyncIO)", "AI Gateway Architecture & Multi-Model Inference (OmniRoute)", "Relational Databases & Architecture (Dual-Database SQLite, PostgreSQL)"],
            "languages": ["Python", "C++", "JavaScript", "SQL", "Shell Scripting"]
        }), 3),
        ("awards", "4. Certifications & Achievements", "fa-award", json.dumps({
            "highlights": [
                "Developer & Author of Safety Gear Compliance Detector (YOLOv8 PPE detection for electrical hazard environments)",
                "Active Contributor to OmniRoute (AI gateway routing 375+ LLM providers and 1,400+ models)",
                "Participant in regional university hackathons and engineering technical symposiums across Odisha (BPUT)",
                "Continuous hands-on implementation of production-grade neural networks and computer vision systems"
            ]
        }), 4),
        ("fields_of_interest", "5. Core Fields of Interest", "fa-compass", json.dumps({
            "interests": [
                {"title": "Real-Time Computer Vision & Edge AI", "desc": "Deploying lightweight object detection models (YOLOv8, Nano-models) for industrial surveillance, worker safety, and autonomous monitoring."},
                {"title": "Industrial Automation & PPE Compliance", "desc": "Deep neural systems that eliminate hazards in high-voltage and construction work environments via automated camera streams."},
                {"title": "Generative AI & Unified Model Gateways", "desc": "Designing quota-aware multi-LLM routers, token compression engines, and Model Context Protocol (MCP) tool integrations."},
                {"title": "Cybersecurity & Defensive Architecture", "desc": "Zero-trust architectures, dual-database air-gapped isolation, cryptographically salted authentication."}
            ]
        }), 5),
        ("personal_about", "6. Personal Philosophy & Background", "fa-user-astronaut", json.dumps({
            "origin_roots": "Hailing from the scenic cultural highlands of Koraput, Odisha, driven by a vision to harness modern AI and deep learning to solve tangible physical-world problems.",
            "motto": "Transforming abstract neural architectures into reliable safety shields and intuitive developer systems.",
            "hobbies": ["Exploring latest Computer Vision research papers", "Open-source tinkering and AI model testing", "Algorithmic problem solving", "Tech community networking"]
        }), 6),
        ("internships", "7. Internships & Practical Project Experience", "fa-briefcase", json.dumps({
            "projects_experience": [
                {"role": "Lead Computer Vision Researcher & Developer", "org": "Safety Gear AI Initiative (Self-Directed Engineering)", "period": "2024 - Present", "desc": "Designed, labeled, and trained YOLOv8 architectures to detect safety gear (helmets, harnesses, insulated gloves) in electrical hazard workspaces."},
                {"role": "Open-Source Gateway Contributor", "org": "OmniRoute AI Gateway", "period": "2024 - Present", "desc": "Tested and maintained universal multi-provider routing supporting 375+ AI providers, auto-fallback, and token compression."},
                {"role": "Undergraduate CSE Researcher", "org": "VITAM / BPUT Technical Labs", "period": "2023 - Present", "desc": "Active laboratory and coursework development focusing on data structures, algorithmic engineering, and web microservices."}
            ]
        }), 7)
    ]
    cursor.executemany("""
    INSERT INTO dossier_sections (section_key, title, icon, content_json, order_index)
    VALUES (?, ?, ?, ?, ?)
    """, sections)

    # Re-seed AI Knowledge Base with enriched exact details
    cursor.execute("DELETE FROM ai_knowledge")
    knowledge_items = [
        ("Identity & Full Name", "Full Name: BISWAJEET SHADANGI. Online Handle: Pshypher-Techie. Location: Koraput, Odisha, India.", "Identity"),
        ("Academic Credentials", "Biswajeet is currently pursuing B.Tech in Computer Science & Engineering (CSE) - 2nd Year at VITAM (Vignan Institute of Technology and Management) under BPUT (Biju Patnaik University of Technology, Odisha).", "Education"),
        ("Verified Contacts", "Phone: +91 7847881225. Email: biswajeetshadangi98@gmail.com. LinkedIn: https://www.linkedin.com/in/biswajeet-shadangi-701590447. Instagram: https://www.instagram.com/_pshypher_12_. X/Twitter: https://x.com/BISWAJEET140222. GitHub: https://github.com/Pshypher-Techie.", "Contacts"),
        ("Origins & Hometown", "Biswajeet comes from Koraput, Odisha, India.", "Background"),
        ("Technical Skills", "Specialized in Computer Vision (YOLOv8, OpenCV), PyTorch, Deep Learning, Python Full-Stack (FastAPI, AsyncIO), AI Gateways (OmniRoute), and Dual-Database Secure Architecture.", "Skills"),
        ("Safety Gear AI", "Author of safety-gear-compliance-detector, safety-gear-detection-ai, and worker-safety-ai using YOLOv8 to automate workplace safety and PPE compliance (helmets, gloves, vests) in electrical environments.", "Projects"),
        ("OmniRoute AI Gateway", "Active contributor to OmniRoute, an open-source AI gateway bridging 375+ LLM providers and 1,400+ models with quota-aware routing and RTK+Caveman token compression.", "Projects"),
        ("Field of Interest", "Focused on Real-Time Computer Vision & Edge AI, Industrial Safety Automation, Multi-LLM Routing Gateways, and Defensive Cybersecurity Architecture.", "Interests"),
        ("Personal Philosophy", "Passionate engineer from Koraput applying AI to tangible physical-world problems, with a philosophy of converting abstract neural models into practical, life-saving systems.", "Personal")
    ]
    cursor.executemany("""
    INSERT INTO ai_knowledge (topic, fact_content, category)
    VALUES (?, ?, ?)
    """, knowledge_items)

    conn.commit()
    conn.close()

def get_dossier_data():
    conn = get_dossier_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile_info LIMIT 1")
    profile = dict(cursor.fetchone() or {})
    
    cursor.execute("SELECT * FROM footprint_sources ORDER BY verified DESC, confidence DESC")
    footprints = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM repositories ORDER BY stars DESC, id ASC")
    repos = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM dossier_sections ORDER BY order_index ASC")
    sections = [
        {
            "id": row["id"],
            "section_key": row["section_key"],
            "title": row["title"],
            "icon": row["icon"],
            "content": json.loads(row["content_json"]),
            "order_index": row["order_index"]
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("SELECT * FROM ai_knowledge")
    knowledge = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT 5")
    scans = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "profile": profile,
        "footprints": footprints,
        "repositories": repos,
        "sections": sections,
        "knowledge": knowledge,
        "recent_scans": scans
    }

def update_dossier_repositories(repo_list: list):
    conn = get_dossier_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    for r in repo_list:
        cursor.execute("""
        INSERT INTO repositories (name, description, url, language, stars, is_fork, updated_at, ai_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            description=excluded.description,
            url=excluded.url,
            language=excluded.language,
            stars=excluded.stars,
            updated_at=excluded.updated_at
        """, (
            r.get("name"),
            r.get("description") or "No description provided",
            r.get("html_url"),
            r.get("language") or "Python",
            r.get("stargazers_count", 0),
            1 if r.get("fork") else 0,
            r.get("updated_at") or now,
            f"Repository {r.get('name')} in {r.get('language') or 'code'}."
        ))
    cursor.execute("""
    INSERT INTO scan_logs (scan_time, status, sources_found, details)
    VALUES (?, 'LIVE_SYNC', ?, 'Live GitHub API repository sync completed.')
    """, (now, len(repo_list)))
    conn.commit()
    conn.close()

def add_custom_footprint(platform: str, identifier: str, url: str, category: str, summary: str):
    conn = get_dossier_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO footprint_sources (platform, identifier, url, verified, confidence, category, summary, last_checked)
    VALUES (?, ?, ?, 1, 95, ?, ?, ?)
    """, (platform, identifier, url, category, summary, now))
    conn.commit()
    conn.close()

def get_dossier_stats():
    conn = get_dossier_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM repositories")
    repos_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM footprint_sources WHERE verified = 1")
    verified_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ai_knowledge")
    facts_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM dossier_sections")
    sections_cnt = cursor.fetchone()[0]
    conn.close()
    return {
        "total_repositories": repos_cnt,
        "verified_footprint_sources": verified_cnt,
        "ai_knowledge_facts": facts_cnt,
        "dossier_sections_count": sections_cnt
    }
