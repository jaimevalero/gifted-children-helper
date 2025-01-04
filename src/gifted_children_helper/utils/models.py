import os

from crewai import LLM
from loguru import logger
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from enum import Enum

class Provider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"



def get_provider(default_model=None) -> Provider:
    """
    Get the provider from the model name.
    
    Returns:
        Provider: The provider enum value.
    """
    if not default_model:
        default_model = get_model_name()
    #logger.info(f"Default model name: {default_model}")
    
    if "ollama" in default_model:
        provider = Provider.OLLAMA
    elif "openai" in default_model or 'deepseek-chat' in default_model:
        provider = Provider.OPENAI
    else:
        raise ValueError(f"Provider not recognized for model {default_model}")
    
    #logger.info(f"Provider determined: {provider}")
    return provider

def get_api_key():
    """
    Retrieve the API key from the environment variable.

    Returns:
        str: The API key.
    """
    provider = get_provider()
    if provider == Provider.OPENAI:
        return os.getenv("OPENAI_API_KEY")
    elif provider == Provider.OLLAMA:
        raise ValueError("OLLAMA provider does not require an API key")
    
def get_embed_aux_model_name():
    """
    Retrieve the auxiliary embedding model name from the environment variable.

    Returns:
        str: The name of the auxiliary embedding model. 
    """
    provider = get_provider()
    if provider == Provider.OPENAI:
        aux_model_name =  os.getenv("OPENAI_MODEL_AUX_EMBED_NAME", get_model_name())
    elif provider == Provider.OLLAMA:
        aux_model_name = os.getenv("OLLAMA_MODEL_AUX_EMBED_NAME", get_model_name())
    else:
        raise ValueError("Provider not recognized")
    return aux_model_name
    
def get_model_embed_name():
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
    provider = get_provider()
    if provider == Provider.OPENAI:
        return os.getenv("OPENAI_API_BASE")
    elif provider == Provider.OLLAMA:
        return os.getenv("OLLAMA_API_BASE")
    else:
        raise ValueError("Provider not recognized")

def get_model_embed():

    embed_model_name = get_model_embed_name()
    base_url = get_base_url()   

    provider = get_provider()

    provider =  Provider.OLLAMA
    if provider ==  Provider.OLLAMA :
        embed_model = OllamaEmbedding(
                model_name=embed_model_name,
                base_url="http://127.0.0.1:11434", #base_url,
                num_ctx=8192,
                request_timeout=3600,
                keep_alive="25m",
                ollama_additional_kwargs={
                    "prostatic": 0, 
                    "num_ctx" : 8192},
            )      
    elif provider == Provider.OPENAI:
        embed_model =OpenAIEmbedding(
                model_name=embed_model_name,
                api_key=get_api_key(),
                api_base=base_url,
                num_ctx=8192,
                request_timeout=3600,
                keep_alive="25m",
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
    model_name = os.getenv("OLLAMA_MODEL_NAME", os.getenv("OPENAI_MODEL_NAME"))
    if not model_name:
        raise ValueError("MODEL_NAME environment variable not set")
    return model_name

def get_model_aux():
    llm = Ollama(
            model="qwen2.5:14b-8k",
            base_url = "http://127.0.0.1:11434",
            num_ctx=1024*32,
            context_window=1028*8,
            request_timeout=3600,
            keep_alive="25m"
            )
    return llm

def get_model_main(model_name=None):
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
    provider = get_provider()

    if provider ==  Provider.OLLAMA :
        Settings.context_windows= 8192
        llm = Ollama(
                model=model_name.replace("ollama/", ""),
                base_url = base_url,
                num_ctx=1024*32,
                context_window=1028*8,
                request_timeout=3600,
                keep_alive="25m"
                )
    elif provider == Provider.OPENAI:
        llm = OpenAI(
                model=model_name.replace("openai/", ""),
                api_base = base_url,
                api_key=get_api_key(),
                num_ctx=8192,
                request_timeout=3600,
                keep_alive="25m")
        
    return llm

