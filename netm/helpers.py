# Netmaiesta Helpers

import requests
import json
import logging
import threading

from django.http import HttpResponse, Http404, JsonResponse
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def netmJsonResponse(body='{ "status_code" : 999 }'):

    if isinstance(body, int):
        body = '{ "status_code" : ' + str(body) + ' }'

    if(isinstance(body, dict)) :
        body = json.dumps(body)

    response = HttpResponse()
    netmJsonHeaders(response)
    response.write(body)
    return response

def netmJsonHeaders(response):

    response["Access-Control-Allow-Origin"] = "*"
    response['Content-Type'] = "application/json; charset=utf-8"
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

def formToDocument(form):
    return json.loads(json.dumps(form.clean()))

def send_sms(no, name, sms_msg) :
    
    # x = send_sms('94762724081', 'Aslam', 'Hi there')
    # sms_msg =  + ' is your Kithunu verification code'

    post_data = {
        'user_id' : '10898',
        'api_key' : 'LrydNspY3SeURSo40bto',
        'sender_id' : 'NotifyDEMO',
        'to' : no,
        'message' : sms_msg,
        'contact_fname' : name
    }

    response = requests.post('https://app.notify.lk/api/v1/send', data=post_data)
    content = response.content.decode('utf-8')
    dic = json.loads(content)
    logger.error(dic)

    return dic

def send_sms_thread(no, name, sms_msg) :
    threading.Thread(target=send_sms, args=(no, name, sms_msg)).start()

def send_email(to, subject, message) :
    send_mail(subject, '', 'Netm Sandbox <netm.sandbox@gmail.com>', [to], fail_silently=False, html_message=message)

def send_email_thread(to, subject, message) :
    threading.Thread(target=send_email, args=(to, subject, message)).start()