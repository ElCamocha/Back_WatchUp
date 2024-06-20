import os.path
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from BackEnd.GlobalInfo.Keys import strSmtpEmail, strSmtpUser, strSmtpPassword, intSmtpPort, strSmtpServer

class ServerMail(object):
    def __init__(self):
        self.strEmail = strSmtpEmail
        self.strSmtpUser = strSmtpUser
        self.strPassword = strSmtpPassword
        self.strServer = strSmtpServer
        self.intPort = intSmtpPort
        smtp = smtplib.SMTP(self.strServer, self.intPort)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.strEmail, self.strPassword)
        self.smtp = smtp
        
        
    def fnSendMessage(
            self, strSubject, strBody, strToSend, strFileName="info.pdf", pdfFile=None
    ):
        currentPath = os.path.dirname(__file__)
        msg = MIMEMultipart('mixed')
        msg["Subject"] = strSubject
        msg["From"] = formataddr(('watchup', strSmtpEmail))
        msg["To"] = strToSend

        HTML_Contents = MIMEText(strBody, 'html')
        msg.attach(HTML_Contents)

        if pdfFile is not None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(pdfFile)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=strFileName)
            part.add_header('Content-Disposition', 'inline', filename=strFileName)
            msg.attach(part)

        self.smtp.sendmail(msg["From"], msg["To"], msg.as_string())


def verifyEmailTemplate(link: str):
    title = 'Verifica tu cuenta de Watch Up'
    header = 'Verifica tu correo electrónico para poder seguir usando tu cuenta de Watch Up'
    body = '''
        Accede al siguiente enlace para confirmar tu correo electrónico. En caso de que no lo hayas solicitado ignora este mensaje. <br/>(Revisa tu bandeja de SPAM y muévelo a tu bandeja de entrada para poder ver el link de verificación)
    '''
    button = 'Verificar mi cuenta'
    
    template = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="viewport" content="width=device-width"/>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <title>{title}</title>
</head>

<body style="background-color: #FFFFFF;">
<center>
    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" style="background-color: #9CBECE; padding: 24px; width: auto; border-radius: 20px">
        <tr>
            <td align="center" valign="top" id="bodyCell">
                <table border="0" cellpadding="0" cellspacing="0" width="550">
                    <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" valign="top"></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="550"
                                               class="flexibleContainer">
                                            <tr>
                                                <td align="center" valign="top" width="550"
                                                    class="flexibleContainerCell">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td valign="top" class="textContent">
                                                                <p style="font-size:30px;text-align: center;line-height:31px;color:#262424; font-weight: 600;font-family: 'Roboto', sans-serif;">
                                                                    {header}
                                                                </p>
                                                                <p id="letra"
                                                                   style="font-size:21px;color: #262424;text-align: justify;font-family: 'Roboto', sans-serif;">
                                                                    {body}
                                                                </p>
                                                                <a role="button"
                                                                   style="border-radius: 12px; background-color: #FFFFFF; border-width: 0; display: inline-block; cursor: pointer; color: #001B46; font-family: 'Roboto', sans-serif; font-size: 20px; font-weight: bold; padding: 12px 16px; text-decoration: none;" target="_blank"
                                                                   href="{link}">{button}</a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</center>
</body>

</html>
"""
    return template


def forgotPasswordEmailTemplate(link: str):
    title = 'Cambia tu contraseña de tu cuenta de bitspot'
    header = 'Ingresa al siguiente enlace para cambiar tu contraseña'
    body = '''
        Accede al siguiente enlace para cambiar tu contraseña. En caso de que no lo hayas solicitado ignora este mensaje. <br/>(Revisa tu bandeja de SPAM y muévelo a tu bandeja de entrada para poder ver el link de verificación)
    '''
    button = 'Recuperar contraseña'

    template = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="viewport" content="width=device-width"/>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <title>{title}</title>
</head>

<body style="background-color: #FFFFFF;">
<center>
    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" style="background-color: #9CBECE; padding: 24px; width: auto; border-radius: 20px">
        <tr>
            <td align="center" valign="top" id="bodyCell">
                <table border="0" cellpadding="0" cellspacing="0" width="550">
                    <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" valign="top"></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="550"
                                               class="flexibleContainer">
                                            <tr>
                                                <td align="center" valign="top" width="550"
                                                    class="flexibleContainerCell">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td valign="top" class="textContent">
                                                                <p style="font-size:30px;text-align: center;line-height:31px;color:#262424; font-weight: 600;font-family: 'Roboto', sans-serif;">
                                                                    {header}
                                                                </p>
                                                                <p id="letra"
                                                                   style="font-size:21px;color: #262424;text-align: justify;font-family: 'Roboto', sans-serif;">
                                                                    {body}
                                                                </p>
                                                                <a role="button"
                                                                   style="border-radius: 12px; background-color: #FFFFFF; border-width: 0; display: inline-block; cursor: pointer; color: #001B46; font-family: 'Roboto', sans-serif; font-size: 20px; font-weight: bold; padding: 12px 16px; text-decoration: none;" target="_blank"
                                                                   href="{link}">{button}</a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</center>
</body>

</html>
"""
    return template
