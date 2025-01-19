# Standard library imports
import os
import sys
import threading
from datetime import datetime
from typing import Dict

# Special sqlite3 hack (must be before other imports)
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Third-party imports
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import uvicorn
import requests
from dotenv import load_dotenv
from filelock import FileLock

# Add the src directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


from gifted_children_helper.utils.secrets import load_secrets
load_secrets()

# Local application imports
from backend_fastapi.auth_store import AuthStore
from gifted_children_helper.utils.reports import log_system_usage
from gifted_children_helper.main import get_case, run



# Create an instance of the FastAPI class
app = FastAPI()

# Add CORS middleware to allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AuthStore
auth_store = AuthStore()

# Define a Pydantic model for the form data
class FormData(BaseModel):
    description: str
    family_dynamics: str
    emotional_behavior: str
    skills_development: str
    school_context: str
    problems_difficulties: str
    additional_observations: str
    uuid: str  

def verify_google_token(token: str) -> dict:
    """
    Verify the Google ID token.

    Args:
        token (str): The Google ID token.

    Returns:
        dict: The token information if valid, raises HTTPException otherwise.
    """
    try:
        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Token verification failed")

def websocket_callback( *args, **kwargs):
    """
    Callback function to send progress updates via WebSocket.

    Args:
        uuid (str): The unique identifier for the report generation job.
        args: Additional positional arguments.
        kwargs: Additional keyword arguments to send as part of the update.
    """
    logger.info(f"Sending update to WebSocket for UUID : args={args}, kwargs={kwargs}")

@app.get("/health")
@app.get("/healthz")
@app.get("/status")
async def health_check():
    """
    Health check endpoint that responds to multiple paths (/health, /healthz, /status)
    following common REST API conventions.
    
    Returns:
        dict: Health status information including timestamp and service name
    """
    logger.debug("Health check requested")
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "gifted-children-helper-api"
    }

# Define a route to handle form submissions
@app.post("/generate-report")
async def submit_form(request: Request, form_data: FormData):
    """
    Endpoint to handle form submission.
    
    Args:
        request (Request): The request object containing headers.
        form_data (FormData): The form data submitted by the user.
    
    Returns:
        dict: A dictionary containing the submitted data.
    """
    # Extract the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    token = auth_header.split(" ")[1]
    token_info = verify_google_token(token)
    user_id = token_info['sub']
    
    # Store the authorization
    auth_store.add_auth(form_data.uuid, user_id)
    
    # Log the received form data and jobId
    logger.info(f"Received form data: {form_data}")
    logger.info(f"Token info: {token_info}")
    logger.info(f"Job ID: {form_data.uuid}")
    uuid = form_data.uuid
    case = ""
    if form_data.description:
        case += f"**Descripción del Niño/a:** {form_data.description}\n"
    if form_data.family_dynamics:
        case += f"**Dinámica Familiar:** {form_data.family_dynamics}\n"
    if form_data.emotional_behavior:
        case += f"**Comportamiento y Manejo Emocional:** {form_data.emotional_behavior}\n"
    if form_data.skills_development:
        case += f"**Habilidades y Desarrollo:** {form_data.skills_development}\n"
    if form_data.school_context:
        case += f"**Contexto Escolar y Extraescolar:** {form_data.school_context}\n"
    if form_data.problems_difficulties:
        case += f"**Problemas y Situaciones Difíciles:** {form_data.problems_difficulties}\n"
    if form_data.additional_observations:
        case += f"**Observaciones Adicionales:** {form_data.additional_observations}\n"
    
    case = get_case()

    # Run the report generation in a separate thread
    thread = threading.Thread(target=run, args=(case, websocket_callback, uuid))
    thread.start()

    log_system_usage()

    # Return the UUID to the frontend immediately
    return {"uuid": form_data.uuid }

@app.get("/report_download/{uuid}")
async def report_download(uuid: str):
    """
    HTTP endpoint to download the generated report.
    Returns the PDF with a fixed filename regardless of the UUID.

    Args:
        uuid (str): The unique identifier for the report generation job.

    Returns:
        FileResponse: The generated report file with fixed filename 'final_report.pdf'
    """
    # Check if the report file exists
    pdf_file = f"logs/{uuid}.pdf"
      
    if os.path.exists(pdf_file):
        return FileResponse(
            path=pdf_file, 
            media_type="application/pdf", 
            filename="final_report.pdf"  # Nombre fijo para el archivo descargado
        )
    raise HTTPException(status_code=404, detail="Report file not found")

# HTTP endpoint to send report status updates
@app.get("/report_status/{uuid}")
async def report_status(request: Request, uuid: str):
    """
    HTTP endpoint to send report status updates.

    Args:
        uuid (str): The unique identifier for the report generation job.

    Returns:
        dict: The progress status of the report generation.
    """
    # Extract and verify token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    token = auth_header.split(" ")[1]
    token_info = verify_google_token(token)
    user_id = token_info['sub']
    
    report_belongs_user = auth_store.verify_auth(uuid, user_id) # Verify authorization
    if not report_belongs_user:
        raise HTTPException(status_code=403, detail="Unauthorized access to report")
    
    progress_file = f"tmp/{uuid}_progress.json"
    lock = FileLock(f"{progress_file}.lock")  # Create a lock for the progress file
    if os.path.exists(progress_file):
        try:
            with lock:  # Use the lock when accessing the file
                with open(progress_file) as f:
                    progress = json.load(f)  # Convert the string to a JSON object
                    logger.info(f"Sending progress update for UUID {uuid}: {progress}")
                    return progress
        except Exception as e:
            logger.error(f"An error occurred while reading progress file: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while reading progress file")
    raise HTTPException(status_code=404, detail="Progress file not found")

# Add cleanup task
@app.on_event("startup")
async def startup_event():
    """Clean up expired entries on startup"""
    auth_store.cleanup()

# Run the application on port 8080
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)


