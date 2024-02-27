from .details import HTMXDetails
from django.http import HttpRequest

class HTMXRequest(HttpRequest):
    htmx: HTMXDetails
