from datetime import datetime
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from loguru import logger
import os 
from crewai import Agent, LLM
from src.gifted_children_helper.utils.reports import copy_report # type: ignore

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
    def clinical_psychologist(self) -> Agent:
        logger.info("Initializing psychologist agent")
        return Agent(
            config=self.agents_config['clinical_psychologist'],
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
    def coordinator(self) -> Agent:
        logger.info("Initializing coordinator agent")
        return Agent(
            config=self.agents_config['coordinator'],
            model=get_model(),
            verbose=True
        )

    @agent
    def clinical_psychologist(self) -> Agent:
        logger.info("Initializing clinical psychologist agent")
        return Agent(
            config=self.agents_config['clinical_psychologist'],
            model=get_model(),
            verbose=True
        )

    @agent
    def neurologist(self) -> Agent:
        logger.info("Initializing neurologist agent")
        return Agent(
            config=self.agents_config['neurologist'],
            model=get_model(),
            verbose=True
        )

    @agent
    def occupational_therapist(self) -> Agent:
        logger.info("Initializing occupational therapist agent")
        return Agent(
            config=self.agents_config['occupational_therapist'],
            model=get_model(),
            verbose=True
        )

    @agent
    def educational_psychologist(self) -> Agent:
        logger.info("Initializing educational psychologist agent")
        return Agent(
            config=self.agents_config['educational_psychologist'],
            model=get_model(),
            verbose=True
        )

    @agent
    def family_therapist(self) -> Agent:
        logger.info("Initializing family therapist agent")
        return Agent(
            config=self.agents_config['family_therapist'],
            model=get_model(),
            verbose=True
        )

    @task
    def initial_case_evaluation(self) -> Task:
        logger.info("Initializing initial case evaluation task")
        return Task(
            config=self.tasks_config['initial_case_evaluation'],
        )

    @task
    def clinical_psychology_assessment(self) -> Task:
        logger.info("Initializing clinical psychology assessment task")
        return Task(
            config=self.tasks_config['clinical_psychology_assessment'],
        )

    @task
    def neurological_assessment(self) -> Task:
        logger.info("Initializing neurological assessment task")
        return Task(
            config=self.tasks_config['neurological_assessment'],
        )

    @task
    def occupational_therapy_assessment(self) -> Task:
        logger.info("Initializing occupational therapy assessment task")
        return Task(
            config=self.tasks_config['occupational_therapy_assessment'],
        )

    @task
    def educational_psychology_assessment(self) -> Task:
        logger.info("Initializing educational psychology assessment task")
        return Task(
            config=self.tasks_config['educational_psychology_assessment'],
        )

    @task
    def family_therapy_assessment(self) -> Task:
        logger.info("Initializing family therapy assessment task")
        return Task(
            config=self.tasks_config['family_therapy_assessment'],
        )

    @task
    def activity_planning_assessment(self) -> Task:
        logger.info("Initializing activity planning assessment task")
        return Task(
            config=self.tasks_config['activity_planning_assessment'],
        )


    @task
    def integration_planning(self) -> Task:
        logger.info("Task: integration_planning")
        # Generate filename for the output file logs/report-yyyy-mm-dd-hh-mm.md
        if "logs" not in os.listdir():
            os.mkdir("logs")
        # Remove if exists logs/last_report.md
        if os.path.exists("logs/last_report.md"):
            os.remove("logs/last_report.md")
        
        task = Task(
            config=self.tasks_config['integration_planning'],
#            context=[self.research_candidates_task(), self.match_and_score_candidates_task(), self.outreach_strategy_task()],
            callback=copy_report
        )
    
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
            manager_agent=self.agents[-1], # The aforementioned manager
            planning=False            
        )
