import os
import shutil
from loguru import logger
from datetime import datetime
import subprocess

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
        # Execute the pandoc command to convert Markdown to PDF
        command = ['pandoc', markdown_file, '-o', pdf_file, '-V', 'geometry:margin=1in']

        subprocess.run(command, check=True)
        logger.info("Converted {} to {}", markdown_file, pdf_file)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to convert {} to PDF: {}", markdown_file, e)
    except Exception as e:
        logger.error("An unexpected error occurred: {}", e)

# Example usage
# convert_markdown_to_pdf('logs/last_report.md', 'logs/last_report.pdf')
