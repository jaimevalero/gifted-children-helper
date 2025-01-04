from loguru import logger
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import Document  # Importamos Document correctamente desde llama_index.schema # Importamos Document correctamente desde llama_index.schema
from gifted_children_helper.utils.models import get_model
import os
import pickle
from crewai.tools import tool
import uuid  # Importamos uuid para generar identificadores únicos

def save_index_file(index, file_path):
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

def read_text_file(file_path):
    """
    Read a text file and return its content as a list of Document instances.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of Document instances.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Generamos un identificador único para cada documento y creamos instancias de Document
        return [Document(text=content, doc_id=str(uuid.uuid4()))]
    except Exception as e:
        logger.error("Failed to read text file {}: {}", file_path, e)
        return []

def query_file(question, file_path, save_index=True):
    """
    Query a document (PDF or text) with a given question.

    Args:
        question (str): The question to ask.
        file_path (str): The path to the document.

    Returns:
        str: The response text from the query.
    """
    BASE_PATH = os.path.expanduser("~/git/gifted-children-helper/knowledge/external_docs/books")
    if not file_path.startswith(BASE_PATH):
        file_path = os.path.join(BASE_PATH, file_path)
    
    # Assert that the file exists
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return None
    
    try:
        # Ensure the tmp directory exists
        tmp_dir = os.path.expanduser("~/tmp")
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
            logger.info("Created directory {}", tmp_dir)

        # Construct the index file path
        index_file_name = os.path.basename(file_path).replace(".pdf", "_index.pkl").replace(".txt", "_index.pkl")
        index_path = os.path.join(tmp_dir, index_file_name)

        DEFAULT_MODEL = 'gpt-3.5-turbo' 
        # Define model for embeddings and for the answering 
        if Settings.llm.model == DEFAULT_MODEL : 

            # Settings.llm = get_model_main(embed_aux_model_name)
            Settings.llm = get_model("AUX")
            Settings.embed_model = get_model("EMBED")
        
        if os.path.exists(index_path):
            index = load_index(index_path)
        else:
            if file_path.endswith(".pdf"):
                reader = SimpleDirectoryReader(input_files=[file_path])
                data = reader.load_data()
            elif file_path.endswith(".txt") or file_path.endswith(".txt.temp"):
                data = read_text_file(file_path)
            else:
                logger.error(f"Unsupported file type: {file_path}")
                return None
            
            logger.info(f"File data loaded successfully {file_path=}")
            index = VectorStoreIndex.from_documents(data, show_progress=True)
            if save_index:
                save_index_file(index, index_path)
        
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)

        logger.info(f"Querying {file_path=} with question: {question=}")

        try:
            response = query_engine.query(question)
            response.print_response_stream()
            return response.response_txt
        except Exception as e:
            logger.error("Error during query execution: {}", e)
            return None
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error loading file {file_path=}: {e}")
        if "openai" in str(e).lower():
            logger.error("It seems you have exceeded your OpenAI quota, but you are using Ollama. Please check your configuration.")
        elif "ollama" in str(e).lower():
            logger.error("There was an issue with the Ollama service. Please check your network connection and configuration.")
        return None

@tool("Consultar un libro sobre altas capacidades en niños.")
def ask_altas_capacidades_en_ninos(question:str) -> str:
    """Consultar el libro: altas capacidades en niños. """
    return query_file(question, file_path="altas_capacidades_en_niños.pdf")

@tool("Barreras en el entorno escolar para alumnos de altas capacidades")    
def ask_barreras_entorno_escolar_alumnos_altas_capacidades(question:str) -> str:
    """ Consultar el libro: Barreras en el entorno escolar para alumnos de altas capacidades """
    return query_file(question, file_path="barreras_entorno_escolar_alumnos_altas_capacidades.pdf")


@tool("Manual de atención al alumnado con necesidades específicas de apoyo educativo")
def ask_manual_necesidades_especificas(question: str) -> str:
    """Consultar el libro : Manual de atención al alumnado con necesidades específicas de apoyo educativo."""
    return query_file(question, file_path="manual_de_atencion_al_alumnado_con_necesidades_especificas.pdf")

@tool("La integración sensorial en el desarrollo y aprendizaje infantil")
def ask_integracion_sensorial(question: str) -> str:
    """Consultar el libro: La integración sensorial en el desarrollo y aprendizaje infantil."""
    return query_file(question, file_path="integracion_sensorial_en_el_desarrollo_y_aprendizaje_infantil.pdf")


@tool("Terapia Cognitivo Conductual Aplicada A Niños Y Adolescentes")
def ask_terapia_cognitivo_conductual(question: str) -> str:
    """Consultar el libro: Terapia Cognitivo Conductual Aplicada A Niños Y Adolescentes."""
    return query_file(question, file_path="terapia_cognitivo_conductual_aplicada_a_niños_y_adolescentes.txt")

def test_text_file(file_path="~/git/gifted-children-helper/knowledge/external_docs/books/TerapiaCognitivoConductualAplicadaANinosYAdolescdentes.txt",save_index=False):
    """
    Test the query_file function with a predefined text file and question.
    """
    # Expand the file path
    file_path =  os.path.expanduser(file_path)
    question = """ Quien es el autor o autores de este libro y que conclusiones se pueden sacar de el?"""
    response = query_file(question, file_path,save_index)
    logger.info("Response: {}", response)

def test_find_error_in_file(file_path):
    """
    Find the error in the file by iteratively reading lines and testing the file.

    Args:
        file_path (str): The path to the text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        for i in range(35, len(lines) + 1):  # Start from the first line
            temp_file_path = f"{file_path}.temp"
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                temp_file.writelines(lines[:i])
            
            logger.info("Testing with first {} lines", i)
            try:
                test_text_file(temp_file_path)
            except Exception as e:
                logger.error("Error found with first {} lines: {}", i, e)
                break
    except Exception as e:
        logger.error("Failed to read the file: {}", e)
        raise e

def test_all_files():
    FILES= [
        "altas_capacidades_en_niños.pdf",
        "barreras_entorno_escolar_alumnos_altas_capacidades.pdf",
        "integracion_sensorial_en_el_desarrollo_y_aprendizaje_infantil.pdf",
        "manual_de_atencion_al_alumnado_con_necesidades_especificas.pdf",
        "terapia_cognitivo_conductual_aplicada_a_niños_y_adolescentes.txt",
        ]
    for file in FILES:
        test_text_file(file,save_index=False)

if __name__ == "__main__":
   test_all_files()