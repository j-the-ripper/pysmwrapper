"""
Utility to send text and media messages with WhatsApp's cloud APIs
"""
import requests
import mimetypes

ConnectErrs =  (requests.exceptions.Timeout, 
                requests.exceptions.ConnectionError)

class WhatsApp:
    """
    Initiate WhatsApp object
    """
    def __init__(self, token=None, phone_number_id=None):
        """
        Intiate WhatsApp object with token, phone_number_id

        :params
            token[str] - Token from facebook portal to run APIs
            phone_number_id[str] - Test number given on the developer portal
        :return
            whatsapp object
        """
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v14.0"
        self.url = f"{self.base_url}/{self.phone_number_id}/messages"
        self.upload_url = f"{self.base_url}/{self.phone_number_id}/media"
        self.upload_headers = {
            "Authorization": f"Bearer {self.token}"
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    def __str__(self):
        return f"WhatsApp-{self.phone_number_id}"
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.phone_number_id}','{self.token}')"

    def send_message(self,message, phone_number,preview_url=True, recipient_type="individual"):
        """
        Send text simple message to phone_number
        :params
            message[str]        - Message to send
            phone_number[str]   - Phone number of user with country code without '+'.
            preview_url[bool]   - Whether to send links with preview or not
            recipient_type[str] - Type of recipient group or individual
        :return
            Response JSON
        """
        data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": phone_number,
                "type": "text",
                "text": {
                        "preview_url": preview_url,
                        "body": message
                    },
                }

        return self._call_post(data)



    def send_media (self,
                    media_link,
                    phone_number,
                    media_type,
                    access_type=True,   
                    caption=None,
                    recipient_type="individual"
                    ):
        """
        Send media message(audio, document, image, video) to phone_number.
        :params
            media_type[str]   - Type of media(audio, document, image, video) to send
            phone_number[str] - Phone number of user with country code without '+'
            media_link[str]   - Link of media if access_type is True or Media ID if access_type
                                is False
            access_type[bool] - True means send media with media_link, False means send media
                                with id
            caption[str]      - Caption of the media
        :return
            Response JSON
        """
        
        data = self._get_media_payload(media_link,phone_number,media_type,access_type,
                                        recipient_type)
        if media_type != "audio":
            data[media_type]["caption"] = caption

        return self._call_post(data)
        

    def send_location  (self,
                        longitude,
                        latitude,
                        phone_number,
                        location_name=None,
                        location_address=None):
        """
        Send location message to phone_number
        :params
            longitude[str]: Longitude of the location
            latitude[str]: Latitude of the location
            location_name[str]: Name of the location
            location_address[str]: Address of the location. 
                                    Only displayed if name is present.
            phone_number[str]: Phone number of the user with country code wihout +
        :return
            Response JSON
        """
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "location",
            "location": {
                "longitude": longitude,
                "latitude": latitude,
                "name": location_name,
                "address": location_address,
            },
        }

        if location_name is not None:
            data["location"]["name"] = location_name
            data["location"]["address"] = location_address

        return self._call_post(data)

    def upload_media(self,file_path):
        """
        Upload media to WA server
        :params
            file_path[str]: Absolute path of the file
        :return
            Response JSON
        """
        file_name = file_path.split("/")[-1]
        mime_type = str(mimetypes.guess_type(file_path)[0])
        data = {
                'messaging_product': 'whatsapp'
                }
        files=[
          ('file',(file_name,open(file_path,'rb'),mime_type))
        ]

        try:
            resp = requests.post(self.upload_url, headers=self.upload_headers, data=data, 
                                    files=files, timeout=10)
            return resp.json()
        except ConnectErrs as err:
            return {'connect_error':{'message' : str(err)}}     


    def retrieve_media_url(self,media_id):
        """
        Get media information such as url,hash,file_size for given media_id
        :params
            media_id[str] : media_id received from upload_media API
        :return
            Response JSON
        """
        resp = requests.get(self.upload_url, headers=self.upload_headers, 
                            data=data, files=files, timeout=10)
        return resp.json()

    def download_media( self,
                        file_name,
                        file_path,
                        media_link,
                        mime_type):
        """
        Saves media content to given file path
        :params
            media_link[str] : media_link received from retrieve_media_url API
            file_name[str] : Name of the file you want to save
            file_path[str]: Absolute path of the file
            mime_type[str] : MimeType of file to be saved
        :return
            Internal response JSON
        """

        try:
            file_extension = mimetypes.guess_extension(mime_type)
            file_path += (filename + file_extension)
            resp_content = requests.get(media_link,headers=self.upload_headers,stream=True)
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(resp_content.raw, out_file)
            del resp_content
            return {'success' : {'message' : 'File saved successfully'}}
        except ConnectErrs as err:
            return {'connect_error':{'message' : str(err)}}    

    def _call_post(self,data):
        try:
            resp = requests.post(url=self.url, headers=self.headers, json=data, timeout=10)
            return resp.json()
        except ConnectErrs as err:
            return {'connect_error':{'message' : str(err)}}       


    def _get_media_payload (self,
                            media_link,
                            phone_number,
                            media_type,
                            access_type=True,
                            recipient_type="individual"
                            ):
        if access_type:
            return {
                        "messaging_product": "whatsapp",
                        "recipient_type": recipient_type,
                        "to": phone_number,
                        "type": media_type,
                        media_type: {
                            "link" : media_link,
                        }
                    }
        return {
                    "messaging_product": "whatsapp",
                    "recipient_type": recipient_type,
                    "to": phone_number,
                    "type": media_type,
                    media_type: {
                        "id" : media_link,
                    }
                }
