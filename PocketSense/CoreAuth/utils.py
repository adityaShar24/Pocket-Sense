from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .models import (
    EmailVerification,
)

def send_verification_email(user, request):
    email_verification = EmailVerification.objects.create(user=user)
    token = email_verification.token
    uid = urlsafe_base64_encode(force_bytes(user.id))

    current_site = get_current_site(request)
    verification_url = f"http://{current_site.domain}/auth/verify-email/{uid}/{token}/"

    subject = "Verify your College Email"
    message = render_to_string('email/email_verification.html', {
        'user': user,
        'verification_url': verification_url,
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email="noreply@college.com",
        to=[user.email],
    )
    email.content_subtype = "html"  # Specify the content type as HTML
    email.send()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(id=uid)
        email_verification = EmailVerification.objects.get(user=user, token=token)
        
        if not email_verification.is_verified:
            email_verification.is_verified = True
            email_verification.save()
            return HttpResponse("Email verified successfully!")
        else:
            return HttpResponse("Email already verified.")
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        return HttpResponse("Invalid verification link.")