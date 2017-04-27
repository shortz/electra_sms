from twilio.rest import Client


class SendSms:
    def __init__(self, num):
        self.num = num
        self.account_sid = "ACed9fdd9e2994efea59b8282bbadf991c"
        self.auto_token = "75ed8a3caad7e163b5e191b331692535"
        self.twilio_num = '+12672027428'
        self.client = Client(self.account_sid, self.auto_token)

    def send_sms(self, message):
        self.client.messages.create(
            to=self.num,
            from_=self.twilio_num,
            body=message
        )
