import os
from email.message import EmailMessage
import ssl
import smtplib

from dotenv import load_dotenv
load_dotenv()

EM_PASS = os.getenv("EM_PASS")



def submit_user_feedback(feedback_str):
    email_sender = 'sgovindgari@gmail.com'
    email_password = EM_PASS
    email_reciever = 'sgovindgari@gmail.com'

    subject = 'SpecMe new user feedback'
    body = feedback_str

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())