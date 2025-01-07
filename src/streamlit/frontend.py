import sys
import os

# Ugly hack because of https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Add the src directory to PYTHONPATH, because stream cloud expects all paths refered to app file directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from chromadb import Documents
from chromadb import EmbeddingFunction 
from chromadb import Embeddings

import streamlit as st
from loguru import logger
import uuid
from dotenv import load_dotenv
import json
try : 
    from streamlit.auth.authenticate import Authenticator
except:
    from auth.authenticate import Authenticator

# Call load_secrets to initialize secrets
from gifted_children_helper.utils.secrets import load_secrets  # Import the moved function

load_secrets(st)

from gifted_children_helper.main import run



def auth():

    # emails of users that are allowed to login
    allowed_users = os.getenv("ALLOWED_USERS").split(",")

    
    #st.write("## Streamlit Google Auth")

    authenticator = Authenticator(
        allowed_users=allowed_users,
        token_key=os.getenv("TOKEN_KEY"),
        secret_path="client_secret.json",
        # redirect_uri="http://localhost:8501",
        redirect_uri= "https://guiding-families.streamlit.app",
    )
    authenticator.check_auth()
    authenticator.login()


    # show content that requires login
    if st.session_state["connected"]:
        st.write(f"Bienvenido {st.session_state['user_info'].get('email')}")
        logger.info(f"Logado {st.session_state['user_info'].get('email')}")
        if st.button("Log out ❌"):
            authenticator.logout()

    if not st.session_state["connected"]:
        st.warning("Por favor, lógate con google para continuar. Además, solo usuarios autorizados pueden acceder a esta aplicación") 


def mock_google_auth():
    # Mock authentication for demonstration purposes
    logger.debug("Mocking Google authentication")
    st.session_state["connected"] = True
    st.session_state["user_info"] = {"email": "example@example.con"}


def streamlit_callback(message: str= None, progress: float = None, title: str = None):
    """
    Callback function to update progress in Streamlit.
    
    :param message: Message to display.
    :param progress: Progress percentage (0 to 1).
    """
    logger.info(f"Streamlit callback called with message: {message} and progress: {progress}")
    # Convert markdown to html
    if message:
        st.markdown(message)
    
    if progress is not None:
        # if "progress_bar" not in st.session_state:
        #     st.session_state.progress_bar = st.progress(0)
        progress = min(1.0, max(0.0, progress))  # Ensure progress is between 0 and 1   
        st.session_state.progress_bar.progress(progress)
        # If there is a title, update the text
    if title:
        st.session_state.progress_bar.text(title)

def call_crew_ai(case, session_id, streamlit_callback):
    # Initialize the progress bar before starting tasks
    logger.info("Calling Crew AI with session ID: {}", session_id)
    if "progress_bar" not in st.session_state:
        st.session_state.progress_bar = st.progress(0)
    
    st.toast("Generando el informe. Esto tarda varios minutos. Por favor, espere")
    # Aquí puedes llamar a la función de Crew.ai y pasar el callback
    # Ejemplo de uso del callback:


    streamlit_callback("Iniciando contacto con la ia...", 0.1,"Iniciando contacto con la ia...")

    # Ejecuta el run del modulo gifted_children_helper.main
    pdf_filename = run(case, streamlit_callback,session_id)

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
</nav>""", unsafe_allow_html=True)

def main():
    # Add the navigation bar
    add_navbar()

    # Set the title of the Streamlit app
    logger.info("Starting Streamlit app")

    # Información de la aplicación y enlace al reporte de ejemplo
    st.info("""Esta aplicación de inteligencia artificial simula un gabinete psicológico, especializado en familias con niños de altas capacidades.

Por favor, completa el formulario para generar un informe psicológico.
[Descargar reporte de ejemplo ficticio.](https://github.com/jaimevalero/gifted-children-helper/raw/master/src/streamlit/static/example_report.pdf)

            """)
    st.info("""            
No olvides logarte con google y aceptar los términos del servicio.""")
    
    # Load the CSS from the static file
    css_file_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Generate a UUID for the session if not already present
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Add text areas for user input with lighter placeholder text
    if "description" not in st.session_state:
        st.session_state.description = ""
    if "family_dynamics" not in st.session_state:
        st.session_state.family_dynamics = ""
    if "emotional_behavior" not in st.session_state:
        st.session_state.emotional_behavior = ""
    if "skills_development" not in st.session_state:
        st.session_state.skills_development = ""
    if "school_context" not in st.session_state:
        st.session_state.school_context = ""
    if "problems_difficulties" not in st.session_state:
        st.session_state.problems_difficulties = ""
    if "additional_observations" not in st.session_state:
        st.session_state.additional_observations = ""

    st.session_state.description = st.text_area("1. Descripción del Niño/a", value=st.session_state.description, placeholder="""
Incluye edad, lugar de residencia, personalidad, y características principales.
Ejemplo: 
Juan es un niño de 8 años que vive en Madrid con su hermano Enrique de 11. Es un niño muy curioso, con gran interés por la astronomía y los videojuegos. A menudo hace preguntas complejas sobre el universo y muestra un vocabulario avanzado para su edad.
""")

    st.session_state.family_dynamics = st.text_area("2. Dinámica Familiar", value=st.session_state.family_dynamics, placeholder="""
Describe cómo interactúa con la familia, rutinas en casa, y relación con hermanos.
Ejemplo: 
En casa, Juan mantiene una relación cercana con su madre, quien lo apoya en sus proyectos escolares. Sin embargo, suele discutir con su hermano Enrique, quien a veces se siente desplazado por la atención que recibe Juan debido a sus logros académicos. Los padres tratan de mantener un equilibrio, pero a menudo enfrentan dificultades para atender las necesidades de ambos hijos.
""")

    st.session_state.emotional_behavior = st.text_area("3. Comportamiento y Manejo Emocional", value=st.session_state.emotional_behavior, placeholder="""
Explica cómo se comporta en diferentes situaciones y gestiona sus emociones.
Ejemplo: 
Juan suele frustrarse cuando no logra alcanzar la perfección en sus proyectos o cuando se siente incomprendido por sus compañeros en el colegio. Tiende a aislarse cuando está molesto, aunque responde bien a actividades estructuradas como clases de música. Su autoestima es alta en lo académico, pero se muestra inseguro en interacciones sociales.
""")

    st.session_state.skills_development = st.text_area("4. Habilidades y Desarrollo", value=st.session_state.skills_development, placeholder="""
Describe las habilidades del niño/a y áreas de desarrollo (académico, físico, creativo, social).
Ejemplo: 
Juan destaca en matemáticas y ciencias, resolviendo problemas avanzados para su edad. Ha comenzado a escribir cuentos breves y muestra creatividad en su forma de narrar. Sin embargo, en actividades deportivas se siente menos capaz y evita participar en juegos de equipo, lo que afecta su integración social.
""")

    st.session_state.school_context = st.text_area("5. Contexto Escolar y Extraescolar", value=st.session_state.school_context, placeholder="""
Comenta sobre su progreso académico y actividades fuera de la escuela.
Ejemplo: 
En el colegio, Juan suele aburrirse con tareas repetitivas y ha manifestado interés por proyectos más desafiantes. Participa en un taller de robótica después de clases, donde trabaja con estudiantes mayores y disfruta la experiencia. Sus profesores reconocen su talento, pero a veces no saben cómo manejar sus necesidades específicas.
""")

    st.session_state.problems_difficulties = st.text_area("6. Problemas y Situaciones Difíciles", value=st.session_state.problems_difficulties, placeholder="""
Indica los problemas principales y cuándo suelen ocurrir.
Ejemplo: 
Juan se siente aislado socialmente, ya que sus compañeros lo perciben como "diferente" debido a su forma de expresarse y sus intereses. En casa, las tensiones con su hermano mayor son frecuentes, especialmente en actividades compartidas como juegos de mesa. Su madre señala que Juan tiene dificultades para manejar la frustración y aceptar críticas constructivas.
""")

    st.session_state.additional_observations = st.text_area("7. Observaciones Adicionales", value=st.session_state.additional_observations, placeholder="""
Añade cualquier otro detalle que consideres importante.
Ejemplo: 
Juan tiene un gran interés por aprender programación y ha comenzado a explorar plataformas en línea. Sus padres están preocupados por su exceso de tiempo frente a pantallas y buscan formas de equilibrar sus actividades tecnológicas con experiencias al aire libre. También mencionan que Juan muestra interés por participar en programas para niños de altas capacidades.
""")

    # Mock authentication
    

    # Count words in all text areas
    total_words = count_words(st.session_state.description, st.session_state.family_dynamics, st.session_state.emotional_behavior, st.session_state.skills_development, st.session_state.school_context, st.session_state.problems_difficulties, st.session_state.additional_observations)
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
        data_policy_accepted = st.checkbox("Acepto los términos de servicio y la política de privacidad", value=debug_mode)


    # Add footer with link to source code
    footer_html = """<div style='text-align: right;'>
      <p>Desarrollado con ❤️ para <a href="https://www.asociacionamaci.com/" target="_blank">AMACI</a></p>
    </div>"""

    # Si no se han aceptado los terminos del servicio, no permita enviar el formulario, y poner un st.error
    # Ojo que al principio no debe mostrar el error, solo cuando se intente enviar el formulario
    if not data_policy_accepted:
        st.error("Por favor, acepta los términos de servicio para continuar.")

    # If is LOCAL environent variable is set to 1, mock the google auth
    if os.getenv("LOCAL","0") == "1":
        mock_google_auth()    
    else:
        auth()

    try :
        if not st.session_state["connected"]:
            authorized = False
        else:
            authorized = True
    except:
        authorized = False
                 
    if st.button("Generar informe 📝", disabled=send_button_disabled or not data_policy_accepted or not authorized):
        # Initialize the case variable
        case = ""

        # Append each section if the associated text is not empty
        if st.session_state.description:
            case += f"**Descripción del Niño/a:** {st.session_state.description}\n"
        if st.session_state.family_dynamics:
            case += f"**Dinámica Familiar:** {st.session_state.family_dynamics}\n"
        if st.session_state.emotional_behavior:
            case += f"**Comportamiento y Manejo Emocional:** {st.session_state.emotional_behavior}\n"
        if st.session_state.skills_development:
            case += f"**Habilidades y Desarrollo:** {st.session_state.skills_development}\n"
        if st.session_state.school_context:
            case += f"**Contexto Escolar y Extraescolar:** {st.session_state.school_context}\n"
        if st.session_state.problems_difficulties:
            case += f"**Problemas y Situaciones Difíciles:** {st.session_state.problems_difficulties}\n"
        if st.session_state.additional_observations:
            case += f"**Observaciones Adicionales:** {st.session_state.additional_observations}\n"
        
        report_filename = call_crew_ai(case, st.session_state.session_id, streamlit_callback)
        
        # Set progress to 100% after completion
        streamlit_callback("Informe generado con éxito.", 1.0)

        st.toast("Acabado el informe, descarguelo para verlo")

        # Ensure the file is only accessible to the current user
        if os.path.exists(report_filename):
            # if report ends with .pdf, the mime = "application/pdf"
            # else, if reports ends with .md, the mime = "text/markdown"
            mime = "application/pdf" if report_filename.endswith(".pdf") else "text/markdown"
            file_name = "informe_final.pdf" if report_filename.endswith(".pdf") else "informe_final.md"
            with open(report_filename, "rb") as file:
                st.download_button(
                    label="Descargar informe 📥",  # Added download icon
                    data=file,
                    file_name=file_name, 
                    mime=mime
                )
            
            
    # Log the current app mode
    logger.info("End of render")


    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
