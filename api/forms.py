from django import forms
import json
from . import models
from netm.database import logger


class SignupFormA(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    gender = forms.CharField(required=True)
    dob = forms.CharField(required=True)
    user_type = forms.CharField(required=True)


def jsonForm(req):
    logger.error("---- Request : \n" + req.body.decode('utf-8') + "\n----")
    return json.loads(req.body.decode('utf-8'))
