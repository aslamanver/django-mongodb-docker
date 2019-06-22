from django.shortcuts import render
from django.http import HttpResponse, Http404
from pymongo import MongoClient
from bson.json_util import dumps
import json
from netm.database import *
from django.views.decorators.http import require_http_methods
from django.utils.crypto import get_random_string
from django.core import signing
from datetime import datetime
import time
from django.db.models.functions import Now

from .forms import *
from django.http import JsonResponse
import random
import string

STATUS_CODE_EMPTY = 444
STATUS_CODE_FORM_INVALID = 999
STATUS_CODE_SUCCESS = 222
STATUS_CODE_FAILED = 404
STATUS_CODE_EMAIL_EXISTS = 777
STATUS_CODE_EMAIL_NOT_EXISTS = 555

USER_STATUS_EMAIL_VERIFICATION = 10
USER_STATUS_MOBILE_VERIFICATION = 20

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

            x = db.members().insert_one(formToDocument(form))

            if x.inserted_id:

                member: Members = Members.objects(email=form.cleaned_data['email']).first()
                rand = get_random_string(length=1, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ').capitalize() + str(random.randint(1000, 9999))
                # Send email server as well
                member.verification_code = rand
                member.status = USER_STATUS_EMAIL_VERIFICATION
                member.save()

                return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse()


def signup_email_verify(request):

    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == "POST":

        form = jsonForm(request)
        member: Members = Members.objects(email=form['email'], verification_code=form['vcode']).first()

        if member :
            member.verification_code = "-"
            member.status = USER_STATUS_MOBILE_VERIFICATION
            member.save()

            return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse(STATUS_CODE_FAILED)


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
