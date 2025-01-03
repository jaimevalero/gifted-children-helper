import streamlit as st
import requests
from fpdf import FPDF
import time
from loguru import logger
import uuid
import os
from gifted_children_helper.main import run
from dotenv import load_dotenv
from streamlit.components.v1 import html

# Load environment variables
load_dotenv()

def mock_google_auth():
    # Mock authentication for demonstration purposes
    logger.info("Mocking Google authentication")
    st.session_state["user_email"] = "user_mock@example.com"
    return st.session_state["user_email"]

def streamlit_callback(message: str, progress: float = None):
    """
    Callback function to update progress in Streamlit.
    
    :param message: Message to display.
    :param progress: Progress percentage (0 to 1).
    """
    logger.info(f"Streamlit callback called with message: {message} and progress: {progress}")
    # Convert markdown to html
    st.markdown(message)
    
    if progress is not None:
        if "progress_bar" not in st.session_state:
            st.session_state.progress_bar = st.progress(0)
        progress = min(1.0, max(0.0, progress))  # Ensure progress is between 0 and 1   
        st.session_state.progress_bar.progress(progress)

def call_crew_ai(case, session_id, callback):
    # Initialize the progress bar before starting tasks
    logger.info("Calling Crew AI with session ID: {}", session_id)
    if "progress_bar" not in st.session_state:
        st.session_state.progress_bar = st.progress(0)
    
    st.write("Generando el informe. Esto tarda varios minutos. Por favor, espere")
    # Aquí puedes llamar a la función de Crew.ai y pasar el callback
    # Ejemplo de uso del callback:


    callback("Iniciando contacto con la ia...", 0.1)
    case = ""
    # Ejecuta el run del modulo gifted_children_helper.main
    pdf_filename = run(case, callback,session_id)

    return pdf_filename




def count_words(*texts):
    # Count the total number of words in the provided texts
    logger.info("Counting words in provided texts")
    return sum(len(text.split()) for text in texts)

def load_terms_and_policy():
    # Load the terms of service and privacy policy from an external file
    logger.info("Loading terms of service and privacy policy")
    terms_file_path = os.path.join(os.path.dirname(__file__), 'static', 'terms_and_policy.md')
    with open(terms_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def add_navbar():
    """
    Add a navigation bar to the Streamlit app.
    """
    logger.info("Adding navigation bar to the app")
    st.markdown("""
<nav class="navbar navbar-light bg-light">
  <span class="navbar-brand mb-0 h1">Gabinete integral de psicología</span>
</nav>
    """, unsafe_allow_html=True)

def main():
    # Add the navigation bar
    add_navbar()
    
    # Set the title of the Streamlit app
    logger.info("Starting Streamlit app")

    #st.title("Formulario para Informe Psicológico")
    st.info("""Esta aplicación simula, mediante inteligencia artificial, un gabinete psicológico especializado en familias con niños/as de altas capacidades.

Por favor, completa el formulario para generar un informe psicológico.""")
    
    # Load the CSS from the static file
    css_file_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Generate a UUID for the session if not already present
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Add text areas for user input with lighter placeholder text
    description = st.text_area("1. Descripción del Niño/a", placeholder="""
Incluye edad, lugar de residencia, personalidad, y características principales.
Ejemplo: 
Juan es un niño de 8 años que vive en Madrid con su hermano Enrique de 11. Es un niño muy curioso, con gran interés por la astronomía y los videojuegos. A menudo hace preguntas complejas sobre el universo y muestra un vocabulario avanzado para su edad.
""")

    family_dynamics = st.text_area("2. Dinámica Familiar", placeholder="""
Describe cómo interactúa con la familia, rutinas en casa, y relación con hermanos.
Ejemplo: 
En casa, Juan mantiene una relación cercana con su madre, quien lo apoya en sus proyectos escolares. Sin embargo, suele discutir con su hermano Enrique, quien a veces se siente desplazado por la atención que recibe Juan debido a sus logros académicos. Los padres tratan de mantener un equilibrio, pero a menudo enfrentan dificultades para atender las necesidades de ambos hijos.
""")

    emotional_behavior = st.text_area("3. Comportamiento y Manejo Emocional", placeholder="""
Explica cómo se comporta en diferentes situaciones y gestiona sus emociones.
Ejemplo: 
Juan suele frustrarse cuando no logra alcanzar la perfección en sus proyectos o cuando se siente incomprendido por sus compañeros en el colegio. Tiende a aislarse cuando está molesto, aunque responde bien a actividades estructuradas como clases de música. Su autoestima es alta en lo académico, pero se muestra inseguro en interacciones sociales.
""")

    skills_development = st.text_area("4. Habilidades y Desarrollo", placeholder="""
Describe las habilidades del niño/a y áreas de desarrollo (académico, físico, creativo, social).
Ejemplo: 
Juan destaca en matemáticas y ciencias, resolviendo problemas avanzados para su edad. Ha comenzado a escribir cuentos breves y muestra creatividad en su forma de narrar. Sin embargo, en actividades deportivas se siente menos capaz y evita participar en juegos de equipo, lo que afecta su integración social.
""")

    school_context = st.text_area("5. Contexto Escolar y Extraescolar", placeholder="""
Comenta sobre su progreso académico y actividades fuera de la escuela.
Ejemplo: 
En el colegio, Juan suele aburrirse con tareas repetitivas y ha manifestado interés por proyectos más desafiantes. Participa en un taller de robótica después de clases, donde trabaja con estudiantes mayores y disfruta la experiencia. Sus profesores reconocen su talento, pero a veces no saben cómo manejar sus necesidades específicas.
""")

    problems_difficulties = st.text_area("6. Problemas y Situaciones Difíciles", placeholder="""
Indica los problemas principales y cuándo suelen ocurrir.
Ejemplo: 
Juan se siente aislado socialmente, ya que sus compañeros lo perciben como "diferente" debido a su forma de expresarse y sus intereses. En casa, las tensiones con su hermano mayor son frecuentes, especialmente en actividades compartidas como juegos de mesa. Su madre señala que Juan tiene dificultades para manejar la frustración y aceptar críticas constructivas.
""")

    additional_observations = st.text_area("7. Observaciones Adicionales", placeholder="""
Añade cualquier otro detalle que consideres importante.
Ejemplo: 
Juan tiene un gran interés por aprender programación y ha comenzado a explorar plataformas en línea. Sus padres están preocupados por su exceso de tiempo frente a pantallas y buscan formas de equilibrar sus actividades tecnológicas con experiencias al aire libre. También mencionan que Juan muestra interés por participar en programas para niños de altas capacidades.
""")

    # Mock authentication
    email = mock_google_auth()
    #st.sidebar.markdown(f"**Usuario autenticado:** {email}")

    # Count words in all text areas
    total_words = count_words(description, family_dynamics, emotional_behavior, skills_development, school_context, problems_difficulties, additional_observations)
    #st.sidebar.write(f"Total words: {total_words}")

    MINIMUN_WORDS = 200 
    debug_mode = os.getenv("LOCAL") == "1" # Check if LOCAL mode is enabled
    minimun_words = 0 if debug_mode else MINIMUN_WORDS
    words_remaining = minimun_words - total_words

    if words_remaining > 0:
        st.error(f"Por favor, escribe al menos {minimun_words} palabras. Faltan {words_remaining} palabras.")
        send_button_disabled = True
    else:
        send_button_disabled = False

    # Load terms of service and privacy policy
    terms_and_policy = load_terms_and_policy()

    with st.expander("Términos de Servicio y Política de Privacidad"):
        st.markdown(terms_and_policy)

    data_policy_accepted = st.checkbox("Acepto los términos de servicio.", value=debug_mode)

    # Add footer with link to source code
    footer_html = """<div style='text-align: right;'>
      <p>Desarrollado con ❤️ para <a href="https://www.asociacionamaci.com/" target="_blank">AMACI</a></p>
    </div>"""

    # Si no se han aceptado los terminos del servicio, no permita enviar el formulario, y poner un st.error
    # Ojo que al principio no debe mostrar el error, solo cuando se intente enviar el formulario
    if not data_policy_accepted:
        st.error("Por favor, acepta los términos de servicio para continuar.")

    if st.button("Generar informe 📝", disabled=send_button_disabled or not data_policy_accepted):
        # Initialize the case variable
        case = ""

        # Append each section if the associated text is not empty
        if description:
            case += f"**Descripción del Niño/a:** {description}\n"
        if family_dynamics:
            case += f"**Dinámica Familiar:** {family_dynamics}\n"
        if emotional_behavior:
            case += f"**Comportamiento y Manejo Emocional:** {emotional_behavior}\n"
        if skills_development:
            case += f"**Habilidades y Desarrollo:** {skills_development}\n"
        if school_context:
            case += f"**Contexto Escolar y Extraescolar:** {school_context}\n"
        if problems_difficulties:
            case += f"**Problemas y Situaciones Difíciles:** {problems_difficulties}\n"
        if additional_observations:
            case += f"**Observaciones Adicionales:** {additional_observations}\n"
        
        pdf_filename = call_crew_ai(case, st.session_state.session_id, streamlit_callback)
        
        # Set progress to 100% after completion
        streamlit_callback("Informe generado con éxito.", 1.0)

        # Ensure the file is only accessible to the current user
        if os.path.exists(pdf_filename):
            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="Descargar informe 📥",  # Added download icon
                    data=file,
                    file_name="informe_final.pdf",  # Specify the desired download name
                    mime="application/pdf"
                )
            
            
    # Log the current app mode
    logger.info("Current app mode: Generar Informe")


    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
