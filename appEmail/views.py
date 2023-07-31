from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from . tasks import process_message
import boto3

# Create your views here.
def index(request):

  return render(request, "appEmail/index.html")

def sendMailPage(request):
  
  userGroups = []
  try:
      for element in request.user.groups.all():
          userGroups.append(element.name)
  except:
      pass
  
  context = {
      "userGroups" : userGroups,
      "sidebarActive" : "e-mail",
      "altSidebarActive"  : "sendMail"
  }

  ses = boto3.client('ses')

  mail_templates = ses.list_templates(MaxItems=25)
  
  context["mailTemplates"] = mail_templates

  if request.method == 'POST':
    if 'send_with_celery' in request.POST:

        send_template_name = request.POST.get('send_template_name')
        mail_from = request.POST['mail_from']
        mail_to = request.POST['mail_to']
        mail_cc = request.POST['mail_cc']
        reply_to = 'tfakgul2@gmail.com'

        try:
            process_message.delay(send_template_name,mail_from,mail_to,mail_cc,reply_to)
            success_message = "Mail is successfully sent to Tasks. (Without Delay)"
        except:
            success_message = "Operation failed."   

        return render(request, 'appEmail/sendMail.html', {'success_message': success_message})
  
  return render(request, "appEmail/sendMail.html", context)

def createMailPage(request):
  
  userGroups = []
  try:
      for element in request.user.groups.all():
          userGroups.append(element.name)
  except:
      pass
  context = {
      "userGroups" : userGroups,
      "sidebarActive" : "e-mail",
      "altSidebarActive"  : "createMail"
  }
  
  return render(request, "appEmail/createMail.html", context)
