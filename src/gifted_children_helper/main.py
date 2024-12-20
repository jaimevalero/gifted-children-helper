#!/usr/bin/env python
import sys
import warnings

from loguru import logger

from gifted_children_helper.crew import GiftedChildrenHelper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
def get_case():
    case = """
Tengo un niño de altas capacidades de 8 años que en la escuela se porta muy mal, a decir de los profesores. Es alborotador y muy inquieto.
El niño dice que se aburre en la escuela porque le repiten muchas veces las cosas y el lo entiendo a la primera. No tiene adaptación curricular.
Sus padres le hicieron las pruebas para TDAH hace dos años y salió negativo. Si, dió positivo en altas capacidades.
De aficiones, le gusta la geología y la historia, y hacer experimentos en casa, pero los fines de semana los pasa en casa de su abuela, que no tiene movilidad para ir a sitios, y solo una vez al mes va con sus padres de excursión.
"""
    return case

def run():
    """
    Run the crew.
    """
    inputs = {
        'case' : get_case()
    }
    GiftedChildrenHelper().crew().kickoff(inputs=inputs)


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
