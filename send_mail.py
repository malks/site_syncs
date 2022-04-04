#!/usr/bin/python3
from smtplib import SMTP
from email.message import EmailMessage
import os

home=str(os.path.expanduser("~"))
f=open(os.path.join(os.path.expanduser("~"),".smtp_auth"),"r")
  
authdata={}
msg = EmailMessage()

for x in f:
  authdata[str(x.split("=")[0]).strip()]=str(x.split("=")[1]).strip()

def send_mail(data):
    server_smtp=SMTP(authdata["SERVER"],authdata["PORT"])
    server_smtp.connect(authdata["SERVER"],authdata["PORT"])
    server_smtp.ehlo()
    server_smtp.starttls()
    server_smtp.ehlo()
    server_smtp.login(authdata["USER"],authdata["PASSWORD"])
    msg["Subject"] = "Contato Site"
    msg["From"] = "noreply@lunelli.com.br"
    msg["To"] = "support@grupolunelli.zendesk.com"
    message=""
    message+="Formulário de dúvidas do Site lunelli.com.br\n\n"
    message+="Nome: "+data["00N4W00000S0yWc"]+"\n"
    message+="Email: "+data["email"]+"\n"
    message+="Fone: ("+data["00N4W00000S0yWW"]+") "+data["00N4W00000S0yX1"]"\n"
    message+="Mensagem: "+data["description"]+"\n"
    msg.set_content(message)
    server_smtp.send_message(msg)
    ret=server_smtp.quit()
    print(ret)