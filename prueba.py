from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import mimetypes

SCOPES = ['https://mail.google.com/']

def main():
     creds = None
     
     if os.path.exists('token.json'):
          creds = Credentials.from_authorized_user_file('token.json', SCOPES)

     # If there are no (valid) credentials available, let the user log in.
     if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
          else:
               flow = InstalledAppFlow.from_client_secrets_file('token.json', SCOPES)
               creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
          with open('token.json', 'w') as token:
               token.write(creds.to_json())

     try:
        # Llamado a la api de GMAIL
        service = build('gmail', 'v1', credentials = creds)
        results = service.users().labels().list(userId = 'me').execute()
        labels = results.get('labels', [])

     #    if not labels:
     #        print('No labels found.')
     #        return
     #    print('Labels:')
     #    for label in labels:
     #        print(label['name'])

     except HttpError as error:
        print(f'An error occurred: {error}')

     return service



def enviarMensaje(service):
     
     email_mensaje = "Mensaje de prueba desde la API de Gmail."
     mensaje_enc = MIMEText(email_mensaje)
     mensaje_enc['to'] = "oyp@scienza.com.ar"
     mensaje_enc['from'] = "adrian23.alarcon@gmail.com"
     mensaje_enc['subject'] = "Prueba API GMAIL Python"
     
     # mensaje_enc.attach(MIMEText(email_mensaje, 'plain'))

     # raw_string = base64.urlsafe_b64encode(mensaje_enc.as_bytes()).decode()
     raw_string = base64.urlsafe_b64encode(mensaje_enc.as_bytes()).decode()

     message = service.users().messages().send(userId='me', body= {'raw': raw_string}).execute()
     print(message)




def enviar_mensaje_adjuntos(file, service):
     mensaje_mail = "Esta es otra prueba enviando archivos adjuntos"

     mimeMultipart = MIMEMultipart()
     mimeMultipart['to'] = "oyp@scienza.com.ar"
     mimeMultipart['from'] = "adrian23.alarcon@gmail.com"
     mimeMultipart['subject'] = "Mensaje con adjuntos - API Gmail"

     mimeMultipart.attach(MIMEText(mensaje_mail, 'plain'))

     tipo_contenido, encoding = mimetypes.guess_type(file)
     main_type, sub_type = tipo_contenido.split('/', 1)

     file_name = os.path.basename(file)

     f = open(file_name, 'rb')

     my_file = MIMEBase(main_type, sub_type)
     my_file.set_payload(f.read())
     my_file.add_header('Content-Disposition', 'attachment', filename = file_name)
     encoders.encode_base64(my_file)

     f.close()

     mimeMultipart.attach(my_file)

     raw_str = base64.urlsafe_b64encode(mimeMultipart.as_bytes()).decode()
     message = service.users().messages().send(userId='me', body= {'raw': raw_str}).execute()
     print(message)



servicio = main()
enviar_mensaje_adjuntos('prueba.pdf', servicio)