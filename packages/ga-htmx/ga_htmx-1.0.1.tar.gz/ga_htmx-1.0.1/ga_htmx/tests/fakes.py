from django.utils.functional import cached_property
from django.http.request import parse_accept_header

class FakeUser:
    def __init__(self, perms=None, is_authenticated=True):
        self.perms = perms or []
        self.is_authenticated = is_authenticated

    def has_perm(self, perm):
        return perm in self.perms
    
    def __repr__(self):
        return f"<User: perms={self.perms} is_authenticated={self.is_authenticated}>"

def getlist(self, key):
    data = self.get(key, [])
    if isinstance(data, list):
        return data
    return [data]

class FakeForm:
    def __init__(self, is_valid=True):
        self._valid = is_valid

    def is_valid(self):
        return self._valid
    
class FakeRequestData(dict):
    def getlist(self, key):
        return getlist(self, key)

class FakeRequest:
    def __init__(self, headers=None, user=None, method="GET", data=None):
        self.headers = headers or {}
        self.user = user or FakeUser()
        self.method = method
        data = data or {}
        setattr(self, method, FakeRequestData(data.items()))

    @property
    def content_type(self):
        return self.headers.get("Content-Type", "")
    
    @cached_property
    def accepted_types(self):
        """Return a list of MediaType instances."""
        return parse_accept_header(self.headers.get("Accept", "*/*"))

    def accepts(self, media_type):
        if "Accept" not in self.headers:
            return False
        
        return any(
            accepted_type.match(media_type) for accepted_type in self.accepted_types
        )

        
    
