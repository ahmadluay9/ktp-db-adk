import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 1. Mount the static directory
# This allows the HTML to access /static/chatbot.js and /static/questions.json
os.makedirs("static", exist_ok=True) # Ensure dir exists
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Serve the index.html at the root
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# 3. Dummy API endpoints to prevent 404 errors in the console
# (The chatbot.js tries to fetch these on load)
@app.get("/api/sessions")
async def get_sessions(user_id: str = None, app_name: str = None):
    return []

if __name__ == "__main__":
    print("Server running at http://localhost:8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)