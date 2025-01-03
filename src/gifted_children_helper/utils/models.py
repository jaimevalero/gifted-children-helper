import os

from crewai import LLM
from loguru import logger
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

def get_embed_aux_model_name():
    """
    Retrieve the auxiliary embedding model name from the environment variable.

    Returns:
        str: The name of the auxiliary embedding model. 
    """
    return os.getenv("OLLAMA_MODEL_AUX_EMBED_NAME", get_model_name())
def get_embed_model_name():
    """
    Retrieve the embedding model name from the environment variable.

    Returns:
        str: The name of the embedding model. Defaults to 'mxbai-embed-large' if not set.
    """
    if not os.getenv("EMBED_MODEL"):
        raise ValueError("EMBED_MODEL environment variable not set")
    return os.getenv("EMBED_MODEL").replace("ollama/", "")

def get_base_url():
    """
    Retrieve the base URL from the environment variable.

    Returns:
        str: The base URL for ollama
    """
    return os.getenv("OLLAMA_API_BASE")

def get_embed_model():
    embed_model_name = get_embed_model_name()
    base_url = get_base_url()   
     
    embed_model = OllamaEmbedding(
            model_name=embed_model_name,
            base_url=base_url,
            num_ctx=8192,
            request_timeout=3600,
            keep_alive="25m",
            ollama_additional_kwargs={
                "prostatic": 0, 
                "num_ctx" : 8192},
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
    # load .env file
    
    model_name = os.getenv("OLLAMA_MODEL_NAME")
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
    if not model_name:
        model_name = get_model_name()
    base_url = get_base_url()


    Settings.context_windows= 8192
    llm = Ollama(
            model=model_name.replace("ollama/", ""),
            base_url = base_url,
            num_ctx=1024*32,
            context_window=1028*8,
            request_timeout=3600,
            keep_alive="25m"
            )
    return llm

