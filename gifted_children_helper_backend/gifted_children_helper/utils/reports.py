import os
import shutil
from loguru import logger
from datetime import datetime
import subprocess
import psutil  # Import psutil for system monitoring

def copy_report(*args, **kwargs):
    """ 
    Given a newly generated report, "logs/last_report.md"
    copy it to "logs/report-yyyy-mm-dd-hh-mm.md"
    """
    try:
        # Log the arguments received
        logger.info("Args: {}, Kwargs: {}", args, kwargs)
        
        # Generate filename for the output file logs/report-yyyy-mm-dd-hh-mm.md
        filename = f"logs/report-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.md"
        
        # Copy the report to the new filename
        shutil.copy("logs/last_report.md", filename)
        
        # Log the successful copy operation
        logger.info("Report copied to {}", filename)

    except Exception as e:
        # Log the exception
        logger.error("An error occurred while copying the report: {}", e)

def convert_markdown_to_pdf(markdown_file, pdf_file):
    """
    Convert a Markdown file to PDF using pandoc.

    Args:
        markdown_file (str): The path to the Markdown file.
        pdf_file (str): The path to the output PDF file.
    """
    try:
        logger.info(f"Converting {markdown_file} to {pdf_file}")
        # Execute the pandoc command to convert Markdown to PDF
        #command = ['pandoc', markdown_file, '-o', pdf_file, '-V', 'geometry:margin=1in']
        command = [
            'pandoc',
            markdown_file,
            '-o', pdf_file,
            '--pdf-engine=pdflatex',  # Más ligero que el motor por defecto
            '-V', 'geometry:margin=1in',
            '--standalone',  # Procesa más rápido documentos independientes
            '-f', 'markdown-raw_html',  # Deshabilita parsing innecesario
            '--variable=papersize:a4',  # Especifica tamaño papel explícitamente
            '+RTS', '-N2', '-RTS'  # Usar 2 threads para procesamiento
        ]        
        # Capture stdout and stderr
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Log the successful conversion
        logger.info(f"Converted {markdown_file} to {pdf_file} with output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Log the error with stdout and stderr
        logger.error(f"Failed to convert {markdown_file} to {pdf_file}: {e}")
        raise e
    except Exception as e:
        # Log any unexpected errors
        logger.error("An unexpected error occurred: {}", e)
        raise e

def log_system_usage():
    """
    Log the system's CPU and memory usage.
    """
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    logger.info("Memory usage: RSS = {} MB, VMS = {} MB", memory_info.rss / (1024 * 1024), memory_info.vms / (1024 * 1024))
    logger.info("CPU usage: {}%", psutil.cpu_percent(interval=1))

# Example usage
# convert_markdown_to_pdf('logs/last_report.md', 'logs/last_report.pdf')
