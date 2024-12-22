from loguru import logger
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from gifted_children_helper.utils.models import get_base_url, get_model, get_embed_model, get_model_name
from llama_index.llms.ollama import Ollama
import os
import pickle
from crewai.tools import tool

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
        str: The response text from the query.
    """
    BASE_PATH = os.path.expanduser("~/git/gifted-children-helper/knowledge/external_docs/books")
    if not pdf_path.startswith(BASE_PATH):
        pdf_path = os.path.join(BASE_PATH, pdf_path)
    
    # Assert that the PDF file exists
    
    try:
        # Ensure the tmp directory exists
        tmp_dir = os.path.expanduser("~/tmp")
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
            logger.info("Created directory {}", tmp_dir)

        # Construct the index file path
        index_file_name = os.path.basename(pdf_path).replace(".pdf", "_index.pkl")
        index_path = os.path.join(tmp_dir, index_file_name)

        Settings.llm = Ollama(
            model=get_model_name().replace("ollama/", ""),
            base_url = get_base_url(),
            context_window=5000)
        
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

        logger.info(f"Querying {pdf_path=} with question: {question=}")

        response = query_engine.query(question)
        response.print_response_stream()
        return response.response_txt
    except Exception as e:
        logger.exception(e)
        if "openai" in str(e).lower():
            logger.error("It seems you have exceeded your OpenAI quota, but you are using Ollama. Please check your configuration.")
        return "An error occurred while querying the PDF document."


@tool("Consulta libro sobre altas capacidades en niños.")
def ask_altas_capacidades_en_ninos(question:str) -> str:
    """ Consulta libro sobre altas capacidades en niños. """
    return query_pdf(question, pdf_path="Altas capacidades en niños.pdf")

@tool("Consulta normativa sobre la adaptación curricular en colegios de Madrid, que pueden hacer los colegios para adaptar a los alumnos de altas capacidades")
def ask_normativa_adaptacion_curricular_madrid(question:str) -> str:
    """ Consulta normativa sobre la adaptación curricular en colegios de Madrid. Que pueden hacer los colegios para adaptar a los alumnos de altas capacidades"""
    return query_pdf(question, pdf_path="adaptacion-curricular-normativa.pdf")
    
@tool("Barreras en el entorno escolar para alumnos de altas capacidades")    
def ask_barreras_entorno_escolar_alumnos_altas_capacidades(question:str) -> str:
    """ Barreras en el entorno escolar para alumnos de altas capacidades """
    return query_pdf(question, pdf_path="barreras_entorno_escolar_alumnos_altas_capacidades.pdf")

@tool("Modelos de adaptación curricular")
def ask_modelos_adaptacion_curricular(question:str) -> str:
    """ Modelos de adaptación curricular """
    return query_pdf(question, pdf_path="adaptacion-curricular-ejemplos.pdf")

def test_query_pdf():
    """
    Test the query_pdf function with a predefined PDF and question.
    """
    # Define the PDF file path
    pdf_path = os.path.expanduser("~/git/gifted-children-helper/knowledge/external_docs/books/Altas capacidades en niños.pdf")

    # Define the question
    question = """
    Dime falsas creencias sobre el alumnado de altas capacidades. Show statements in bullet form 
    """

    # Query the PDF
    logger.info("Inicio Querying PDF...")
    response = query_pdf(question, pdf_path)
    logger.info("Finish Querying PDF...")
    logger.info("Response: {}", response)




