from loguru import logger
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def send_mail_sendgrid(file_path: str, user_email: str, user_name: str) -> bool:
    """
    Send an email with a PDF or Markdown attachment using SendGrid.

    Args:
        file_path (str): Path to the file to be sent.
        user_email (str): Recipient's email address.
        user_name (str): Recipient's name.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    logger.info(f"Preparing to send email to {user_email} with attachment {file_path}")

    # Validate that the file exists and is not empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        logger.error(f"File {file_path} does not exist or is empty")
        return False

    # Validate that SENDGRID_API_KEY is set
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        logger.error("SENDGRID_API_KEY is not set in the environment variables")
        return False

    sendgrid_from_email = os.getenv('SENDGRID_FROM_EMAIL')

    # Determine the file type and set the appropriate content type and filename
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        file_type = 'application/pdf'
        attachment_filename = 'last_report.pdf'
    elif file_extension == '.md':
        file_type = 'text/markdown'
        attachment_filename = 'last_report.md'
    else:
        logger.error(f"Unsupported file type: {file_extension}")
        return False

    # Read the file
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Encode the file to base64
    encoded_file = base64.b64encode(file_data).decode()

    # Create the attachment
    attachment = Attachment(
        FileContent(encoded_file),
        FileName(attachment_filename),
        FileType(file_type),
        Disposition('attachment')
    )

    # Create the email
    message = Mail(
        from_email=sendgrid_from_email,
        to_emails=user_email,
        subject='Su informe de resultados',
        html_content=f"""
        <html>
        <body>
            <p>Estimado/a {user_name}:</p>
            <p>Adjuntamos el informe de evaluación. Esperamos sea de utilidad.</p>
            <p>Atentamente</p>
            <p>El equipo de guiding families</p>
        </body>
        </html>
        """
    )
    message.attachment = attachment

    try:
        # Send the email
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        logger.info(f"Email sent to {user_email} with status code {response.status_code}")
        return response.status_code == 202
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {e}")
        return False
