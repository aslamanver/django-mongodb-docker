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

def home(request):

    # c = Customer()
    # c.name = "Aslam"
    # c.address = "Dehiwala"
    # c.save()

    return HttpResponse(Customer.objects().to_json(indent=4), content_type="application/json")

    # customers = db.customers()
    # return HttpResponse(json.dumps(list(customers.find()), indent=4, default=str), content_type="application/json")


def edit(request, oid):

    c = Customer.objects.get(id=oid)

    return HttpResponse(c.name)


@require_http_methods(["POST"])
def entrance(request):

    token = {
        '_token': get_random_string(length=32) + signing.dumps(str(time.time()) + "Salt" + "UsernameOID"),
    }

    return HttpResponse(json.dumps(token), content_type="application/json")
