from dotenv import load_dotenv
import os
import json
from loguru import logger

def load_secrets(st=None):
    """
    Load secrets from Streamlit's secrets.toml and update environment variables and client_secret.json.
    """
    logger.info("Loading secrets from secrets.toml")
    
    # Load environment variables from .env file
    load_dotenv(override=False)

    if st:
        # Update environment variables with secrets from secrets.toml
        os.environ["MAIN_TOKEN"] = st.secrets["MAIN_TOKEN"]
        os.environ["AUX_TOKEN"] = st.secrets["AUX_TOKEN"]
        os.environ["EMBED_TOKEN"] = st.secrets["EMBED_TOKEN"]
        os.environ["TOKEN_KEY"] = st.secrets["TOKEN_KEY"]

        # Update client_secret.json with secrets from secrets.toml
        client_secret_path = "client_secret.json"
        with open(client_secret_path, "r") as file:
            client_secret_data = json.load(file)

        client_secret_data["web"]["client_id"] = st.secrets["client_id"]
        client_secret_data["web"]["client_secret"] = st.secrets["client_secret"]

        with open(client_secret_path, "w") as file:
            json.dump(client_secret_data, file, indent=2)
            
    else:
        # We are not in a Streamlit environment, just load secrets from secrets.toml
        # Load secrets from secrets file, and sets  environment variables
        secrets_file = ".streamlit/secrets.toml"
        if os.path.exists(secrets_file):
            with open(secrets_file, "r") as file:
                secrets = file.readlines()
                for secret in secrets:
                    key, value = secret.strip().split(" = ")
                    # skip empty lines , or lines that contains "#" caracters
                    if not key or key.startswith("#"):
                        continue
                    os.environ[key] = value.replace('"', "").replace("'", "")
        else:
            logger.error("Secrets file not found")
    # Check if the secrets were loaded correctly, if env MAIN_TOKEN is not set, raise an error
    if not os.getenv("MAIN_TOKEN"):
        logger.error("Error loading secrets")
        raise ValueError("Error loading secrets MAIN_TOKEN")





