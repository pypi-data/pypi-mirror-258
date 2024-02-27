from urllib.parse import unquote


HXRequest               = "HX-Request"
HXBoosted               = "HX-Boosted"
HXCurrentURL            = "HX-Current-URL"
HXHistoryRestoreRequest = "HX-History-Restore-Request"
HXPrompt                = "HX-Prompt"
HXTarget                = "HX-Target"
HXTrigger               = "HX-Trigger"
HXTriggerName           = "HX-Trigger-Name"


def _get_header_value(request, name: str) -> str | None:
    value = request.headers.get(name) or None
    if value:
        if request.headers.get(f"{name}-URI-AutoEncoded") == "true":
            value = unquote(value)
    return value

def is_htmx(request) -> bool:
    return _get_header_value(request , HXRequest) in ["true", "1"]

def is_boosted(request) -> bool:
    return _get_header_value(request , HXBoosted) in ["true", "1"]

def hx_current_url(request) -> str | None:
    return _get_header_value(request , HXCurrentURL)
    
def hx_history_restore_request(request) -> bool:
    return _get_header_value(request, HXHistoryRestoreRequest) in ["true", "1"]

def hx_prompt(request) -> str | None:
    return _get_header_value(request, HXPrompt)

def hx_target(request) -> str | None:
    return _get_header_value(request, HXTarget)

def hx_trigger(request) -> str | None:
    return _get_header_value(request, HXTrigger)

def hx_trigger_name(request) -> str | None:
    return _get_header_value(request, HXTriggerName)
