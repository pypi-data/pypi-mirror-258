from typing import Callable, Iterable, Union
from django.http import HttpRequest
from .request import is_htmx, is_boosted, _get_header_value

# Checks for the HTMXTemplateRenderer instance.
CheckType = Union[
    str, list, bool,
    Callable[[HttpRequest], Union[bool, str]],
]
ValueType = Union[CheckType, Iterable[CheckType]]

def _check_equals(a: str, b: str):
    """Used to check if two string values are equal"""
    return a == b

def _check_contains(a: str, b: str):
    """Used to check if a string contains another string"""
    return b in a

def _check_startswith(a: str, b: str):
    """Used to check if a string starts with another string"""
    return a.startswith(b)

def _check_endswith(a: str, b: str):
    """Used to check if a string ends with another string"""
    return a.endswith(b)

def _maybe_call(value, request):
    """Call the value if it is a callable, otherwise return the value."""
    if callable(value):
        return value(request)
    return value

def _check_bool(request: HttpRequest, data: str, value: bool) -> bool:
    """Match a boolean value."""
    if value:
        return str(data).lower() in ["true", "1"]
    return str(data).lower() in ["false", "0"]

def _check_list(request: HttpRequest, data: str, value: ValueType, case_sensitive: bool, check_fn: Callable[[str, str], bool] = None):
    """Match a list of values."""
    return all(_check_value(request, data, v, case_sensitive, check_fn) for v in value)

def _check_str(request: HttpRequest, data: str, value: str, case_sensitive: bool, check_fn: Callable[[str, str], bool] = None):
    """Match a string value."""
    if case_sensitive:
        if check_fn(data, value):
            return True
    else:
        if check_fn(data.lower(), value.lower()):
            return True
    return False

def _check_value(request: HttpRequest, data: str, value: ValueType, case_sensitive: bool, check_fn: Callable[[str, str], bool]) -> bool:
    value = _maybe_call(value, request)

    if isinstance(value, (list, tuple)):
        if _check_list(request, data, value, case_sensitive, check_fn, request):
            return True
    elif isinstance(value, bool):
        if _check_bool(request, data, value, request):
            return True
    elif isinstance(value, str):
        if _check_str(request, data, value, case_sensitive, check_fn):
            return True
    else:
        raise ValueError(f"Invalid value type: {type(value)}")
    
    return False

def _create_header_check(header: str, value: ValueType, case_sensitive: bool, check_fn: Callable[[str, str], bool]) -> bool:
    def check(request):
        header_value = _get_header_value(request, header)
        if header_value is None:
            return bool(header_value) == bool(value)

        return _check_value(request, header_value, value, case_sensitive, check_fn)
    
    name = check_fn.__name__.strip("_")
    check.__name__ = f"_if_header_{name}"
    
    return check

def _if_method_equals(method: str) -> Callable[[HttpRequest], bool]:
    """
    Check if the request method equals the given method.
    """
    if isinstance(method, str):
        method = [method.lower()]
    else:
        method = [m.lower() for m in method]

    def check(request: HttpRequest):
        return request.method.lower() in method
    
    return check

def _if_header_equals(header: str, value: ValueType, case_sensitive: bool = False) -> bool:
    """
    Check if the header value equals the given value.
    """
    return _create_header_check(header, value, case_sensitive, _check_equals)

def _if_header_contains(header: str, value: ValueType, case_sensitive: bool = False) -> bool:
    """
    Check if the header value contains the given value.
    """
    return _create_header_check(header, value, case_sensitive, _check_contains)

def _if_header_startswith(header: str, value: ValueType, case_sensitive: bool = False) -> bool:
    """
    Check if the header value starts with the given value.
    """
    return _create_header_check(header, value, case_sensitive, _check_startswith)

def _if_header_endswith(header: str, value: ValueType, case_sensitive: bool = False) -> bool:
    """
    Check if the header value ends with the given value.
    """
    return _create_header_check(header, value, case_sensitive, _check_endswith)

def _if_user_has_perm(perm: str | Callable[[HttpRequest], str]) -> bool:
    """
    Check if the user has the given permission.
    """
    _perm = perm

    def check(request: HttpRequest):
        perm = _maybe_call(_perm, request)
        if hasattr(request, "user"):
            return request.user.has_perm(perm)
        return False
    
    return check

def _if_user_authenticated(request: HttpRequest) -> bool:
    """
    Check if the user is authenticated.
    """
    if hasattr(request, "user"):
        return request.user.is_authenticated
    
    return False

def _if_value_in_params(param: str, value: Union[Union[str, list[str]], Callable[[HttpRequest], Union[str, list[str]]]], method: str = "GET", case_sensitive: bool = False) -> bool:
    """
    Check if the given value is in the request parameters.
    """
    _value = value

    def check(request: HttpRequest):
        value = _maybe_call(_value, request)
        if not request.method == method:
            return False

        data = getattr(request, method)
        data = data.getlist(param)

        return any(
            _check_value(request, d, value, case_sensitive, _check_contains) 
            for d in data
        )
    
    return check

class BaseCheck:
    __repr__format__ = None

    def __init__(self, check: Callable):
        if check is None:
            raise ValueError("Check must be a callable, not None")
        self.check = check

    def __call__(self, request):
        return self.check(request)
    
    def __and__(self, other):
        return And(self, other)
    
    def __rand__(self, other):
        return And(other, self)
    
    def __or__(self, other):
        return Or(self, other)
    
    def __ror__(self, other):
        return Or(other, self)
    
    def __invert__(self):
        return Not(self)
    
    def __repr__(self):
        if self.__repr__format__:
            return self.__repr__format__.format(self=self)
        return f"{self.__class__.__name__}"
    
class Lambda(BaseCheck):
    """
        Semantic sugar for creating a check from a lambda or other callable.
        This class is not necessary, but it can be useful for readability.
    """

class And(BaseCheck):
    def __init__(self, *checks: BaseCheck):
        def combined_check(request):
            return all(check(request) for check in checks)
        self._checks = checks
        super().__init__(combined_check)

    def __repr__(self):
        return f"({' && '.join(repr(check) for check in self._checks)})"

class Or(BaseCheck):
    def __init__(self, *checks: BaseCheck):
        def combined_check(request):
            return any(check(request) for check in checks)
        self._checks = checks
        super().__init__(combined_check)

    def __repr__(self):
        return f"({' || '.join(repr(check) for check in self._checks)})"
    
class Not(BaseCheck):
    def __repr__(self):
        return f"!{repr(self.check)}"
    
    def __call__(self, request):
        return not self.check(request)
    
class _HeaderCheck(BaseCheck):
    __repr__format__ = "[{self.header}] == {self.value}"
    __check_func__ = None

    def __init__(self, header: str, value: ValueType, case_sensitive: bool = False):
        self.header = header
        self.value = value
        self.case_sensitive = case_sensitive
        _check = self.__class__.__check_func__
        super().__init__(_check(header, value, case_sensitive))

class HeaderEquals(_HeaderCheck):
    __check_func__ = _if_header_equals

class HeaderContains(_HeaderCheck):
    __check_func__ = _if_header_contains

class HeaderStartswith(_HeaderCheck):
    __check_func__ = _if_header_startswith

class HeaderEndswith(_HeaderCheck):
    __check_func__ = _if_header_endswith

class UserHasPerm(BaseCheck):
    __repr__format__ = "{self.perm}"

    def __init__(self, perm: str | Callable[[HttpRequest], str]):
        self.perm = perm
        super().__init__(_if_user_has_perm(perm))

class UserAuthenticated(BaseCheck):
    def __init__(self):
        super().__init__(_if_user_authenticated)

class HasValue(BaseCheck):
    __repr__format__ = "[{self.method}/{self.param}] == {self.value}"

    def __init__(self, param: str, value: Union[Union[str, list[str]], Callable[[HttpRequest], Union[str, list[str]]]], method: str = "GET", case_sensitive: bool = False):
        self.param = param
        self.method = method
        self.value = value
        super().__init__(_if_value_in_params(param, value, method, case_sensitive))

class IsMethod(BaseCheck):
    __repr__format__ = "{self.method}"

    def __init__(self, method: Union[str, list[str]]):
        self.method = method
        super().__init__(_if_method_equals(method))

class Accepts(BaseCheck):
    def __init__(self, *content_type: str):
        self.content_type = content_type
        super().__init__(self._check_accepts)

    def _check_accepts(self, request: HttpRequest):
        return any(request.accepts(content_type) for content_type in self.content_type)

class ContentType(BaseCheck):
    def __init__(self, content_type: str):
        self.content_type = content_type
        super().__init__(self._check_content_type)

    def _check_content_type(self, request: HttpRequest):
        return request.content_type == self.content_type

class FormValid(BaseCheck):
    """
        Check if the form is valid.
    """
    def __init__(self, form):
        self.form = form

    def __call__(self, request):
        return self.form.is_valid()

class IsHtmx(BaseCheck):
    def __init__(self):
        super().__init__(is_htmx)

class IsBoosted(BaseCheck):
    def __init__(self):
        super().__init__(is_boosted)
