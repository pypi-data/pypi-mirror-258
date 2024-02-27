from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect as _redirect
from .request import is_htmx
from .response import (
    HXRedirect,
)

def redirect(to: str, request=None, permanent: bool = False, *args, **kwargs):
    """
    Redirects to to a given URL, which may be a path relative to the request path.
    """
    if request is not None and is_htmx(request):
        status = 301 if permanent else 302
        response = HttpResponseRedirectBase(to, status=status)
        response[HXRedirect] = to
        del response["Location"]
        return response
    else:
        return _redirect(to, request=request, permanent=permanent, *args, **kwargs)
    
redirect.takes_request = True
redirect.django_redirect = _redirect


