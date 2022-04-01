#!/usr/bin/python3
from smtplib import SMTP
import os

home=str(os.path.expanduser("~"))
f=open(os.path.join(os.path.expanduser("~"),".smtp_auth"),"r")
  
authdata={}

for x in f:
  authdata[str(x.split("=")[0]).strip()]=str(x.split("=")[1]).strip()

def send_mail(data):
    server_smtp=SMTP(authdata["SERVER"],authdata["PORT"])
    server_smtp.connect(authdata["SERVER"],authdata["PORT"])
    server_smtp.ehlo()
    server_smtp.starttls()
    server_smtp.ehlo()
    server_smtp.login(authdata["USER"],authdata["PASSWORD"])
    message="Mensagem originada do Site lunelli.com.br\n\n"
    message+="Nome: "+data["00N4W00000S0yWc"]+"\n"
    message+="Email: "+data["email"]+"\n"
    message+="Mensagem: "+data["description"]+"\n"
    server_smtp.sendmail("noreply@lunelli.com.br","osmar.gascho@nbwdigital.com.br",message)
    ret=server_smtp.quit()
    print(ret)