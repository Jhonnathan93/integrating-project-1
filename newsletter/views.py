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
    # Obtén todos los lectores de la base de datos
    readers = Reader.objects.all()

    _ = load_dotenv('keys.env')
    sender_email = os.environ.get('sender_email')
    password = os.environ.get('password')

    # Define el mensaje que se enviará
    subject = "BookNexus - Newsletter Octubre"
    body = """\
        <html>
            <body>
                <img src="https://github.com/jhothinnan/Images/blob/main/Newsletter.png?raw=true" alt="Newsletter">
            </body>
        </html>
        """ 

    # Crea una instancia de un servidor SMTP con SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Inicia sesión en tu cuenta de Gmail
        server.login(sender_email, password)

        for reader in readers:
            receiver_email = reader.email  # Obtiene el correo del lector
            # Crea un mensaje MIMEText
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            # Crea la parte de texto del mensaje
            text = MIMEText(body, "html")

            # Adjunta la parte de texto al mensaje
            message.attach(text)

            # Envía el correo al lector
            server.sendmail(sender_email, receiver_email, message.as_string())

    # Redirige a una página de confirmación u otra vista
    return render(request, 'email_sent_confirmation.html')
