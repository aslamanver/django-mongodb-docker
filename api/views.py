from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from django.core import signing
from django.db.models.functions import Now
from django.core.mail import send_mail

from pymongo import MongoClient
from bson.json_util import dumps

import datetime
import json
import time
import random
import string
import requests

from netm.database import *
from .forms import *

STATUS_CODE_EMPTY = 444
STATUS_CODE_FORM_INVALID = 999
STATUS_CODE_SUCCESS = 222
STATUS_CODE_FAILED = 404
STATUS_CODE_EMAIL_EXISTS = 777
STATUS_CODE_EMAIL_NOT_EXISTS = 555
STATUS_CODE_SMS_SEND_FAILED = 666

USER_STATUS_EMAIL_VERIFICATION = 10
USER_STATUS_MOBILE_VERIFICATION = 20
USER_STATUS_VERIFIED = 30

# def entrance(request):
#     token = {'_token': get_random_string(length=32) + signing.dumps(str(time.time()) + "Salt" + "UsernameOID")}
#     return HttpResponse(json.dumps(token), content_type="application/json")

# Signup First Step

def signup_a(request):

    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == "POST":
            
        if request.GET.get('email_check'):

            return netmJsonResponse(STATUS_CODE_EMAIL_EXISTS if Members.objects(email=request.GET.get('email_check')) else STATUS_CODE_EMAIL_NOT_EXISTS)

        form = SignupFormA(jsonForm(request))

        if form.is_valid():

            if Members.objects(email=form.cleaned_data['email']).first():
                
                return netmJsonResponse(STATUS_CODE_EMAIL_EXISTS)

            rand = get_random_string(length=1, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ').capitalize() + str(random.randint(1000, 9999))                

            memberDoc = formToDocument(form)
            memberDoc['verification_code'] = rand
            memberDoc['status'] = USER_STATUS_EMAIL_VERIFICATION

            dbDoc = db.members().insert_one(memberDoc)

            # Send email
            email_msg = 'Hi %s, Your Kithunu account verification code is : <b>%s</b> <p>Thank you<br>Kithunu Team</p>' % (memberDoc['first_name'], memberDoc['verification_code'])
            send_mail('Kithunu Verfication', '', 'Netm Sandbox <netm.sandbox@gmail.com>', [memberDoc['email']], fail_silently=False, html_message=email_msg)

            return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse()


def signup_email_verify(request):

    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == 'POST':

        form = jsonForm(request)
        member: Members = Members.objects(email=form['email'], verification_code=form['vcode']).first()

        if member :
            member.verification_code = str(random.randint(1000, 9999))
            member.status = USER_STATUS_MOBILE_VERIFICATION
            member.save()

            return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse(STATUS_CODE_FAILED)


def signup_mobile_add(request):
    
    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == 'POST':

        form = jsonForm(request)
        member: Members = Members.objects(email=form['email']).first()

        if member :
            member.mobile = form['mobile']
            member.save()

            sms = send_sms(member.getMobile(), member.first_name, member.verification_code + ' is your Kithunu verification code')

            return netmJsonResponse(STATUS_CODE_SUCCESS if sms['status'] == 'success' else STATUS_CODE_SMS_SEND_FAILED)

        return netmJsonResponse(STATUS_CODE_FAILED)

def signup_mobile_verify(request):
    
    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == 'POST':

        form = jsonForm(request)
        member: Members = Members.objects(mobile=form['mobile'], verification_code=form['vcode']).first()

        if member :
            member.verification_code = '-'
            member.status = USER_STATUS_VERIFIED
            member.save()

            return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse(STATUS_CODE_FAILED)

# def signup_mobile_change(request):
    
#     # Temporary Solution
#     if not request.body.decode('utf-8'):
#         return netmJsonResponse(STATUS_CODE_EMPTY)

#     if request.method == 'POST':

#         form = jsonForm(request)
#         member: Members = Members.objects(email=form['email']).first()

#         if member :
#             member.verification_code = '-'
#             member.status = USER_STATUS_VERIFIED
#             member.save()

#             return netmJsonResponse(STATUS_CODE_SUCCESS)

#         return netmJsonResponse(STATUS_CODE_FAILED)

def send_sms(no, name, sms_msg) :
    # x = send_sms('94762724081', 'Aslam', 'Hi there')
    # sms_msg =  + ' is your Kithunu verification code'
    post_data = {
        'user_id' : '10893',
        'api_key' : '674tbOWVZgu0cRgX7Mlf',
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

def netmJsonResponse(body='{ "status_code" : 999 }'):

    if isinstance(body, int):
        body = '{ "status_code" : ' + str(body) + ' }'

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
