from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

import json
import logging
import random
import time
import requests

from mongoengine import *
from netm.helpers import *

# connect('netm', host='mongodb.netm', port=27017)
connect('netm')

class Members(Document):

    USER_STATUS_EMAIL_VERIFICATION = 10
    USER_STATUS_MOBILE_VERIFICATION = 20
    USER_STATUS_VERIFIED = 30

    user_id = StringField()
    email = StringField()
    password = StringField()
    first_name = StringField()
    last_name = StringField()
    gender = StringField()
    dob = StringField()
    user_type = StringField()
    mobile = StringField()
    status = IntField()
    verification_code = StringField()
    access_token = StringField()

    def getMobile(self) :
        return self.mobile

    def createMember(self) :
        self.setUserId()
        self.setEmailVCode()
        self.hashPassword()
        self.status = self.USER_STATUS_EMAIL_VERIFICATION
        self.save()

    def setUserId(self) :
        # KM 107 0001 , KG 107 0001
        self.user_id = 'K' + str(self.gender).capitalize() + '107' + '%04d' % (len(Members.objects) + 1)

    def verifyEmail(self) :
        self.status = self.USER_STATUS_MOBILE_VERIFICATION
        self.save()

    def addMobile(self, mobile) :
        self.setMobileVCode()
        self.mobile = mobile
        self.save()

    def verifyMobile(self) :
        self.verification_code = '-'
        self.status = self.USER_STATUS_VERIFIED
        self.generateAccessToken()
        self.save() 
        
    def setEmailVCode(self) :
        self.verification_code = get_random_string(length=1, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ').capitalize() + str(random.randint(1000, 9999))

    def setMobileVCode(self) :
        self.verification_code = str(random.randint(1000, 9999))

    def hashPassword(self) :
        self.password = make_password(self.password)

    def generateAccessToken(self) :
        self.access_token = make_password(str(self.id) + str(time.time()) + get_random_string(length=2))

    def sendEmailVCode(self) :
        email_msg = 'Hi %s, Please use <b>%s</b> as your verification code, or else simply click the link here <a href="http://"></a> to activate your Kithunu account <p>Thanks,<br>Kithunu Team</p>' % (self.first_name, self.verification_code)
        send_email_thread(self.email, 'Kithunu Verfication', email_msg)

    def sendMobileVCode(self) :
        send_sms_thread(self.getMobile(), self.first_name, self.verification_code + ' is your Kithunu verification code')


# Don't refer after this line
class Database():

    col_name = "members"

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client["netm"]
        self.col = self.db[self.col_name]

    def members(self):
        self.col = self.db['members']
        return self.col

    def users(self):
        self.col = self.db['users']
        return self.col
        
db = Database()

if __name__ == "__main__":
    print("Netm is working")
