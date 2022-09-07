import os
from dotenv import load_dotenv
from pysmwrapper import WhatsApp

load_dotenv()
token = os.getenv("TOKEN")
print(token)
whatsapp = WhatsApp(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))
print(whatsapp.upload_media("/home/jaypatel/pic.png"))
#print(whatsapp.send_media('https://i.imgur.com/FXvlGEd.jpeg','919405235423','image',caption='this').text)