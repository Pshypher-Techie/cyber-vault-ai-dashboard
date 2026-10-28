import uvicorn
from app.config import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    print(f"===============================================================")
    print(f"CYBER-VAULT :: AI-POWERED INTELLIGENCE DOSSIER (LIVE SERVER)")
    print(f"Listening on: http://127.0.0.1:{SERVER_PORT}")
    print(f"Theme: Futuristic Cyber Bluish-Green")
    print(f"Databases: Dual Isolated (users_auth.db & dossier_data.db)")
    print(f"===============================================================")
    uvicorn.run("app.main:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)

