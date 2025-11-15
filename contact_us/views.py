from django.shortcuts import render
from .models import info
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.


def contact_us(request):
    my_info = info.objects.first()
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            subject, # subject
            message, # message
            settings.EMAIL_HOST_USER, # sender email
            [email], # receiver email
            fail_silently=False, # if the email fails to send, it will not raise an error
        )
        messages.success(request, 'Your message has been sent successfully.')
        return render(request, 'contact_us/contact_us.html', {
            'my_info': my_info,
            'latitude': my_info.latitude if my_info else 0,
            'longitude': my_info.longitude if my_info else 0,
            })
    return render(request, 'contact_us/contact_us.html', {
        'my_info': my_info,
        'latitude': my_info.latitude if my_info else 0,
        'longitude': my_info.longitude if my_info else 0,
        })
