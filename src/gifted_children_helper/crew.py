from datetime import datetime
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from loguru import logger
import os 
from crewai import Agent, LLM

def get_model(model_name=None):
    # Get the model from the environment variable or use a default value
    model_name = model_name or os.getenv("MODEL_NAME")
    if not model_name:
        model_name = "ollama/llama3.1:8b"
    base_url = os.getenv("API_BASE","http://127.0.0.1:11434/")
    return LLM(
        base_url=base_url,
        model=model_name,
    )

@CrewBase
class GiftedChildrenHelper():
    """GiftedChildrenHelper crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def psychologist(self) -> Agent:
        logger.info("Initializing psychologist agent")
        return Agent(
            config=self.agents_config['psychologist'],
            verbose=True
        )

    @agent
    def educational_advisor(self) -> Agent:
        logger.info("Initializing educational advisor agent")
        return Agent(
            config=self.agents_config['educational_advisor'],
            model=get_model(),
            verbose=True
        )

    @agent
    def activity_coordinator(self) -> Agent:
        logger.info("Initializing activity coordinator agent")
        return Agent(
            config=self.agents_config['activity_coordinator'],
            model=get_model(),
            verbose=True
        )

    @agent
    def social_skills_coach(self) -> Agent:
        logger.info("Initializing social skills coach agent")
        return Agent(
            config=self.agents_config['social_skills_coach'],
            model=get_model(),
            verbose=True
        )

    @agent
    def parent_advisor(self) -> Agent:
        logger.info("Initializing parent advisor agent")
        return Agent(
            config=self.agents_config['parent_advisor'],
            model=get_model(),
            verbose=True
        )

    # @agent
    # def researcher(self) -> Agent:
    #     logger.info("Initializing researcher agent")
    #     return Agent(
    #         config=self.agents_config['researcher'],
    #         model=get_model(),
    #         verbose=True
    #     )

    @agent
    def sensory_specialist(self) -> Agent:
        logger.info("Initializing sensory specialist agent")
        return Agent(
            config=self.agents_config['sensory_specialist'],
            model=get_model(),
            verbose=True
        )

    @agent
    def coordinator(self) -> Agent:
        logger.info("Initializing coordinator agent")
        return Agent(
            config=self.agents_config['coordinator'],
            model=get_model(),
            verbose=True
        )

    @task
    def case_evaluation(self) -> Task:
        logger.info("Initializing case evaluation task")
        return Task(
            config=self.tasks_config['case_evaluation'],
        )

    @task
    def sensory_assessment(self) -> Task:
        logger.info("Initializing sensory assessment task")
        return Task(
            config=self.tasks_config['sensory_assessment'],
        )

    @task
    def intervention_planning(self) -> Task:
        logger.info("Initializing intervention planning task")
        return Task(
            config=self.tasks_config['intervention_planning'],
        )

    @task
    def generate_report(self) -> Task:
        logger.info("Task: generate_report")
        # Generate filename for the output file logs/report-yyyy-mm-dd-hh-mm.md
        if "logs" not in os.listdir():
            os.mkdir("logs")
        # Remove if exists logs/last_report.md
        if os.path.exists("logs/last_report.md"):
            os.remove("logs/last_report.md")

        task = Task(
            config=self.tasks_config['generate_report']
        )
        # Copy the last report in logs/last_report.md to logs/report-yyyy-mm-dd-hh-mm.md
        filename = "logs/report-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".md"
        if os.path.exists("logs/last_report.md"):
            with open("logs/last_report.md", "r") as src:
                with open(filename, "w") as dst:
                    dst.write(src.read())        
        return task
    
    @crew
    def crew(self) -> Crew:
        """Creates the GiftedChildrenHelper crew"""
        logger.info("Creating the GiftedChildrenHelper crew")
        return Crew(
            agents=self.agents[:-1], # All but last agent, which is the manager
            tasks=self.tasks,
            verbose=True,
            embedder= {
                "provider": "ollama",
                "config": {
                    "model": "mxbai-embed-large"
                }    
            },        
            process=Process.hierarchical,
            #process=Process.sequential,

            manager_agent=self.agents[-1], # The aforementioned manager
            planning=False            
        )
