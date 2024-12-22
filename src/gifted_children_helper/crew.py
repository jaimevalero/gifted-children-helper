from datetime import datetime
import os
from loguru import logger
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from gifted_children_helper.tools.custom_pdf_search_tool import ask_altas_capacidades_en_ninos, ask_barreras_entorno_escolar_alumnos_altas_capacidades, ask_modelos_adaptacion_curricular, ask_normativa_adaptacion_curricular_madrid
from src.gifted_children_helper.utils.reports import copy_report  # type: ignore
from gifted_children_helper.utils.models import get_embed_model_name, get_model

@CrewBase
class GiftedChildrenHelper():
    """GiftedChildrenHelper crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    MAX_EXECUTION_TIMEOUT=900

    @agent
    def clinical_psychologist(self) -> Agent:
        logger.info("Initializing psychologist agent")
        return Agent(
            config=self.agents_config['clinical_psychologist'],
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]

        )

    @agent
    def educational_advisor(self) -> Agent:
        logger.info("Initializing educational advisor agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,
            config=self.agents_config['educational_advisor'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos,
                   ask_modelos_adaptacion_curricular]
        )

    @agent
    def activity_coordinator(self) -> Agent:
        logger.info("Initializing activity coordinator agent")
        return Agent(
            config=self.agents_config['activity_coordinator'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]
        )

    @agent
    def coordinator(self) -> Agent:
        logger.info("Initializing coordinator agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,
            config=self.agents_config['coordinator'],
            model=get_model(),
            verbose=True
        )

    @agent
    def clinical_psychologist(self) -> Agent:
        logger.info("Initializing clinical psychologist agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,
            config=self.agents_config['clinical_psychologist'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]
        )

    @agent
    def neurologist(self) -> Agent:
        logger.info("Initializing neurologist agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,            
            config=self.agents_config['neurologist'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]
        )

    @agent
    def occupational_therapist(self) -> Agent:
        logger.info("Initializing occupational therapist agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,            
            config=self.agents_config['occupational_therapist'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]
        )

    @agent
    def educational_psychologist(self) -> Agent:
        logger.info("Initializing educational psychologist agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,            
            config=self.agents_config['educational_psychologist'],
            model=get_model(),
            verbose=True,
            tools=[
                ask_altas_capacidades_en_ninos,
                ask_normativa_adaptacion_curricular_madrid,
                ask_barreras_entorno_escolar_alumnos_altas_capacidades,
                ask_modelos_adaptacion_curricular
                ]
        )

    @agent
    def family_therapist(self) -> Agent:
        logger.info("Initializing family therapist agent")
        return Agent(
            max_execution_time = self.MAX_EXECUTION_TIMEOUT,            
            config=self.agents_config['family_therapist'],
            model=get_model(),
            verbose=True,
            tools=[ask_altas_capacidades_en_ninos]
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

    # @task
    # def integration_planning(self) -> Task:
    #     logger.info("Task: integration_planning")
    #     # Generate filename for the output file logs/report-yyyy-mm-dd-hh-mm.md
    #     if "logs" not in os.listdir():
    #         os.mkdir("logs")
    #     filename = f"logs/report-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.md"
    #     # Remove if exists logs/last_report.md
    #     if os.path.exists("logs/last_report.md"):
    #         os.remove("logs/last_report.md")
        
    #     task = Task(
    #         config=self.tasks_config['integration_planning'],
    #         # context=[
    #         #     self.clinical_psychology_assessment(),
    #         #     self.neurological_assessment(),
    #         #     self.occupational_therapy_assessment(),
    #         #     self.educational_psychology_assessment(),
    #         #     self.family_therapy_assessment(),
    #         #     self.activity_planning_assessment()],
    #         callback=copy_report,
    #         output_file=filename
    #     )
    
    #     return task
        
    def generate_consolidated_report(self):
        """
        Generate a consolidated report from all task outputs and save it to last_reports.md.
        """
        logger.info("Generating consolidated report")

        # Initialize the report content
        report_content = ""

        # Iterate over the tasks and collect their outputs
        for task in self.crew.tasks[1:-1]:  # Exclude the first and last tasks
            task_name = task.config['name']
            task_output = task.output.raw
            report_content += f"# Informe {task_name.replace('_', ' ').title()}\n\n{task_output}\n\n"

        # Instructions for the LLM
        instructions = """
        Asegúrate de que todo el informe esté en español.
        Por cada tarea, añade un título de primer nivel con el nombre de la tarea.
        Formatea el informe en Markdown.
        """

        # Use the LLM to generate the final report
        llm = get_model()
        final_report = llm.generate(f"{instructions}\n\n{report_content}", language="es")

        # Save the final report to last_reports.md
        with open("logs/last_reports.md", "w") as report_file:
            report_file.write(final_report)

        logger.info("Consolidated report generated and saved to logs/last_reports.md")

    @crew
    def crew(self) -> Crew:
        """Creates the GiftedChildrenHelper crew"""
        logger.info("Creating the GiftedChildrenHelper crew")

        cordinator_role = 'Coordinador del gabinete'
        non_manager_agents = [ agent  for agent in self.agents if agent.role != cordinator_role] 
        manager_agent = [ agent  for agent in self.agents if agent.role == cordinator_role][0]
        embed_model_name = get_embed_model_name()

        crew = Crew(
            agents=non_manager_agents,
            tasks=self.tasks,
            verbose=True,
            embedder= {
                "provider": "ollama",
                "config": {
                    "model": embed_model_name
                }    
            },        
            process=Process.hierarchical,
            manager_agent=manager_agent,
            planning=False,
            language="es"
        )
        
        logger.info("GiftedChildrenHelper crew created successfully")
        return crew
