import copy
from typing import Callable, Type, TypeVar, Union
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirectBase
from django.template.response import TemplateResponse

from .response import (
    HXLocation,
    HXPushUrl,
    HXRedirect,
    HXRefresh,
    HXReplaceUrl,
    HXReswap,
    HXRetarget,
    HXReselect,
    HXTrigger,
    HXTriggerAfterSettle,
    HXTriggerAfterSwap,
)
from .check import (
    BaseCheck,
)
from .request import is_htmx

_CHECK_T = Union[bool, Callable[[HttpRequest], bool], BaseCheck]

def _should_use_tpl(request: HttpRequest, *use_template_if: _CHECK_T):
    for condition in use_template_if:
        if callable(condition):
            condition = condition(request)

        if not condition and condition is not None:
            return False
        
    return True

def _check_template(tpl: "Tpl"):
    if tpl is None:
        raise RuntimeError("No template provided")
    return tpl

def _to_valid_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    
    return value

def _header_if_not_none(d, header, value):
    if value is not None:
        d[header] = _to_valid_value(value)

    return d

def _redirect_response(tpl: "Tpl", request: HttpRequest, context: dict = None):
    to_url = tpl.template
    response = HttpResponseRedirectBase(to_url, **tpl.response_kwargs)
    if is_htmx(request):
        del response["Location"]
        response[HXRedirect] = to_url
    return response

def _render_json_response(tpl: "Tpl", request: HttpRequest, context: dict = None):
    return JsonResponse(tpl.template, **tpl.response_kwargs)

def _render_response(tpl: "Tpl", request: HttpRequest, context: dict = None):
    template = tpl.template
    context = context or {}
    return TemplateResponse(request, template, context=context, **tpl.response_kwargs)

def _render_hx_response(tpl: "HtmxTpl", request: HttpRequest, context: dict = None):
    response = _render_response(tpl, request, context)
    if is_htmx(request):
        for header, value in tpl.headers.items():
            response[header] = value
    return response

class Tpl:
    render_fn = _render_response

    def __init__(self, template: str, *use_template_if: _CHECK_T, priority: int = 0, **response_kwargs):
        self.request = None
        self.template = template
        self.use_template_if = use_template_if
        self.priority = priority
        self.response_kwargs = response_kwargs

    def __str__(self):
        return f"{self.__class__.__name__}({self.template})"

    def __lt__(self, other):
        if isinstance(other, int):
            return self.priority < other
        return self.priority < other.priority
    
    def __gt__(self, other):
        if isinstance(other, int):
            return self.priority > other
        return self.priority > other.priority

    def __bool__(self):
        return _should_use_tpl(self.request, *self.use_template_if)

    def render(self, context: dict = None) -> HttpResponse:
        return self.render_fn(self.request, self, context)

class RedirectTpl(Tpl):
    render_fn = _redirect_response

    def __init__(self, to_url: str, *use_template_if: _CHECK_T, priority: int = 0):
        super().__init__(to_url, *use_template_if, priority=priority)

class JsonTpl(Tpl):
    render_fn = _render_json_response

    def __init__(self, data: dict, *respond_json_if: _CHECK_T, priority: int = 0, **response_kwargs):
        super().__init__(data, *respond_json_if, priority=priority, **response_kwargs)

class HtmxTpl(Tpl):
    """
        HtmxTemplate is used to render a template to a HTMX response.
        It will only apply the headers to the response if the request is a HTMX request.
        If you'd rather use headers themselves there is no benefit to using this class over Tpl.
    """
    render_fn = _render_hx_response

    def __init__(self,
            template: str,
            *use_template_if: _CHECK_T,
            priority: int = 0,
            # Allows you to do a client-side redirect that does not do a full page reload.
            hx_location: str = None,
            # Pushes a new URL to the client's history.
            hx_push_url: str = None,
            # Do a client-side redirect to a new location.
            hx_redirect: str = None,
            # Refresh the current page.
            hx_refresh: bool = False,
            # Replace the current URL in the client's history with a new URL.
            hx_replace_url: str = None,
            # Allows you to specify how the response will be swapped.
            # See https://htmx.org/attributes/hx-swap/ for more values.
            hx_reswap: str = None,
            # A CSS selector that updates the target of the content update to a different element on the page.
            hx_retarget: str = None,
            # A CSS selector that allows you to choose which part of the response is used to be swapped in.
            # Overrides an existing hx-select on the triggering element.
            hx_reselect: str = None,
            # Allows you to trigger client-side events.
            hx_trigger: str = None,
            # Allows you to trigger client-side events after the response has settled.
            hx_trigger_after_settle: str = None,
            # Allows you to trigger client-side events after the response has been swapped.
            hx_trigger_after_swap: str = None,
            **response_kwargs
        ):
        
        headers = {}
        _header_if_not_none(headers, HXLocation, hx_location)
        _header_if_not_none(headers, HXPushUrl, hx_push_url)
        _header_if_not_none(headers, HXRedirect, hx_redirect)
        _header_if_not_none(headers, HXRefresh, hx_refresh)
        _header_if_not_none(headers, HXReplaceUrl, hx_replace_url)
        _header_if_not_none(headers, HXReswap, hx_reswap)
        _header_if_not_none(headers, HXRetarget, hx_retarget)
        _header_if_not_none(headers, HXReselect, hx_reselect)
        _header_if_not_none(headers, HXTrigger, hx_trigger)
        _header_if_not_none(headers, HXTriggerAfterSettle, hx_trigger_after_settle)
        _header_if_not_none(headers, HXTriggerAfterSwap, hx_trigger_after_swap)
        self.headers = headers

        super().__init__(template, *use_template_if, priority=priority, **response_kwargs)

_Tpl = TypeVar("_Tpl", bound=Tpl)

class HTMXTemplateRenderer:

    def __init__(self, request: HttpRequest, base_template: Union[str, Tpl] = None):
        self.request = request

        if isinstance(base_template, str):
            base_template = Tpl(base_template, not is_htmx(request), priority=-1)

        # The full template that will be rendered.
        self._base_template: _Tpl = base_template

        # Extra context data that will be passed to the templates.
        self._context = {}

        # List of templates that will be checked for rendering.
        self._templates: list[Tpl] = []

        # Checks that are used to determine if the renderer 
        # is allowed to render the conditional templates.
        self._base_checks: list[_CHECK_T] = []

    def add_context(self, **kwargs):
        self._context.update(kwargs)

    @property
    def context(self):
        return self._context

    @property
    def base_template(self):
        return self._base_template

    @base_template.setter
    def base_template(self, template: Union[str, _Tpl]):
        if isinstance(template, str):
            template = Tpl(template, priority=-1)

        self._base_template = template

    def add_redirect(self, to_url: Union[str, RedirectTpl], *use_redirect_if: _CHECK_T, priority: int = 0, **response_kwargs):
        """
            Add a redirect to the HTMXTemplateRenderer instance if the condition is met.
        """
        return self._add_template(
            RedirectTpl,
            to_url,
            *use_redirect_if,
            priority=priority,
            response_kwargs=response_kwargs
        )
    
    def add_json(self, data: dict, *respond_json_if: _CHECK_T, priority: int = 0, **response_kwargs):
        return self._add_template(
            JsonTpl,
            data,
            *respond_json_if,
            priority=priority,
            response_kwargs=response_kwargs
        )

    def add_template(self, template: Union[str, Tpl], *use_template_if: _CHECK_T, priority: int = 0, **response_kwargs):
        return self._add_template(
            Tpl,
            template,
            *use_template_if,
            priority=priority,
            response_kwargs=response_kwargs
        )
    
    def add_htmx_template(self, 
            template: Union[str, HtmxTpl],
            *use_template_if: _CHECK_T,
            priority: int = 0,
            # Allows you to do a client-side redirect that does not do a full page reload.
            hx_location: str = None,
            # Pushes a new URL to the client's history.
            hx_push_url: str = None,
            # Do a client-side redirect to a new location.
            hx_redirect: str = None,
            # Refresh the current page.
            hx_refresh: bool = False,
            # Replace the current URL in the client's history with a new URL.
            hx_replace_url: str = None,
            # Allows you to specify how the response will be swapped.
            # See https://htmx.org/attributes/hx-swap/ for more values.
            hx_reswap: str = None,
            # A CSS selector that updates the target of the content update to a different element on the page.
            hx_retarget: str = None,
            # A CSS selector that allows you to choose which part of the response is used to be swapped in.
            # Overrides an existing hx-select on the triggering element.
            hx_reselect: str = None,
            # Allows you to trigger client-side events.
            hx_trigger: str = None,
            # Allows you to trigger client-side events after the response has settled.
            hx_trigger_after_settle: str = None,
            # Allows you to trigger client-side events after the response has been swapped.
            hx_trigger_after_swap: str = None,
            **response_kwargs
        ):
        """
            Add a HTMX template to the HTMXTemplateRenderer instance.
            This can be used to control the response to the client - and the HTMX client itself.
        """
        return self._add_template(
            HtmxTpl,
            template,
            *use_template_if,
            priority=priority,
            hx_location=hx_location,
            hx_push_url=hx_push_url,
            hx_redirect=hx_redirect,
            hx_refresh=hx_refresh,
            hx_replace_url=hx_replace_url,
            hx_reswap=hx_reswap,
            hx_retarget=hx_retarget,
            hx_reselect=hx_reselect,
            hx_trigger=hx_trigger,
            hx_trigger_after_settle=hx_trigger_after_settle,
            hx_trigger_after_swap=hx_trigger_after_swap,
            response_kwargs=response_kwargs
        )
    
    def add_base_check(self, check: _CHECK_T):
        self._base_checks.append(check)
    
    @property
    def can_render_conditionals(self) -> bool:
        """
            Check if the renderer is allowed to render the conditional templates.
        """
        if self.base_template is None:
            # If no base template is set
            # the renderer should choose the first template that matches the condition.
            return True
            
        return _should_use_tpl(self.request, *self._base_checks)

    def render(self, context: dict = None) -> HttpResponse:
        templates = copy.deepcopy(self._templates)
        templates.sort()

        tpl = self.base_template
        if self.can_render_conditionals:
            for template in templates:
                if bool(template):
                    tpl = template
                    break

        tpl = _check_template(tpl)

        context = context or {}
        context.update(self._context)
        context["ACTIVE_TEMPLATE"] = tpl

        return tpl.render(context)
    
    def _add_template(self, 
                      klass: Type[_Tpl],
                      template: Union[str, Tpl],
                      *use_template_if: _CHECK_T,
                      priority: int = 0,
                      response_kwargs: dict = None,
                      **kwargs
            ) -> _Tpl:
        
        if response_kwargs is None:
            response_kwargs = {}

        if isinstance(template, Tpl):
            if use_template_if:
                template.use_template_if += use_template_if

            if response_kwargs:
                template.response_kwargs.update(response_kwargs)
        else:
            template = klass(template, *use_template_if, priority=priority, **kwargs, **response_kwargs)

        template.request = self.request
        self._templates.append(template)
        return template

