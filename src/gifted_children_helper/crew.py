from datetime import datetime
import os
from loguru import logger
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from gifted_children_helper.tools.custom_pdf_search_tool import ask_altas_capacidades_en_ninos, ask_barreras_entorno_escolar_alumnos_altas_capacidades, ask_integracion_sensorial, ask_manual_necesidades_especificas, ask_terapia_cognitivo_conductual
from gifted_children_helper.utils.models import get_embed_model_name, get_model, get_model_name
from gifted_children_helper.utils.connection_webui import communicate_task_gui
import inspect
from gifted_children_helper.utils.reports import convert_markdown_to_pdf




@CrewBase
class GiftedChildrenHelper():
    """GiftedChildrenHelper crew"""

    def __init__(self, task_callback: callable = None):
        self.task_callback = task_callback
        super().__init__()

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tasks_done = 0 # 2 because the first are not counted

    MAX_EXECUTION_TIMEOUT=1200
    model_name = get_model_name()

    def callback_function(self,output):
        self.tasks_done += 1
        total_tasks = len(self.tasks)
        percentage_progress = self.tasks_done / total_tasks

        progress_message = f"""
({self.tasks_done}/{total_tasks}) Acabado el informe del {output.agent}.\n
{output.raw}
        """
        logger.info(progress_message)
        self.task_callback(progress_message, percentage_progress)

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
    def clinical_psychology_assessment(self) -> Task:
        logger.info("Initializing clinical psychology assessment task")
        return Task(
            config=self.tasks_config['clinical_psychology_assessment'],
            callback=self.callback_function,
        )

    @task
    def neurological_assessment(self) -> Task:
        logger.info("Initializing neurological assessment task")
        return Task(
            config=self.tasks_config['neurological_assessment'],
            callback=self.callback_function,
        )

    @task
    def occupational_therapy_assessment(self) -> Task:
        logger.info("Initializing occupational therapy assessment task")
        return Task(
            config=self.tasks_config['occupational_therapy_assessment'],
            callback=self.callback_function,
        )

    @task
    def educational_psychology_assessment(self) -> Task:
        logger.info("Initializing educational psychology assessment task")
        return Task(
            config=self.tasks_config['educational_psychology_assessment'],
            callback=self.callback_function,
        )

    @task
    def family_therapy_assessment(self) -> Task:
        logger.info("Initializing family therapy assessment task")
        return Task(
            config=self.tasks_config['family_therapy_assessment'],
            callback=self.callback_function,
        )


    @task
    def activity_planning_assessment(self) -> Task:
        logger.info("Initializing activity planning assessment task")
        return Task(
            config=self.tasks_config['activity_planning_assessment'],
            context=[
                self.clinical_psychology_assessment(),
                self.neurological_assessment(),
                self.occupational_therapy_assessment(),
                self.educational_psychology_assessment(),
                self.family_therapy_assessment(),
            ],
            callback=self.callback_function,
        )

    def generate_consolidated_report(self,session_id):
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
        contenido_final = report_content
        
        markdown_filename = "logs/last_report.md"
        if os.path.exists(markdown_filename):
            os.remove(markdown_filename)
        with open(markdown_filename, "w") as report_file:
            report_file.write(contenido_final)
        # Generate un temp file with a unique name the content in pdf format. Return it
        if session_id:
            pdf_filename = f"logs/{session_id}.pdf" 
        else :
            pdf_filename = f"logs/last_report.pdf"
        
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)
                              
        convert_markdown_to_pdf(markdown_filename, pdf_filename)
        logger.info(f"Consolidated report generated and saved to {pdf_filename}")
        return pdf_filename
    
    @crew
    def crew(self) -> Crew:
        """Creates the GiftedChildrenHelper crew"""
        logger.info("Creating the GiftedChildrenHelper crew")

        cordinator_role = 'Coordinador del gabinete'
        non_manager_agents = [ agent  for agent in self.agents if agent.role != cordinator_role] 
        manager_agent = [ agent  for agent in self.agents if agent.role == cordinator_role][0]
        embed_model_name = get_embed_model_name()

        # Get provider from model name
        default_model = get_model_name()
        provider = "ollama" if "ollama" in default_model else "openai"

        crew = Crew(
            agents=non_manager_agents,
            tasks=self.tasks,
            
            embedder= {
                "provider": provider,
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