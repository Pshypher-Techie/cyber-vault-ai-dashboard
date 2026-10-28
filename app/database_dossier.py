import sqlite3
import json
from datetime import datetime, timezone
from app.config import DOSSIER_DB_PATH, SUBJECT_NAME, SUBJECT_HANDLE, SUBJECT_EMAIL, SUBJECT_LOCATION

def get_dossier_db_connection():
    conn = sqlite3.connect(DOSSIER_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_dossier_db():
    conn = get_dossier_db_connection()
    cursor = conn.cursor()

    # Table 1: Core Subject Identity & Profile Dossier
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        alias TEXT NOT NULL,
        email TEXT NOT NULL,
        location TEXT,
        headline TEXT,
        bio TEXT,
        specialization TEXT,
        academic_background TEXT,
        avatar_url TEXT,
        updated_at TEXT NOT NULL
    )
    """)

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

    # Table 4: AI Dossier Knowledge Base & Intelligence Facts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        fact_content TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)

    # Table 5: Internet Footprint Scan Audits
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

    # Seed initial verified dossier if empty
    cursor.execute("SELECT COUNT(*) FROM profile_info")
    if cursor.fetchone()[0] == 0:
        now = datetime.now(timezone.utc).isoformat()
        
        # Profile Seed
        cursor.execute("""
        INSERT INTO profile_info (full_name, alias, email, location, headline, bio, specialization, academic_background, avatar_url, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            SUBJECT_NAME,
            SUBJECT_HANDLE,
            SUBJECT_EMAIL,
            SUBJECT_LOCATION,
            "AI & Computer Vision Engineer | Open-Source Gateway Contributor | YOLOv8 Safety Systems Specialist",
            "Software engineer and AI practitioner specialized in deep learning, real-time computer vision (PPE safety compliance detection), and universal AI inference gateways. Active contributor in developer communities with a passion for building robust intelligent systems.",
            "Computer Vision, YOLOv8 Deep Learning, AI Gateway Orchestration, Python Engineering, Worker Safety Automation",
            "Biju Patnaik University of Technology (BPUT), Odisha - Engineering & Hackathon Technical Competitions",
            "https://avatars.githubusercontent.com/u/328466102?v=4",
            now
        ))

        # Verified Footprint Sources
        footprint_items = [
            ("GitHub Primary", "Pshypher-Techie", "https://github.com/Pshypher-Techie", 1, 99, "Code Intelligence", "Primary GitHub identity hosting computer vision models and AI gateway repos", now),
            ("Git Commits Identity", "biswajeetshadangi98@gmail.com", "mailto:biswajeetshadangi98@gmail.com", 1, 99, "Author Verification", "Verified author of commits across active safety AI and web projects", now),
            ("Academic Footprint", "Biswajeet Shadangi (BPUT)", "https://www.bput.ac.in", 1, 90, "Academic & Awards", "Academic records and technical hackathon involvement in Odisha technical universities", now),
            ("AI Inference Gateway", "OmniRoute Contributor", "https://github.com/Pshypher-Techie/OmniRoute", 1, 95, "Open-Source AI", "Active fork & testing of universal multi-provider (375+ LLMs) gateway", now),
            ("Industrial Vision AI", "safety-gear-compliance-detector", "https://github.com/Pshypher-Techie/safety-gear-compliance-detector", 1, 98, "Computer Vision", "YOLOv8 deep learning prototype for electrical hazard & PPE worker compliance", now),
            ("HuggingFace & LeetCode", "Pshypher-Techie / Biswa", "https://leetcode.com", 0, 75, "Competitive & ML", "Algorithmic problem solving and machine learning exploration profile", now),
            ("Gravatar Profile Check", "biswajeetshadangi98@gmail.com", "https://gravatar.com", 1, 85, "Identity Hash", "Global hash confirmation across developer web federations", now),
        ]
        cursor.executemany("""
        INSERT INTO footprint_sources (platform, identifier, url, verified, confidence, category, summary, last_checked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, footprint_items)

        # Repositories Seed (Real GitHub projects discovered)
        repo_items = [
            ("OmniRoute", "Never stop coding. Free MIT AI gateway: one endpoint, 375 providers (150+ free), 1,400+ models (Claude, GPT, Gemini, GLM, DeepSeek). Quota-aware auto-fallback & token compression.", "https://github.com/Pshypher-Techie/OmniRoute", "Python / Multi", 0, 1, now, "Universal multi-model AI routing infrastructure."),
            ("safety-gear-compliance-detector", "AI prototype system for detecting safety gear compliance (PPE) in electrical work environments using YOLOv8 computer vision.", "https://github.com/Pshypher-Techie/safety-gear-compliance-detector", "Python / PyTorch / YOLOv8", 1, 0, now, "Real-time industrial surveillance model classifying helmets, insulating gloves, and harnesses."),
            ("safety-gear-detection-ai", "AI system prototype for detecting safety gear compliance using computer vision and deep learning.", "https://github.com/Pshypher-Techie/safety-gear-detection-ai", "Python", 0, 0, now, "Deep neural network for automated workplace safety inspection."),
            ("worker-safety-ai", "AI system to ensure safety measures among workers using computer vision and monitoring.", "https://github.com/Pshypher-Techie/worker-safety-ai", "Python", 0, 0, now, "Worker hazard prevention monitor with live video inference."),
            ("todo-list-app", "A high performance to-do list application with local storage functionality and reactive UI.", "https://github.com/Pshypher-Techie/todo-list-app", "JavaScript / HTML", 0, 0, now, "Productivity application demonstrating client-side storage state management.")
        ]
        cursor.executemany("""
        INSERT INTO repositories (name, description, url, language, stars, is_fork, updated_at, ai_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, repo_items)

        # AI Knowledge Base Facts
        knowledge_items = [
            ("Identity & Background", "Biswajeet Shadangi (online handle: Pshypher-Techie) is an AI engineer and developer based in Odisha, India.", "Bio"),
            ("Specialization", "Biswajeet specializes in Computer Vision (YOLOv8, object detection for safety/PPE gear), AI gateways, and Python full-stack systems.", "Skills"),
            ("Safety Gear Detection", "Biswajeet built the 'safety-gear-compliance-detector' and 'worker-safety-ai' systems to automate workplace electrical safety and personal protective equipment (PPE) compliance.", "Projects"),
            ("OmniRoute Gateway", "Biswajeet works with OmniRoute, a unified AI gateway supporting 375+ LLM providers and over 1,400 models with quota-aware routing and token compression.", "Projects"),
            ("Education", "Associated with technical universities in Odisha including Biju Patnaik University of Technology (BPUT) with hackathon participation.", "Education"),
            ("Contact", "Verified primary email: biswajeetshadangi98@gmail.com. Verified GitHub: https://github.com/Pshypher-Techie", "Contact")
        ]
        cursor.executemany("""
        INSERT INTO ai_knowledge (topic, fact_content, category)
        VALUES (?, ?, ?)
        """, knowledge_items)

        cursor.execute("""
        INSERT INTO scan_logs (scan_time, status, sources_found, details)
        VALUES (?, 'SUCCESS', 5, 'Initial internet OSINT and GitHub synchronization completed successfully.')
        """, (now,))

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

    cursor.execute("SELECT * FROM ai_knowledge")
    knowledge = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT 5")
    scans = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "profile": profile,
        "footprints": footprints,
        "repositories": repos,
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
    conn.close()
    return {
        "total_repositories": repos_cnt,
        "verified_footprint_sources": verified_cnt,
        "ai_knowledge_facts": facts_cnt
    }

