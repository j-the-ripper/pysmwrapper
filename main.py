import os
from dotenv import load_dotenv
from pysmwrapper import WhatsApp

load_dotenv()
token = os.getenv("TOKEN")
print(token)
whatsapp = WhatsApp(os.getenv("TOKEN"), wa_id=os.getenv("WA_ID"))

print(whatsapp.send_media('https://i.imgur.com/FXvlGEd.jpeg','919405235423','image',caption='this').text)