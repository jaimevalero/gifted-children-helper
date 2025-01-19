from loguru import logger
from crewai.tasks.task_output import TaskOutput

def communicate_task_gui(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    
    logger.info(f"""
        Task completed!
        Task: {output.description}
        Output: {output.raw}
    """)