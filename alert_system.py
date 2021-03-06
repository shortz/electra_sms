import requests
import json
from send_sms import SendSms
import time

START_OF_MSG = "אלקטרה גילתה תקלה במזגנך"
END_OF_MSG = "תמיד כאן בשבילך, אלקטרה"
ORDER_TECH_MSG = "תוכל לעשות זאת בקישור הבא"
FILTER_ERROR_MSG = "הינך מתבקש להחליף פילטרים למזגן, בקישור הבא תוכל לקבל הוראות איך לעשות זאת"
CHANGE_FILTER_VIDEO = "http://bit.ly/acFilter"
CALENDER_LINK = "http://bit.ly/electraTech"
SUPPORT_CALL_YOU_MSG = "אם ברצונך לפנות לנציג שירות נא לחץ על הלינק הבא "
SUPPORT_LINK = "http://bit.ly/setMeeting"


class ClientIntel:
    def __init__(self):
        self.clients_dict = {}

    def add_client(self, client_intel, serial_num):
        self.clients_dict[serial_num] = client_intel

    def get_client(self, serial_num):
        if serial_num in self.clients_dict:
            return self.clients_dict[serial_num]
        print("no client {}".format(serial_num))


class ErrorToMsg:
    def __init__(self):
        self.error_dict = {}

    def add_error_msg(self, error_id, msg):
        self.error_dict[error_id] = msg

    def get_error_msg(self, error_id):
        return self.error_dict[error_id]


class CheckAlert:
    def __init__(self, alert_server_url):
        self.host = alert_server_url

    def connect_to_server(self):
        return self.host

    def get_alert(self):
        response = requests.get(url=self.host)
        j = json.loads(response.text)
        print(j)
        if "acId" in j:
            return j["acId"]


def alert_job(alert_list_arr, alerts_, client_intel, error_to_msg):
    alert_list = alerts_.get_alert()
    if not alert_list:
        print("No list")
        return

    for client_id in alert_list:
        client = client_intel.get_client(client_id)
        if not alert_list[client_id]["errorCode"]:
            print("no error message for {}".format(alert_list[client_id]["errorCode"]))
            continue
        error_msg = error_to_msg.get_error_msg(str(alert_list[client_id]["errorCode"]))
        client_sms = SendSms(client['number'])

        client_sms_msg = "{} {},\n{}.\n{}.\n{}:\n{}\n{}.".format("שלום",
                                                                 client['name'],
                                                                 START_OF_MSG,
                                                                 error_msg,
                                                                 SUPPORT_CALL_YOU_MSG,
                                                                 SUPPORT_LINK,
                                                                 END_OF_MSG)
        if alert_list[client_id]["errorCode"] not in alert_list_arr:
            client_sms.send_sms(client_sms_msg)
            alert_list_arr.append(alert_list[client_id]["errorCode"])
            print("sent message")


if __name__ == '__main__':
    # Fill DB.
    client_db = ClientIntel()
    client_db.add_client({'name': 'גיא עשת', 'number': '+972546626752'}, '3763200171')
    client_db.add_client({'name': 'גיא עשת', 'number': '+972546626752'}, '2')
    client_db.add_client({'name': 'גיא עשת', 'number': '+972546626752'}, '3')
    error_db = ErrorToMsg()
    error_db.add_error_msg('1.0', "{}.\n{}: {}".format("התקלה מצריכה קריאה לטכנאי", ORDER_TECH_MSG, CALENDER_LINK))
    error_db.add_error_msg('1.0', "{}:\n{}".format(FILTER_ERROR_MSG, CHANGE_FILTER_VIDEO))
    error_db.add_error_msg('3.0', "{}.\n{}: {}".format("התקלה מצריכה קריאה לטכנאי", ORDER_TECH_MSG, CALENDER_LINK))
    error_db.add_error_msg('4.0', "{}.\n{}: {}".format("התקלה מצריכה קריאה לטכנאי", ORDER_TECH_MSG, CALENDER_LINK))
    # Set alert server connection.
    alerts = CheckAlert('http://104.199.88.197/get_errors/')
    error_list = []
    while True:
        time.sleep(1)
        alert_job(error_list, alerts, client_db, error_db)
