from typing import TYPE_CHECKING
from django.http import HttpResponse

from .details import HTMXDetails

if TYPE_CHECKING:
    from .types import HTMXRequest


class HtmxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: "HTMXRequest"):

        request.htmx = HTMXDetails(request)
        
        response: HttpResponse = self.get_response(request)

        if response.headers.get("Content-Type") == "application/json":
            return response

        if request.htmx:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"

        return response
    
    