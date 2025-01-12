from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from loguru import logger
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    totalWordCount: int

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
    
    # Log the received form data
    logger.info(f"Received form data: {form_data}")
    logger.info(f"Token info: {token_info}")
    
    # Return the received data as a response
    return form_data.dict()

# Run the application on port 8080
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

