# GiftedChildrenHelper Crew

Demo de gabinete de ayuda integral a las familias de niños de altas capacidades
powered by [crewAI](https://crewai.com). 

## Context

Esta aplicación de inteligencia artificial simula un gabinete psicológico, especializado en familias con niños de altas capacidades. Utiliza [agentes](src/gifted_children_helper/config/agents.yaml) y [tareas](src/gifted_children_helper/config/tasks.yaml) configurados para proporcionar informes detallados y personalizados basados en la información proporcionada por los usuarios.

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


To start the Streamlit application, run the following command:
```bash
streamlit run src/streamlit/frontend.py --server.port=8501 --server.address=0.0.0.0
```

## Example Report

Puedes descargar un reporte de ejemplo ficticio para ver el tipo de informe que genera la aplicación.
[Descargar reporte de ejemplo](https://example.com/reporte-ejemplo.pdf)

## Authentication and Terms of Service

Para acceder a la aplicación, los usuarios deben autenticarse utilizando sus credenciales. Además, es importante que los usuarios lean y acepten los términos de servicio antes de utilizar la aplicación.
