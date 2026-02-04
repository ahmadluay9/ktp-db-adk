import os
import urllib.parse
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService

load_dotenv()

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

APP_NAME = "ktp_agent"

# Pydantic Models (Data Schemas) 
class EventPart(BaseModel):
    text: Optional[str] = None

class EventContent(BaseModel):
    role: Optional[str] = None
    parts: List[EventPart] = []

class SessionEvent(BaseModel):
    author: Optional[str] = None
    role: Optional[str] = None
    parts: List[Dict[str, Any]] = [] 

class SessionResponse(BaseModel):
    id: str
    last_update_time: Optional[Any] = None

class SessionDetailResponse(BaseModel):
    id: str
    events: List[SessionEvent]

# Database Configuration
DB_USER = os.environ.get("CLOUD_SQL_PG_USER")
DB_PASSWORD = os.environ.get("CLOUD_SQL_PG_PASSWORD")
DB_DATABASE = os.environ.get("CLOUD_SQL_PG_SESSIONDB")
DB_CONNECTION_NAME = os.environ.get("CLOUD_SQL_PG_CONNECTION_NAME")
DB_HOST = os.environ.get("CLOUD_SQL_PG_HOST")

if DB_USER and DB_PASSWORD and DB_DATABASE:
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    
    if DB_HOST:
        # TCP Connection (Local testing or specific setup)
        port = os.environ.get("CLOUD_SQL_PG_PORT", "5432")
        SESSION_SERVICE_URI = (
            f"postgresql+asyncpg://{DB_USER}:{encoded_password}@"
            f"{DB_HOST}:{port}/{DB_DATABASE}"
        )
    elif DB_CONNECTION_NAME:
        # Unix Socket Connection (Cloud Run standard)
        SESSION_SERVICE_URI = (
            f"postgresql+asyncpg://{DB_USER}:{encoded_password}@"
            f"/{DB_DATABASE}?host=/cloudsql/{DB_CONNECTION_NAME}"
        )

# Initialize Session Service
try:
    session_service = DatabaseSessionService(db_url=SESSION_SERVICE_URI)
    print(f"Session Service initialized with URI: {SESSION_SERVICE_URI}")
except Exception as e:
    print(f"Failed to initialize Session Service: {e}")
    session_service = None

app = FastAPI()

# Define Routes (Endpoints)
static_path = os.path.join(AGENT_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Route /home to the index.html file
@app.get("/home")
async def read_home():
    return FileResponse(os.path.join(static_path, "index.html"))

# API Routes for Session Management
@app.get("/api/sessions", response_model=List[SessionResponse])
async def list_sessions(user_id: str = Query(...), app_name: str = APP_NAME):
    """Lists all sessions for a specific user with robust error handling."""
    if not session_service:
        raise HTTPException(status_code=500, detail="Database service not initialized")
    
    try:
        response_obj = await session_service.list_sessions(app_name=app_name, user_id=user_id)
        
        # Handle different return types (list vs object vs tuples)
        sessions = []
        if isinstance(response_obj, list):
            sessions = response_obj
        else:
            # If it's a wrapper object (ListSessionsResponse)
            sessions = getattr(response_obj, 'sessions', [])
            
        results = []
        for s in sessions:
            s_id = None
            last_update_time = None
            
            # Case 1: Standard Object
            if hasattr(s, 'id'):
                s_id = s.id
                last_update_time = getattr(s, 'last_update_time', None)
            
            # Case 2: Dictionary
            elif isinstance(s, dict):
                s_id = s.get('id')
                last_update_time = s.get('last_update_time')
            
            # Case 3: Tuple/Row
            elif isinstance(s, (tuple, list)) and len(s) > 0:
                s_id = s[0] # Assume ID is first column
                if len(s) > 1: last_update_time = s[1]

            if s_id:
                # Ensure ID is string
                results.append(SessionResponse(id=str(s_id), last_update_time=last_update_time))
        
        return results

    except Exception as e:
        print(f"Error listing sessions: {e}")
        # Return empty list on error to prevent UI crash, but log it
        return []

@app.get("/api/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str, user_id: str = Query(...), app_name: str = APP_NAME):
    """Gets details and history of a specific session."""
    if not session_service:
        raise HTTPException(status_code=500, detail="Database service not initialized")
    
    try:
        session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        events_data = []
        if hasattr(session, 'events'):
            for event in session.events:
                parts = []
                
                # Extract content parts safely
                if hasattr(event, "content") and event.content:
                    # Check if 'parts' exists and is iterable
                    if hasattr(event.content, "parts") and isinstance(event.content.parts, list):
                        for part in event.content.parts:
                            # Extract text
                            if hasattr(part, "text") and part.text:
                                parts.append({"text": part.text})
                
                events_data.append(SessionEvent(
                    author=getattr(event, "author", None),
                    role=getattr(event.content, "role", None) if hasattr(event, "content") else None,
                    parts=parts
                ))

        return SessionDetailResponse(id=session.id, events=events_data)
    except Exception as e:
        print(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Server running")
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)