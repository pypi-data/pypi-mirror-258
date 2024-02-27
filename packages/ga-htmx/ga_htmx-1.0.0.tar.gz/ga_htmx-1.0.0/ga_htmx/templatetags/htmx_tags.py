from django.urls import reverse as django_reverse
from django.template import Library#, Node
#from django.template.base import Variable, VariableDoesNotExist
from django.utils.safestring import mark_safe
from ..util import buildurlparameters, push
from ..options import DEFAULT_HX_SWAP_DELAYED, DEFAULT_HX_TARGET_ID, DEFAULT_HX_ATTRS, AUTO_PUSH, HTMX_ENABLED


register = Library()

@register.simple_tag
def htmx(method, url=None, reverse: bool = False, skip_push: bool = False, **kwargs):
    """
        Write a list of htmx-attributes for a given url.
    """

    if not HTMX_ENABLED:
        return "data-hx-disabled"
    
    if "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
        kwargs = kwargs["kwargs"]

    if not method:
        raise ValueError("Method must be a string")
    
    if reverse and not url:
        raise ValueError("Url to reverse must be a string")
    
    elif reverse:
        url = django_reverse(url)

    method = method.lower()
    if url:
        attrs_string = f" hx-{method}=\"{url}\""
    else:
        attrs_string = f" hx-{method}"

    if DEFAULT_HX_SWAP_DELAYED and "swap" not in kwargs:
        attrs_string += f" hx-swap=\"{DEFAULT_HX_SWAP_DELAYED}\""

    if DEFAULT_HX_TARGET_ID and "target" not in kwargs:
        attrs_string += f" hx-target=\"{DEFAULT_HX_TARGET_ID}\""

    for key, value in DEFAULT_HX_ATTRS.items():
        if key not in kwargs:
            if callable(value):
                value = value(method, url)
            attrs_string += f" {key}=\"{value}\""

    if not skip_push \
            and AUTO_PUSH \
            and method.lower() in ["get", "post"] \
            and not "push_url" in kwargs:
            
        attrs_string += f" hx-push-url=\"{url}\""

    for key, value in kwargs.items():
        key = key.lower()
        key = key.replace("_", "-")
        attrs_string += f" hx-{key}=\"{value}\""

    return mark_safe(attrs_string)

# class HTMXNode(Node):
#     """
#         Node to render a block if htmx is enabled.
#     """
#     def __init__(self, nodelist, method, url=None, **kwargs: Variable):
#         self.nodelist = nodelist
#         self.method = method
#         self.url = url
#         self.kwargs = kwargs
# 
#     def render(self, context):
#         return self.nodelist.render(context)
#     


@register.simple_tag(takes_context=True)
def allow_htmx_pushing(context, allow_pushing=False):
    """
    Allow pushing for a given request.
    """
    if "request" not in context:
        return ""
    
    request = context["request"]
    push(request, allow_pushing=allow_pushing)
    return ""

@register.simple_tag(takes_context=True)
def buildurlparams(context, include_path=False, **kwargs):
    """
    Build a query string from a given context.
    """
    if "request" not in context:
        return ""
    request = context["request"]
    query = request.GET.copy()
    if include_path:
        return buildurlparameters(query, path=request.path, **kwargs)
    return buildurlparameters(query, **kwargs)
