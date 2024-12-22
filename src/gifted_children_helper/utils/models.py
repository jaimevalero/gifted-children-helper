import os
from crewai import LLM
from loguru import logger
from llama_index.embeddings.ollama import OllamaEmbedding

def get_embed_model_name():
    """
    Retrieve the embedding model name from the environment variable.

    Returns:
        str: The name of the embedding model. Defaults to 'mxbai-embed-large' if not set.
    """
    return os.getenv("EMBED_MODEL", "mxbai-embed-large")

def get_base_url():
    """
    Retrieve the base URL from the environment variable.

    Returns:
        str: The base URL for ollama
    """
    return os.getenv("API_BASE", "http://127.0.0.1:11434")

def get_embed_model():
    embed_model_name = get_embed_model_name()
    base_url = get_base_url()    
    embed_model = OllamaEmbedding(
            model_name=embed_model_name,
            base_url=base_url,
            ollama_additional_kwargs={"prostatic": 0},
        )      
    return embed_model

def get_model_name():
    """
    Retrieve the model name from the provided model name or environment variable.

    Args:
        model_name (str, optional): The name of the model to retrieve. Defaults to None.

    Returns:
        str: The name of the model.
    """
    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        logger.warning("No model name provided, using default model")
        model_name = "ollama/llama3.1:8b"
    return model_name

def get_model(model_name=None):
    """
    Retrieve the model based on the provided model name or environment variable.

    Args:
        model_name (str, optional): The name of the model to retrieve. Defaults to None.

    Returns:
        LLM: An instance of the LLM class configured with the specified or default model name.
    """
    model_name = get_model_name()
    base_url = get_base_url()
    return LLM(
        base_url=base_url,
        model=model_name,
    )

