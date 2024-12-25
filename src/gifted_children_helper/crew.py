from datetime import datetime
import os
from loguru import logger
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from gifted_children_helper.tools.custom_pdf_search_tool import ask_altas_capacidades_en_ninos, ask_barreras_entorno_escolar_alumnos_altas_capacidades, ask_integracion_sensorial, ask_manual_necesidades_especificas,  ask_terapia_cognitivo_conductual
#from src.gifted_children_helper.utils.reports import copy_report  # type: ignore
from gifted_children_helper.utils.models import get_embed_model_name, get_model, get_model_name

import inspect


@CrewBase
class GiftedChildrenHelper():
    """GiftedChildrenHelper crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    MAX_EXECUTION_TIMEOUT=1200
    model_name = get_model_name()

    @agent
    def clinical_psychologist(self) -> Agent:

        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[ask_altas_capacidades_en_ninos,
                   ask_terapia_cognitivo_conductual]

        )

    @agent
    def educational_advisor(self) -> Agent:

        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[
                    ask_barreras_entorno_escolar_alumnos_altas_capacidades,
                    ask_altas_capacidades_en_ninos,
                    ask_manual_necesidades_especificas,
                   ] )
    
 
    @agent
    def activity_coordinator(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[
                    ask_barreras_entorno_escolar_alumnos_altas_capacidades,
                    ask_altas_capacidades_en_ninos,
                    ask_manual_necesidades_especificas,
                   ]    )


    @agent
    def coordinator(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() )

    @agent
    def clinical_psychologist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[ask_altas_capacidades_en_ninos,
                   ask_terapia_cognitivo_conductual] )

    @agent
    def neurologist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[ask_altas_capacidades_en_ninos,
                   ] )

    @agent
    def occupational_therapist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[ask_integracion_sensorial] )
            
  

    @agent
    def educational_psychologist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[
                ask_altas_capacidades_en_ninos,
                ask_manual_necesidades_especificas,
                ask_barreras_entorno_escolar_alumnos_altas_capacidades,
                ]
        )

    @agent
    def family_therapist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            config=config,
            model = get_model() ,
            tools=[
                ask_altas_capacidades_en_ninos,
                ask_barreras_entorno_escolar_alumnos_altas_capacidades,
                ask_terapia_cognitivo_conductual
            ]
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
        Generate a consolidated report from all task outputs and save it to last_report.md.
        """
        logger.info("Generating consolidated report")

        # Initialize the report content
        report_content = ""

        # Iterate over the tasks and collect their outputs
        for i,task in enumerate(self.tasks[1:-1],start=1):
            task_name = task.name
            task_output = task.output.raw
            report_content += f"# {i} Informe: {task_name.replace('_', ' ').title()}\n\n{task_output}\n\n"
        report_content = report_content.replace("```markdown","").replace("```","")
            # Instructions for the LLM
        instructions = f"""
        Eres un maquetista documentador de informes de evaluación psicológicos.
        Para el informe que te paso al final debes
        1) Asegúrate de que todo el informe esté en español.
        2) Por cada tarea, añade un título de primer nivel con el nombre de la tarea.
        3) Formatea el informe en Markdown para que quede cohesivo. 
        4) Importante, no quites nada. 
        5) Responde solo con el informe formateado. El informe es {report_content}:
        """

        # Use the LLM to generate the final report
        try :
            llm = get_model()
            contenido_final = llm.complete(f"{instructions}")
        except Exception as e:
            contenido_final = report_content
        # Save the final report to last_report.md
        # delte the last report if exists
        if os.path.exists("logs/last_report.md"):
            os.remove("logs/last_report.md")
        with open("logs/last_report.md", "w") as report_file:
            report_file.write(contenido_final)

        logger.info("Consolidated report generated and saved to logs/last_report.md")

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
            
            embedder= {
                "provider": "ollama",
                "config": {
                    "model": embed_model_name
                }    
            },        
            process=Process.sequential,
            manager_agent=manager_agent,
            planning=False,
            language="es"
        )
        
        logger.info("GiftedChildrenHelper crew created successfully")
        return crew
