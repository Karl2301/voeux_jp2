import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def send_email(subject, recipient, body):
    sender_email = "krahuel@immacjp2.fr"
    sender_password = "Leju8369"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attacher le corps du message en HTML
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False

def generate_otp():
    return random.randint(100000, 999999)

def send_password_reset_email(recipient, token):
    subject = "Réinitialisation de votre mot de passe"
    body = f"""
    <html>
    <body>
        <p>Bonjour,</p>
        <p>Veuillez cliquer sur le bouton ci-dessous pour réinitialiser votre mot de passe :</p>
        <a href="https://whatsupp.aekio.fr/new_password/{token}" style="
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            padding: 10px 20px;
            text-decoration: none;
            font-size: 16px;
            border-radius: 5px;
        ">Réinitialiser le mot de passe</a>
        <p>Cordialement,<br>Votre équipe.</p>
    </body>
    </html>
    """
    return send_email(subject, recipient, body)

def send_otp_email(recipient, otp):
    subject = "Code de vérification"
    body = f"""
    <html>
    <body>
        <p>Bonjour,</p>
        <p>Votre code de vérification est : <strong>{otp}</strong></p>
        <p>Cordialement,<br>Votre équipe.</p>
    </body>
    </html>
    """
    return send_email(subject, recipient, body)
