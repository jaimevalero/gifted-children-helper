from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from loguru import logger
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import Dict
import asyncio
from gifted_children_helper.utils.reports import log_system_usage
from gifted_children_helper.main import get_case, run
from gifted_children_helper.utils.secrets import load_secrets
import json

# Ugly hack because of https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Add the src directory to PYTHONPATH, because stream cloud expects all paths refered to app file directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Load environment variables from .env file
load_dotenv()
load_secrets()

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
    # Run the report generation with the WebSocket callback
    report_filename = await run(case, websocket_callback, uuid)
    
    log_system_usage()

    if os.path.exists(report_filename):
        mime = "application/pdf" if report_filename.endswith(".pdf") else "text/markdown"
        file_name = "informe_final.pdf" if report_filename.endswith(".pdf") else "informe_final.md"
        return FileResponse(report_filename, media_type=mime, headers={"Content-Disposition": f"attachment; filename={file_name}"})

    # Return the received data as a response
    return {"jobId": form_data.uuid}

# HTTP endpoint to send report status updates
@app.get("/report_status/{uuid}")
async def report_status(uuid: str):
    """
    HTTP endpoint to send report status updates.

    Args:
        uuid (str): The unique identifier for the report generation job.

    Returns:
        dict: The progress status of the report generation.
    """
    progress_file = f"tmp/{uuid}_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            progress = json.load(f)  # Convert the string to a JSON object
            logger.info(f"Sending progress update for UUID {uuid}: {progress}")
            return progress
    raise HTTPException(status_code=404, detail="Progress file not found")

# Run the application on port 8080
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

