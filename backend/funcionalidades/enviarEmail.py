from email.message import EmailMessage
import ssl
import smtplib


class email:
    def __init__(self, emailreceptor, p) -> None:
        self.emailemisor = 'preuebaspython@gmail.com'
        self.emailcontraseña = 'xscvodrwfqutoswh'
        self.emailreceptor = emailreceptor
        self.asunto = 'Recuperar Contraseña'
        self.cuerpo = '''
        
Se solicito un cambio de contraseña

Su contraseña temporal es: '''+p+'''

La contraseña es de un solo uso, cambia la contraseña luego de iniciar'''

    @classmethod
    def enviarCorreo(self, email):
        em = EmailMessage()
        em['From'] = email.emailemisor
        em['To'] = email.emailreceptor
        em['Subject'] = email.asunto
        em.set_content(email.cuerpo)

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
            smtp.login(email.emailemisor, email.emailcontraseña)
            smtp.sendmail(email.emailemisor,
                          email.emailreceptor, em.as_string())
        return True
