from datetime import datetime
import os
from loguru import logger
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from gifted_children_helper.tools.custom_pdf_search_tool import ask_altas_capacidades_en_ninos, ask_barreras_entorno_escolar_alumnos_altas_capacidades, ask_integracion_sensorial, ask_manual_necesidades_especificas, ask_terapia_cognitivo_conductual
from gifted_children_helper.utils.models import Provider,  get_model,  get_model_name, get_provider
import inspect
from gifted_children_helper.utils.reports import convert_markdown_to_pdf




@CrewBase
class GiftedChildrenHelper():
    """GiftedChildrenHelper crew"""

    def __init__(self, task_callback: callable = None, session_id: str = None):
        self.task_callback = task_callback
        self.session_id = session_id

        super().__init__()

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tasks_done = 0 # 2 because the first are not counted

    MAX_EXECUTION_TIMEOUT=1200
    model_name = get_model_name("MAIN")

    def step_callback(self,step_output):
        
        text = None
        try:
            # If step_output is an AgentFinish object, , get the text from the agent output 
            if hasattr(step_output, 'text'):
                result_formatted = step_output.text
                result_formatted = result_formatted.replace("```markdown","").replace("```","").replace("*","")
                result_formatted = next((line.split('Thought:')[1].strip() for line in step_output.text.split('\n') if 'Thought:' in line), "")
                if "\n" in result_formatted:
                    result_formatted = result_formatted.split("\n")[0]
                text = f"*Acción finalizada: {result_formatted}*" 
            elif hasattr(step_output, 'result'):
                # If there is no text attribute, exit the function
                if not hasattr(step_output.result, 'text'):
                    return
                result_formatted = step_output.text
                result_formatted = result_formatted.replace("```markdown","").replace("```","").replace("*","")
                # Coger solo hasta el primer salto de línea "\n"
                if "\n" in result_formatted:
                    result_formatted = result_formatted.split("\n")[0]
                text = f"*Respuesta bibliográfica: {result_formatted}*"
            if text:
                logger.info(f"Step output: {text}")
                # Coger solo hasta el primer salto de línea "\n"
                self.task_callback(text,self.session_id)
        except Exception as e:
            logger.error(f"Error in step callback: {e}")        

    def callback_function(self,output):
        try :
            self.tasks_done += 1
            total_tasks = len(self.tasks)
            percentage_progress = self.tasks_done / total_tasks

            progress_message = f"""{output.raw}""".replace("```markdown","").replace("```","")
            title = f"({self.tasks_done}/{total_tasks}) Acabado el informe del {output.agent}"
            logger.info(progress_message)
            self.task_callback(progress_message, percentage_progress,title,self.session_id)
        except Exception as e:
            logger.error(f"Error in callback function: {e}")

    @agent
    def clinical_psychologist(self) -> Agent:

        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
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
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
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
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
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
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") )

    @agent
    def neurologist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
            tools=[ask_altas_capacidades_en_ninos,
                   ] )

    @agent
    def occupational_therapist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
            tools=[ask_integracion_sensorial] )
            
  

    @agent
    def educational_psychologist(self) -> Agent:
        agent_name = inspect.currentframe().f_code.co_name
        logger.info(f"Initializing {agent_name} agent")
        config = self.agents_config[agent_name]
        config["llm"] = self.model_name

        return Agent(
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
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
            step_callback=self.step_callback,
            config=config,
            model = get_model("MAIN") ,
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
                              
        try :
            convert_markdown_to_pdf(markdown_filename, pdf_filename)

            logger.info(f"Consolidated report generated and saved to {pdf_filename}")
            return pdf_filename
        except Exception as e:
            logger.error(f"Error generating pdf: {e}")
            return markdown_filename
    
    @crew
    def crew(self) -> Crew:
        """Creates the GiftedChildrenHelper crew"""
        logger.info("Creating the GiftedChildrenHelper crew")

        cordinator_role = 'Coordinador del gabinete'
        non_manager_agents = [ agent  for agent in self.agents if agent.role != cordinator_role] 
        manager_agent = [ agent  for agent in self.agents if agent.role == cordinator_role][0]
        embed_model_name = get_model_name("EMBED")
        
        provider = "ollama" if get_provider("MAIN") == Provider.OLLAMA else "openai"
        
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