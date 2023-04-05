from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from binago.utils import pages_mail

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token

from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe

from .models import User

if TYPE_CHECKING:
    from typing import Any
    from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect


def activate_email(request, user, to_email) -> None:
    mail_subject: str = "Verify your account for binago.id"
    message = render_to_string(
        pages_mail('verify_account.html'),
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email: EmailMessage = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f'Account has successfully created. Please check inbox on your email ({to_email}) to verify your account.',
        )
    else:
        messages.error(request, f'Problem sending email to { to_email }')


def verify(request, uidb64, token) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    uid: Any = force_str(urlsafe_base64_decode(uidb64))
    try:
        user: User = User.objects.get(id=uid)
        if user and account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()

            messages.success(request, "Account successfully verified! Please login to continue using your account.")
            return redirect('login')

        messages.error(
            request,
            mark_safe(
                f"""Account verification is invalid. Please make a new <a href="{ reverse('request-verify-account') }">request verify account</a>."""
            ),
        )

    except User.DoesNotExist:
        messages.error(request, "Account does not exists.")

    return redirect('login')
