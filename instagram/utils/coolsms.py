from pprint import pprint

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def coolsms(receiver, message):
    """
    Send SMS automatically
    :param receiver: 전화번호 문자열
    :param message: 메세지 문자열 (90자 이내)
    :return:
    """
    # set api key, api secret
    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"

    # 4 params(to, from, type, text) are mandatory. must be filled
    # params = {
    #     'type': 'sms',  # Message type ( sms, lms, mms, ata )
    #     'to': receiver,  # Recipients Number '01000000000,01000000001'
    #     'from': '01029953874',
    #     'next': message,
    # }
    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = receiver  # Recipients Number '01000000000,01000000001'
    params['from'] = '01029953874'  # Sender number
    params['text'] = message  # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

if __name__ == '__main__':
    coolsms(receiver='01037363692', message='hello')
