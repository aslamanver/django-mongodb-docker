from netm.database import *
from .forms import *
from netm.helpers import *

STATUS_CODE_EMPTY = 444
STATUS_CODE_FORM_INVALID = 999
STATUS_CODE_SUCCESS = 222
STATUS_CODE_FAILED = 404
STATUS_CODE_EMAIL_EXISTS = 777
STATUS_CODE_EMAIL_NOT_EXISTS = 555
STATUS_CODE_SMS_SEND_FAILED = 666

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

            member = Members(**formToDocument(form))
            member.createMember()
            member.sendEmailVCode()

            # Pure PyMongo method :
            # memberDoc = formToDocument(form)
            # memberDoc['verification_code'] = rand
            # memberDoc['status'] = USER_STATUS_EMAIL_VERIFICATION
            # memberDoc['password'] = make_password(memberDoc['password'])
            # dbDoc = db.members().insert_one(memberDoc)

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
            member.verifyEmail()
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
            member.addMobile(form['mobile'])
            member.sendMobileVCode()
            return netmJsonResponse(STATUS_CODE_SUCCESS)

        return netmJsonResponse(STATUS_CODE_FAILED)

def signup_mobile_verify(request):
    
    # Temporary Solution
    if not request.body.decode('utf-8'):
        return netmJsonResponse(STATUS_CODE_EMPTY)

    if request.method == 'POST':

        form = jsonForm(request)
        member: Members = Members.objects(mobile=form['mobile'], verification_code=form['vcode']).first()

        if member :
            member.verifyMobile()

            return netmJsonResponse({
                'statusCode' : STATUS_CODE_SUCCESS,
                'responseData' : { 'accessToken' : member.access_token }
            })

        return netmJsonResponse(STATUS_CODE_FAILED)

