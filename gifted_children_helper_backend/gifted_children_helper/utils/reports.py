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
        
        # Capture stdout and stderr
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Log the successful conversion
        logger.info("Converted {} to {}", markdown_file, pdf_file)
    except subprocess.CalledProcessError as e:
        # Log the error with stdout and s   tderr
        logger.error("Failed to convert {} to PDF: {}\nstdout: {}\nstderr: {}", markdown_file, e, e.stdout, e.stderr)
        raise e
    except Exception as e:
        # Log any unexpected errors
        logger.error("An unexpected error occurred: {}", e)
        raise e

# Example usage
# convert_markdown_to_pdf('logs/last_report.md', 'logs/last_report.pdf')
