# Gabinete de ayuda psicológica para niños de altas capacidades

Simulación de gabinete psicológico de ayuda integral a las familias de niños de altas capacidades.
Powered by [crewAI](https://crewai.com). 

Esta aplicación de inteligencia artificial simula un gabinete psicológico, especializado en familias con niños de altas capacidades. Utiliza [agentes](src/gifted_children_helper/config/agents.yaml) y [tareas](src/gifted_children_helper/config/tasks.yaml) configurados para proporcionar informes detallados y personalizados basados en la información proporcionada por los usuarios.

## Especialistas (agentes) y sus Informes (tareas)

El gabinete cuenta con un equipo multidisciplinar de especialistas, cada uno generando informes específicos:

### Psicólogo Clínico
- **Rol**: Evaluación psicológica completa y diagnóstico
- **Informe**: Análisis detallado incluyendo diagnóstico, recomendaciones familiares y propuestas de intervención domiciliaria

### Neurólogo Pediatra
- **Rol**: Evaluación del desarrollo neurológico
- **Informe**: Valoración neurológica completa con recomendaciones para estimulación neurológica en casa

### Terapeuta Ocupacional
- **Rol**: Especialista en integración sensorial y regulación conductual
- **Informe**: Evaluación de integración sensorial, análisis conductual y plan de actividades de autorregulación

### Psicopedagogo
- **Rol**: Especialista en adaptaciones curriculares y necesidades educativas
- **Informe**: Evaluación psicopedagógica con propuestas de adaptación curricular y estrategias de estudio

### Terapeuta Familiar
- **Rol**: Experto en dinámica familiar y orientación
- **Informe**: Análisis de la dinámica familiar con estrategias de mejora y recomendaciones

### Asesor Educativo
- **Rol**: Coordinación con centros educativos y adaptaciones curriculares
- **Informe**: Propuestas específicas de adaptación al sistema educativo

### Coordinador de Actividades
- **Rol**: Planificación de actividades extraescolares y recursos
- **Informe**: Plan personalizado de actividades con cronograma y recursos necesarios

### Coordinador del Gabinete
- **Rol**: Supervisión y coordinación del equipo multidisciplinar
- **Informe**: Integración de todas las evaluaciones en un plan de intervención coordinado

Cada especialista genera informes profesionales en pdf, proporcionando una visión integral del caso y recomendaciones específicas para implementación tanto en el entorno familiar como educativo.

## Installation
First, you need to install the packages listed on the packages.txt (debian)

```bash
sudo apt-get install $(cat packages.txt)
```

Then, use python 3.10 and pip to install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application, run the following command:

```bash
streamlit run src/streamlit/frontend.py --server.port=8501 --server.address=0.0.0.0
```

## Example Report

Puedes descargar un reporte de ejemplo ficticio para ver el tipo de informe que genera la aplicación.
[Descargar reporte de ejemplo](src/streamlit/static/example_report.pdf)

## Authentication and Terms of Service

Para acceder a la aplicación, los usuarios deben autenticarse utilizando sus credenciales. Además, es importante que los usuarios lean y acepten los términos de servicio antes de utilizar la aplicación.

## Licencia

Este proyecto está licenciado bajo la Licencia Pública Internacional Creative Commons Atribución-NoComercial 4.0. Para más detalles, consulte el archivo [LICENSE](LICENSE).
