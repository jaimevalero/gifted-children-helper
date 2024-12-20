import os
import shutil
from loguru import logger
from datetime import datetime

def copy_report(*args, **kwargs):
    """ 
    Given a newly generated report, "logs/last_report.md"
    copy it to "logs/report-yyyy-mm-dd-hh-mm.md"
    """
    # Log the arguments received
    logger.info(f"Args: {args}, Kwargs: {kwargs}")
    
    # Generate filename for the output file logs/report-yyyy-mm-dd-hh-mm.md
    filename = f"logs/report-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.md"
    
    # Copy the report to the new filename
    shutil.copy("logs/last_report.md", filename)
    
    # Log the successful copy operation
    logger.info(f"Report copied to {filename}")

