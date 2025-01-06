import os

from crewai import LLM
from loguru import logger
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from langchain_openai import ChatOpenAI

from llama_index.llms.ollama import Ollama as ollama_aux
#from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama

#from openai import OpenAI # Use for deepseek

# from langchain_community.llms.openai import OpenAI # NO VALE
# from langchain_openai.llms.base import OpenAI # NO VALE
from llama_index.core import Settings
from enum import Enum

class Provider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

 

def get_provider(model_type) -> Provider:
    """
    Get the provider from the model name.
    
    Returns:
        Provider: The provider enum value.
    """
    model_type = model_type.upper()

    if model_type not in ["MAIN", "AUX", "EMBED"]:
        raise ValueError(f"Provider not recognized for model {model_type}")
    
    provider_string =  os.environ[f"{model_type}_PROVIDER"] 

    
    if "ollama" in provider_string:
        provider = Provider.OLLAMA
    elif "openai" in provider_string or 'deepseek-chat' in provider_string:
        provider = Provider.OPENAI
    else:
        raise ValueError(f"Provider not recognized for model {provider_string}")
    
    #logger.info(f"Provider determined: {provider}")
    return provider

def get_api_key(model_type):
    """
    Retrieve the API key from the environment variable.

    Returns:
        str: The API key.
    """
    model_type = model_type.upper()
    if model_type not in ["MAIN", "AUX", "EMBED"]:
        raise ValueError(f"Provider not recognized for model {model_type}")
    
    return os.getenv(f"{model_type}_TOKEN", None)

    
def get_model_name(model_type):
    """
    Retrieve the embedding model name from the environment variable.

    Returns:
        str: The name of the embedding model. 
    """
    model_type = model_type.upper()
    if model_type not in ["MAIN", "AUX", "EMBED"]:
        raise ValueError(f"Provider not recognized for model {model_type}")
    
    if not os.getenv(f"{model_type}_MODEL_NAME"):
        raise ValueError(f"{model_type}_MODEL_NAME environment variable not set")
    return os.getenv(f"{model_type}_MODEL_NAME")

def get_api_base(model_type):
    """
    Retrieve the api name from the environment variable.

    Returns:
        str: The name of the api. 
    """
    model_type = model_type.upper()
    if model_type not in ["MAIN", "AUX", "EMBED"]:
        raise ValueError(f"Provider not recognized for model {model_type}")
    
    if not os.getenv(f"{model_type}_API_BASE"):
        raise ValueError(f"{model_type}_MODEL_NAME environment variable not set")
    return os.getenv(f"{model_type}_API_BASE")




def __get_model_embed():

    model_type = "EMBED"
    model_name = get_model_name(model_type).replace("openai/deepseek-chat", "")
    base_url = get_api_base(model_type)   
    provider = get_provider(model_type)

    #provider =  Provider.OLLAMA
    if provider ==  Provider.OLLAMA :
        embed_model = OllamaEmbedding(
                model_name=model_name.replace("ollama/", ""),
                base_url=base_url,
                num_ctx=8192,
                request_timeout=3600,
                keep_alive="25m",
                ollama_additional_kwargs={
                    "prostatic": 0, 
                    "num_ctx" : 8192},
            )      
    elif provider == Provider.OPENAI:
        api_key = get_api_key(model_type)
        embed_model =OpenAIEmbedding(
                model_name=model_name.replace("openai/", ""),
                api_key=api_key,
                api_base=base_url,
                num_ctx=8192,
                request_timeout=3600,
                keep_alive="25m",
            )

    
    return embed_model


def __get_model_aux():
    model_type = "AUX"

    model_name = get_model_name(model_type)
    base_url = get_api_base(model_type)   
    provider = get_provider(model_type) 
    if provider ==  Provider.OLLAMA :
        llm = Ollama(
            model=model_name.replace("ollama/", ""),
            base_url = base_url,
            num_ctx=1024*32,
            context_window=1028*8,
            request_timeout=3600,
            keep_alive="25m"
            )
    elif provider == Provider.OPENAI:
        api_key = get_api_key(model_type)
        
        llm = ChatOpenAI(
                    model="deepseek-chat", 
                    openai_api_key=api_key, 
                    openai_api_base='https://api.deepseek.com',
                    max_tokens=8192        )  
    return llm 

def get_model(model_type):

    if model_type == "EMBED":
        return __get_model_embed()
    elif model_type == "AUX":
        return __get_model_aux()
    
    model_name = get_model_name(model_type)
    base_url = get_api_base(model_type)   
    provider = get_provider(model_type) 
    if provider ==  Provider.OLLAMA :
        llm = Ollama(
            model=model_name.replace("ollama/", ""),
            base_url = base_url,
            num_ctx=1024*32,
            context_window=1028*8,
            request_timeout=3600,
            keep_alive="25m"
            )
    elif provider == Provider.OPENAI:
        api_key = get_api_key(model_type)
        os.environ['DEEPSEEK_API_KEY'] = api_key
        llm = LLM(model=model_name,
                  max_tokens=8192,
                  timeout=25*60,
                  )

    return llm

# if main, execute __get_model_embed()
# if __name__ == "__main__":
#     __get_model_embed()