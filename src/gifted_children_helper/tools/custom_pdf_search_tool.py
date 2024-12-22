from loguru import logger
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from gifted_children_helper.utils.models import get_base_url, get_model, get_embed_model, get_model_name
from llama_index.llms.ollama import Ollama
import os
import pickle

def save_index(index, file_path):
    """
    Save the index to a file.

    Args:
        index (VectorStoreIndex): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """
    with open(file_path, 'wb') as f:
        pickle.dump(index, f)
    logger.info("Index saved to {}", file_path)

def load_index(file_path):
    """
    Load the index from a file.

    Args:
        file_path (str): The path to the file where the index is saved.

    Returns:
        VectorStoreIndex: The loaded index.
    """
    with open(file_path, 'rb') as f:
        index = pickle.load(f)
    logger.info("Index loaded from {}", file_path)
    return index

def query_pdf(question, pdf_path):
    """
    Query a PDF document with a given question.

    Args:
        question (str): The question to ask.
        pdf_path (str): The path to the PDF document.

    Returns:
        None
    """
    try:
        # Ensure the tmp directory exists
        tmp_dir = "./tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
            logger.info("Created directory {}", tmp_dir)

        # Construct the index file path
        index_file_name = os.path.basename(pdf_path).replace(".pdf", "_index.pkl")
        index_path = os.path.join(tmp_dir, index_file_name)

        Settings.llm = Ollama(
            model=get_model_name().replace("ollama/", ""),
            config={
                "ollama_base_url": get_base_url()
            }
        )
        Settings.embed_model = get_embed_model()

        if os.path.exists(index_path):
            index = load_index(index_path)
        else:
            reader = SimpleDirectoryReader(input_files=[pdf_path])
            data = reader.load_data()
            logger.info("PDF data loaded successfully")
            index = VectorStoreIndex.from_documents(data, show_progress=True)
            save_index(index, index_path)
        
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)
        logger.info("Query engine created successfully")

        response = query_engine.query(question)
        response.print_response_stream()
    except Exception as e:
        logger.exception(e)
        if "openai" in str(e).lower():
            logger.error("It seems you have exceeded your OpenAI quota, but you are using Ollama. Please check your configuration.")

# Define the PDF file path
pdf_path = "/home/jaimevalero/git/gifted-children-helper/knowledge/external_docs/books/Altas capacidades en niños.pdf"

# Define the question
question = """
Dime falsas creencias sobre el alumnado de altas capacidades. Show statements in bullet form 
"""

# Query the PDF
logger.info("Inicio Querying PDF...")
query_pdf(question, pdf_path)
logger.info("Finish Querying PDF...")


