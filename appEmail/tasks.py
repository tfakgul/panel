from celery import shared_task
from time import sleep
from django.shortcuts import render, redirect, HttpResponse
import boto3

@shared_task
def process_message(template_name,mail_from,mail_to,mail_cc,reply_to):

    ses = boto3.client('ses')

    try:
        response = ses.send_templated_email(
        Source = mail_from,
        Destination={
            'ToAddresses': [
            mail_to,
            ],
            'CcAddresses': [
            mail_cc,
            ]
        },
        ReplyToAddresses=[
            reply_to,
        ],
        Template = template_name,
        TemplateData='{ \"REPLACEMENT_TAG_NAME\":\"REPLACEMENT_VALUE\" }'
        )
        success_message = "Successful"
        
    except:
        success_message = "Operation failed."  

    return None