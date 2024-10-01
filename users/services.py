# from pprint import pprint
from smsaero import SmsAero  # , SmsAeroException

from config.settings import SMSAERO_EMAIL, SMSAERO_API_KEY


def send_sms(phone: int, message: str) -> dict:
    """Отправка смс через смс-аеро"""
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    return api.send_sms(int(phone), message)

# if __name__ == '__main__':
#     try:
#         result = send_sms(79114300043, 'Hello, World!')
#         pprint(result)
#     except SmsAeroException as e:
#         print(f"An error occurred: {e}")
