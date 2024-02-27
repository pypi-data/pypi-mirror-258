from typing import Union, TYPE_CHECKING
from django.http import HttpResponse
from .request import (
    is_htmx,
    is_boosted,
    hx_current_url,
    hx_history_restore_request,
    hx_prompt,
    hx_target,
    hx_trigger,
    hx_trigger_name,
)
from .render import (
    _CHECK_T,
    _Tpl,
    HTMXTemplateRenderer,
    Tpl,
    HtmxTpl,
)

if TYPE_CHECKING:
    from .types import HTMXRequest


class HTMXDetails:
    """
    A class that holds details about the current request being processed.

    This class is used to determine if the current request is an HTMX request, and to provide

    information about the request to the view function.

    Args:
        request: The current request being processed.

    Attributes:
        request: The current request being processed.
        htmx: A boolean indicating if the current request is an HTMX request.
        boosted: A boolean indicating if the current request is a boosted request.
        current_url: The current URL of the request.
        history_restore_request: A boolean indicating if the current request is a history restore request.
        prompt: A boolean indicating if the current request is a prompt request.
        target: The target of the request.
        trigger: The trigger of the request.
        trigger_name: The name of the trigger of the request.
        _renderer: The HTMXTemplateRenderer instance used to render templates and redirects.
    """
    def __init__(self, request: "HTMXRequest"):
        self.request                  = request
        self.htmx                     = is_htmx(request)
        self.boosted                  = is_boosted(request)
        self.current_url              = hx_current_url(request)
        self.history_restore_request  = hx_history_restore_request(request)
        self.prompt                   = hx_prompt(request)
        self.target                   = hx_target(request)
        self.trigger                  = hx_trigger(request)
        self.trigger_name             = hx_trigger_name(request)
        self._renderer                = HTMXTemplateRenderer(request)
    
    @property
    def base_template(self) -> _Tpl:
        return self._renderer.base_template

    @base_template.setter
    def base_template(self, value: Union[str, _Tpl]):
        self._renderer.base_template = value
    
    def __bool__(self):
        return self.htmx
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.request}, is_htmx={self.htmx}, is_boosted={self.boosted})"

    def add_context(self, **kwargs):
        """
        Add context data to the HTMXTemplateRenderer instance.
        """
        return self._renderer.add_context(**kwargs)

    def get_context(self):
        """
        Get the context data from the HTMXTemplateRenderer instance.
        """
        return self._renderer.context
    
    def add_redirect(self, to_url: Union[str, Tpl], *use_redirect_if: _CHECK_T, priority: int = 0, **response_kwargs):
        """
        Add a redirect to the HTMXTemplateRenderer instance.
        """
        return self._renderer.add_redirect(to_url, *use_redirect_if, priority=priority, **response_kwargs)

    def add_json(self, data: dict, *respond_json_if: _CHECK_T, priority: int = 0, **response_kwargs):
        """
        Add a JSON response to the HTMXTemplateRenderer instance.
        """
        return self._renderer.add_json(data, *respond_json_if, priority=priority, **response_kwargs)
        
    def add_template(self, template: Union[str, Tpl], *use_template_if: _CHECK_T, priority: int = 0, **response_kwargs):
        """
        Add a template to the HTMXTemplateRenderer instance.
        """
        return self._renderer.add_template(template, *use_template_if, priority=priority, **response_kwargs)

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
        return self._renderer.add_htmx_template(
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
            **response_kwargs
        )
    
    def add_base_check(self, check: _CHECK_T):
        """
        Add a check to the HTMXTemplateRenderer instance.
        """
        return self._renderer.add_base_check(check)
  
    def render(self, context: dict = None) -> HttpResponse:
        """
        Render the response using the HTMXTemplateRenderer instance.
        """
        return self._renderer.render(context)
