from urllib.parse import urlencode
from django.template import (
    engines, 
    TemplateSyntaxError,
    Template,
)

def buildurlparameters(query, path=None, **kwargs):
    """
    Build a query string from a given context.
    """
    remove = kwargs.pop("remove", None)
    if remove:
        for key in remove.split(","):
            if key in query:
                del query[key]

    prepend = kwargs.pop("prepend", None)
    append = kwargs.pop("append", None)
    
    for key, value in kwargs.items():
        query[key] = value

    encoded =  query.urlencode()

    if prepend and len(encoded) > 0:
        encoded = "?" + encoded

    if append and len(encoded) > 0 and isinstance(append, str):
        encoded = encoded + "&" + append
    elif append and isinstance(append, str):
        encoded = "?" + append
    elif append and isinstance(append, bool):
        if len(encoded) > 0:
            encoded = encoded + "&"
        else:
            encoded = "?"

    if path:
        if not encoded.startswith("?"):
            encoded = "?" + encoded
        encoded = path + encoded
    
    return encoded

def removeduplicateparameters(query):
    params = {}
    for k, v in query.items():
        if isinstance(v, list):
            params[k] = v[-1]
        else:
            params[k] = v
    return urlencode(params)

# https://stackoverflow.com/questions/2167269/load-template-from-a-string-instead-of-from-a-file
def template_from(getter_name: str, template: str, using=None) -> Template:
    """
    Load a template from a file or a string,
    using a given template engine or using the default backends 
    from settings.TEMPLATES if no engine was specified.

    """
    # This function is based on django.template.loader.get_template, 
    chain = []
    engine_list = engines.all() if using is None else [engines[using]]
    for engine in engine_list:
        try:
            fn = getattr(engine, getter_name)
            if fn is None:
                raise AttributeError(f"{engine} does not support loading templates from '{getter_name}'")
            return fn(template)
        
        except TemplateSyntaxError as e:
            chain.append(e)
    raise TemplateSyntaxError(template, chain)
