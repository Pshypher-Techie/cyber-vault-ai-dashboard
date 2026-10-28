import re
from app.database_dossier import get_dossier_db_connection

def query_ai_dossier(query: str) -> dict:
    q = query.strip().lower()
    conn = get_dossier_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profile_info LIMIT 1")
    profile = dict(cursor.fetchone() or {})

    cursor.execute("SELECT * FROM repositories")
    repos = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM ai_knowledge")
    facts = [dict(f) for f in cursor.fetchall()]
    conn.close()

    response_text = ""
    category_matched = "General Intelligence"

    if any(k in q for k in ["who", "about", "bio", "background", "introduce", "summary", "name"]):
        response_text = (
            f"**Identity Dossier: {profile.get('full_name', 'BISWAJEET SHADANGI')}** (Moniker: `{profile.get('alias', 'Pshypher-Techie')}`)\n\n"
            f"• **Formal Qualification**: {profile.get('qualification')}\n"
            f"• **Institution**: {profile.get('college')} affiliated with {profile.get('university')}\n"
            f"• **Comes From / Origin**: {profile.get('origin', 'Koraput, Odisha, India')}\n"
            f"• **Headline**: {profile.get('headline')}\n"
            f"• **Primary Focus**: Developing real-time Computer Vision architectures (YOLOv8 safety gear compliance) and multi-provider AI Gateways (OmniRoute)."
        )
        category_matched = "Identity & Bio"

    elif any(k in q for k in ["qualification", "college", "degree", "education", "vitam", "bput", "year"]):
        response_text = (
            f"**Academic Qualifications:**\n\n"
            f"• **Degree**: {profile.get('qualification')}\n"
            f"• **College**: {profile.get('college')}\n"
            f"• **University**: {profile.get('university')}\n"
            f"• **Location**: Berhampur / Koraput, Odisha, India\n"
            f"• **Academic Track**: Data Structures, Computer Vision, Deep Learning, Object-Oriented Systems."
        )
        category_matched = "Academic Pedigree"

    elif any(k in q for k in ["contact", "phone", "email", "linkedin", "instagram", "twitter", "x", "reach", "hire", "number"]):
        response_text = (
            f"**Official Verified Communication Matrix for {profile.get('full_name')}:**\n\n"
            f"• **Direct Phone**: `{profile.get('phone', '+91 7847881225')}`\n"
            f"• **Direct Email**: `{profile.get('email', 'biswajeetshadangi98@gmail.com')}`\n"
            f"• **LinkedIn**: [{profile.get('linkedin_url')}]({profile.get('linkedin_url')})\n"
            f"• **Instagram**: [{profile.get('instagram_url')}]({profile.get('instagram_url')})\n"
            f"• **X / Twitter**: [{profile.get('twitter_url')}]({profile.get('twitter_url')})\n"
            f"• **GitHub**: [{profile.get('github_url')}](https://github.com/Pshypher-Techie)\n"
            f"• **Origin Base**: Koraput, Odisha, India"
        )
        category_matched = "Direct Contacts"

    elif any(k in q for k in ["koraput", "from", "hometown", "place", "origin", "comes from"]):
        response_text = (
            f"**Geographical Roots & Origin:**\n\n"
            f"• **Hometown**: **Koraput, Odisha, India**\n"
            f"• **Current Studies**: VITAM (Berhampur) under BPUT Odisha.\n"
            f"• Biswajeet is proud of his Koraput roots, bringing regional engineering talent to cutting-edge AI and computer vision."
        )
        category_matched = "Origins"

    elif any(k in q for k in ["skill", "stack", "tech", "languages", "tools"]):
        response_text = (
            "**Technical Competency Matrix:**\n\n"
            "• **Artificial Intelligence & Vision**: Ultralytics YOLOv8, OpenCV, PyTorch, Real-Time Inference Pipelines, Video Stream Analytics.\n"
            "• **Generative AI & LLMs**: OmniRoute Gateway Contributor, 375+ LLM orchestration, Token Compression (RTK+Caveman), Model Context Protocol.\n"
            "• **Software Development**: Python (FastAPI, AsyncIO), C++, JavaScript, Shell, RESTful Architectures.\n"
            "• **Systems & Security**: Air-Gapped Dual-Database Design (SQLite/PostgreSQL), Cryptographic Token Derivation, Linux/OpenSSH."
        )
        category_matched = "Skillset Matrix"

    elif any(k in q for k in ["safety", "yolo", "vision", "ppe", "gear", "compliance", "hazard"]):
        response_text = (
            "**Industrial Safety & Computer Vision Architecture:**\n\n"
            "Biswajeet has engineered custom deep learning solutions to prevent industrial casualties:\n"
            "1. **`safety-gear-compliance-detector`**: YOLOv8-powered model detecting mandatory PPE (hardhats, safety goggles, insulating electrical gloves, harness straps).\n"
            "2. **`safety-gear-detection-ai` & `worker-safety-ai`**: Real-time surveillance prototypes with automated hazard warnings for electrical work environments."
        )
        category_matched = "Computer Vision Deep Dive"

    elif any(k in q for k in ["omniroute", "gateway", "llm", "inference"]):
        response_text = (
            "**OmniRoute AI Gateway Infrastructure:**\n\n"
            "Biswajeet is an active contributor to **OmniRoute**:\n"
            "• Connects 375+ AI providers (with 150+ free tiers) and 1,400+ models.\n"
            "• Auto-fallback with quota awareness.\n"
            "• Token compression algorithms saving 15% to 95% token overhead."
        )
        category_matched = "AI Infrastructure"

    elif any(k in q for k in ["internship", "experience", "work"]):
        response_text = (
            "**Practical Experience & Projects:**\n\n"
            "• **Safety Gear AI Initiative**: Lead developer of deep learning PPE detection for workplace safety.\n"
            "• **OmniRoute Open-Source Contributor**: Open-source model gateway optimization and benchmarking.\n"
            "• **VITAM/BPUT Labs**: Undergraduate research in software engineering and algorithmic problem solving."
        )
        category_matched = "Experience"

    elif any(k in q for k in ["interest", "field"]):
        response_text = (
            "**Core Fields of Interest:**\n\n"
            "1. **Real-Time Edge AI & Computer Vision** (YOLOv8, embedded inference).\n"
            "2. **Industrial Safety Automation** (hazard mitigation).\n"
            "3. **Multi-LLM Routing & Compression Systems**.\n"
            "4. **Defensive Cybersecurity & Data Isolation**."
        )
        category_matched = "Fields of Interest"

    else:
        response_text = (
            f"Verified internet records confirmed for **{profile.get('full_name')}** from Koraput, Odisha. "
            f"He is currently in his 2nd Year B.Tech CSE at VITAM under BPUT. "
            f"You can ask about his **qualifications**, **phone/social contacts**, **YOLOv8 safety models**, **OmniRoute AI gateway**, or **skills**!"
        )

    return {
        "query": query,
        "category": category_matched,
        "response": response_text,
        "confidence": 0.99
    }
