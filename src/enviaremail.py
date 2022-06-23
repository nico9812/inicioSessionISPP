from email.message import EmailMessage
import ssl, smtplib

class email:
  def __init__(self,emailreceptor,p) -> None:
    self.emailemisor='preuebaspython@gmail.com'
    self.emailcontraseña='xscvodrwfqutoswh'
    self.emailreceptor=emailreceptor
    self.asunto='Recuperar Contraseña'
    self.cuerpo='contraseña temporal: '+p

  @classmethod
  def enviaremail(self, email):
    print(email.emailemisor, email.emailreceptor, email.asunto, email.cuerpo)
    em = EmailMessage()
    em['From'] = email.emailemisor
    em['To'] = email.emailreceptor
    em['Subject'] = email.asunto
    em.set_content(email.cuerpo)

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
      smtp.login(email.emailemisor,email.emailcontraseña)
      smtp.sendmail(email.emailemisor, email.emailreceptor, em.as_string())
