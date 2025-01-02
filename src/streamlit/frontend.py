import streamlit as st
import requests
from fpdf import FPDF
import time
from loguru import logger
import uuid
import os
from gifted_children_helper.main import run
from dotenv import load_dotenv

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

def main():
    # Set the title of the Streamlit app
    logger.info("Starting Streamlit app")
    st.title("Formulario para Informe Psicológico")
    st.write("Esta aplicación simula, mediante inteligencia artificial, un gabinete psicológico especializado en familias con niños/as de altas capacidades.")
    st.write("Completa el formulario para generar un informe psicológico.")
    
    # Add a button to toggle dark mode with an icon
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    def toggle_dark_mode():
        st.session_state.dark_mode = not st.session_state.dark_mode

    st.sidebar.button("🌙 Modo oscuro", on_click=toggle_dark_mode)

    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            body {
                background-color: #121212;
                color: #f0f0f0;
            }
            .stTextArea textarea {
                background-color: #333;
                color: #f0f0f0;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px;
            }
            .stButton button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            .stButton button:hover {
                background-color: #45a049;
            }
            .stSidebar .css-1d391kg {
                background-color: #333;
            }
            .stSidebar .css-1d391kg .css-1v3fvcr {
                color: #f0f0f0;
            }
            .stSidebar .css-1d391kg .css-1v3fvcr:hover {
                color: #4CAF50;
            }
            .stTextArea label {
                font-size: 18px;
                font-weight: bold;
                color: #f0f0f0;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Load the CSS from the static file
        css_file_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
        with open(css_file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Generate a UUID for the session if not already present
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Add text areas for user input with lighter placeholder text
    description = st.text_area("1. Descripción del Niño/a", placeholder="Incluye edad, lugar de residencia, personalidad, y características principales...", height=100)
    family_dynamics = st.text_area("2. Dinámica Familiar", placeholder="Describe cómo interactúa con la familia, rutinas en casa, y relación con hermanos...", height=100)
    emotional_behavior = st.text_area("3. Comportamiento y Manejo Emocional", placeholder="Explica cómo se comporta en diferentes situaciones y gestiona sus emociones...", height=100)
    skills_development = st.text_area("4. Habilidades y Desarrollo", placeholder="Describe las habilidades del niño/a y áreas de desarrollo (académico, físico, creativo, social)...", height=100)
    school_context = st.text_area("5. Contexto Escolar y Extraescolar", placeholder="Comenta sobre su progreso académico y actividades fuera de la escuela...", height=100)
    problems_difficulties = st.text_area("6. Problemas y Situaciones Difíciles", placeholder="Indica los problemas principales y cuándo suelen ocurrir...", height=100)
    additional_observations = st.text_area("7. Observaciones Adicionales", placeholder="Añade cualquier otro detalle que consideres importante...", height=100)

    # Mock authentication
    email = mock_google_auth()
    st.sidebar.markdown(f"**Usuario autenticado:** {email}")

    # Count words in all text areas
    total_words = count_words(description, family_dynamics, emotional_behavior, skills_development, school_context, problems_difficulties, additional_observations)
    st.sidebar.write(f"Total words: {total_words}")

    MINIMUN_WORDS = 200 
    debug_mode = os.getenv("DEBUG") == "1" # Check if DEBUG mode is enabled
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

    # Si no se han aceptado los terminos del servicio, no permita enviar el formulario, y poner un st.error
    # Ojo que al principio no debe mostrar el error, solo cuando se intente enviar el formulario
    if not data_policy_accepted:
        st.error("Por favor, acepta los términos de servicio para continuar.")

    if st.button("Generar informe", disabled=send_button_disabled or not data_policy_accepted):
        # Call Crew.ai with session ID and all text areas
        #st.write("**Generando informe:**")

        case = f""" 
        **Descripción del Niño/a:** {description}
        **Dinámica Familiar:** {family_dynamics}
        **Comportamiento y Manejo Emocional:** {emotional_behavior}
        **Habilidades y Desarrollo:** {skills_development}
        **Contexto Escolar y Extraescolar:** {school_context}
        **Problemas y Situaciones Difíciles:** {problems_difficulties}
        **Observaciones Adicionales:** {additional_observations}
        """
        
        pdf_filename = call_crew_ai(case, st.session_state.session_id, streamlit_callback)
        
        # Set progress to 100% after completion
        streamlit_callback("Informe generado con éxito.", 1.0)

        # Ensure the file is only accessible to the current user
        if os.path.exists(pdf_filename):
            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="Descargar informe",
                    data=file,
                    file_name="informe_final.pdf",  # Specify the desired download name
                    mime="application/pdf"
                )
        
    # Log the current app mode
    logger.info("Current app mode: Generar Informe")

if __name__ == "__main__":
    main()
