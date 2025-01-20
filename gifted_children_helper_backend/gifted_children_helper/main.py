#!/usr/bin/env python
import sys
import warnings
import os
from gifted_children_helper_backend.gifted_children_helper.utils.secrets import load_secrets
from loguru import logger
from dotenv import load_dotenv

from gifted_children_helper.crew import GiftedChildrenHelper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
def get_case():
    """ Read file (filename case.lst) and return the case as a string
     ignore empty lines and lines starting with # """
    with open("case.lst") as f:
        lines = f.readlines()
    # Ignore empty lines and lines starting with #
    case = "".join([line for line in lines if line.strip() and not line.startswith("#")])
    case = "<case>" + case + "</case>"
    logger.info(f"Case: {case}")
    return case


def run(case: str = None, callback: callable = None,session_id: str = None):
    """
    Run the crew.
    """
    if not case:
        case = get_case()
    inputs = {
        'case': case
    }
    #load_dotenv()
    ensure_dirs_exist()
    
    try:
        helper = GiftedChildrenHelper(task_callback=callback, session_id=session_id)
        crew = helper.crew()
        crew.kickoff(inputs=inputs)
        # por cada una de las crew.tasks, añadirlo todo a un solo string.
        # Despues , formatearlo para darle uniformidad
        pdf_filename = helper.generate_consolidated_report(session_id)
        # Print token usage
        logger.info(f"Token usage: {crew.usage_metrics}")
        return pdf_filename
        
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {e}")
        logger.exception(e)
        raise Exception(f"An error occurred while running the crew: {e}")
    
def ensure_dirs_exist():
    dirs = ["logs", "tmp"]
    # Ensure the directories exist in the current working directory
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
            logger.info(f"Created directory {dir}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'case' : get_case()
    }
    try:
        GiftedChildrenHelper().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GiftedChildrenHelper().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'case' : get_case()
    }
    try:
        GiftedChildrenHelper().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

if __name__ == "__main__":
    logger.info("Running the main function")
    # Depending on the arguments, run the crew, train the crew, or replay the crew
    #load_dotenv()
    load_secrets()

    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            train()
        elif sys.argv[1] == "replay":
            replay()
        elif sys.argv[1] == "run":
            run()            
        elif sys.argv[1] == "test":
            test()
        else:
            run()
    else:
        run()
    logger.info("Finished running the main function")
