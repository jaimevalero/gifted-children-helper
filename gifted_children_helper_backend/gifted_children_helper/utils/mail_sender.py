from loguru import logger
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def send_mail_sendgrid(pdf_file: str, user_email: str, user_name: str) -> bool:
    """
    Send an email with a PDF attachment using SendGrid.

    Args:
        pdf_file (str): Path to the PDF file to be sent.
        user_email (str): Recipient's email address.
        user_name (str): Recipient's name.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    logger.info(f"Preparing to send email to {user_email} with attachment {pdf_file}")

    # Validate that the PDF file exists and is not empty
    if not os.path.exists(pdf_file) or os.path.getsize(pdf_file) == 0:
        logger.error(f"PDF file {pdf_file} does not exist or is empty")
        return False

    # Validate that SENDGRID_API_KEY is set
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        logger.error("SENDGRID_API_KEY is not set in the environment variables")
        return False
    sendgrid_from_email = os.getenv('SENDGRID_FROM_EMAIL')
    # Read the PDF file
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()

    # Encode the PDF file to base64
    encoded_pdf = base64.b64encode(pdf_data).decode()

    # Create the attachment
    attachment = Attachment(
        FileContent(encoded_pdf),
        FileName('last_report.pdf'),  # Use the desired filename here
        FileType('application/pdf'),
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
