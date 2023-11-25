from django.shortcuts import render
from django.shortcuts import render
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from book.models import Reader
from dotenv import load_dotenv
import os

# Create your views here.
def send_email_to_readers(request):
    """
    Sends an email to all readers registered in the database.

    :param request: Django request object.
    :return: Rendering response or redirection.
    """
    # Retrieve all readers from the database
    readers = Reader.objects.all()

     # Get sender credentials from environment variables
    _ = load_dotenv('keys.env')
    sender_email = os.environ.get('sender_email')
    password = os.environ.get('password')

    # Define the message to be sent
    subject = "BookNexus - Newsletter Octubre"
    body = """\
        <html>
            <body>
                <img src="https://github.com/jhothinnan/Images/blob/main/Newsletter.png?raw=true" alt="Newsletter">
            </body>
        </html>
        """ 

    # Create an instance of an SMTP server with SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)

        for reader in readers:
            receiver_email = reader.email 
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            text = MIMEText(body, "html")

            message.attach(text)

            server.sendmail(sender_email, receiver_email, message.as_string())

    # Redirect to a confirmation page
    return render(request, 'email_sent_confirmation.html')
