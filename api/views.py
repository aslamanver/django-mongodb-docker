from django.shortcuts import render
from django.http import HttpResponse, Http404
from pymongo import MongoClient
from bson.json_util import dumps
import json
from netm.database import *


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
