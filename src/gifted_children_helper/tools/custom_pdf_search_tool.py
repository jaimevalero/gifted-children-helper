from loguru import logger
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from gifted_children_helper.utils.models import get_base_url, get_model, get_embed_model, get_model_name

from llama_index.llms.ollama import Ollama



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
        Settings.llm = Ollama(
            model = get_model_name().replace("ollama/", ""),
            config = {
                "ollama_base_url" : get_base_url()
            }
        )        
        Settings.embed_model = get_embed_model()

        
        reader = SimpleDirectoryReader(input_files=[pdf_path])
        data = reader.load_data()
        logger.info("PDF data loaded successfully")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)
        logger.info("Query engine created successfully")

        response = query_engine.query(question)
        response.print_response_stream()
        a = 0
    except Exception as e:
        logger.exception(e)
        if "openai" in str(e).lower():
            logger.error("It seems you have exceeded your OpenAI quota, but you are using Ollama. Please check your configuration.")

# Define the PDF file path
pdf_path = "/home/jaimevalero/git/gifted-children-helper/knowledge/external_docs/books/Altas capacidades en niños.pdf"

# Define the question
question = """
Dime falsas creencias sobre el alumnado de altas capacidades. Show statements in bullet form """

# Query the PDF
query_pdf(question, pdf_path)


