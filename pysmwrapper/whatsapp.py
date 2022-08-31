"""
Utility to send text and media messages with WhatsApp's cloud APIs
"""
import logging
import requests

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("pysmwrapper/log/whatsapp_api.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class WhatsApp:
    """
    Initiate WhatsApp object
    """
    def __init__(self, token=None, wa_id=None):
        """
        Intiate WhatsApp object with token, wa_id

        :params
            token[str] - Token from facebook portal to run APIs.
            wa_id[str] - Test number given on the developer portal.
        :return
            whatsapp object
        """
        self.token = token
        self.wa_id = wa_id
        self.base_url = "https://graph.facebook.com/v14.0"
        self.url = f"{self.base_url}/{self.wa_id}/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    def __str__(self):
        return f"WhatsApp-{self.wa_id}"
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.wa_id}','{self.token}')"

    def send_message(self,message, phone_number,preview_url=True, recipient_type="individual"):
        """
        Send text simple message to phone_number.
        :params
            message[str]        - Message to send.
            phone_number[str]   - Phone number of user with country code without '+'.
            preview_url[bool]   - Whether to send links with preview or not.
            recipient_type[str] - Type of recipient group or individual
        :return
            json response of the request made.
        """
        resp = None
        try:
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
            resp = requests.post(url=self.url, headers=self.headers, json=data, timeout=10)
        except Exception as err:
            logger.error("Error in send message: %s",str(err))
        else:
            return resp

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
            media_type[str]   - Type of media(audio, document, image, video) to send.
            phone_number[str] - Phone number of user with country code without '+'.
            media_link[str]   - Link of media if access_type is True or Media ID if access_type
                                is False
            access_type[bool] - True means send media with media_link, False means send media
                                with id.
            caption[str]      - Caption of the media.
        """
        resp = None
        try:
            data = self._get_media_payload(media_link,phone_number,media_type,access_type,
                                            recipient_type)
            if media_type != "audio":
                data[media_type]["caption"] = caption

            resp = requests.post(self.url, headers=self.headers, json=data)
        except Exception as err:
            logger.error("Error in send message: %s",(err))
        else:
            return resp


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
        else:
            # Payload with media id.
            return {
                        "messaging_product": "whatsapp",
                        "recipient_type": recipient_type,
                        "to": phone_number,
                        "type": media_type,
                        media_type: {
                            "id" : media_link,
                        }
                    }
