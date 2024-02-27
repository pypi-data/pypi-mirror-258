from unittest import TestCase
from ..request import (
    HXRequest,
    HXBoosted,
)
from ..check import (
    And,
    Or,
    Not,
    HeaderEquals,
    HeaderContains,
    HeaderStartswith,
    HeaderEndswith,
    UserHasPerm,
    UserAuthenticated,
    HasValue,
    IsMethod,
    Accepts,
    ContentType,
    Lambda,
    FormValid,
    IsHtmx,
    IsBoosted,
)
from .fakes import (
    FakeRequest,
    FakeUser,
    FakeForm,
)

class TestChecks(TestCase):
    def test_and(self):
        check = And(
            HeaderEquals("Content-Type", "application/json"),
            HeaderContains("Accept", "application/json"),
        )
        self.assertTrue(check(FakeRequest(headers={"Content-Type": "application/json", "Accept": "application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Content-Type": "application/json", "Accept": "text/html"})))
        self.assertFalse(check(FakeRequest(headers={})))

    def test_or(self):
        check = Or(
            HeaderEquals("Content-Type", "application/json"),
            HeaderContains("Accept", "application/json"),
        )
        self.assertTrue(check(FakeRequest(headers={"Content-Type": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        })))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))


    def test_not(self):
        check = Not(HeaderEquals("Content-Type", "application/json"))
        self.assertFalse(check(FakeRequest(headers={"Content-Type": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Content-Type": "application/xml"})))

    def test_header_equals(self):
        check = HeaderEquals("Accept", "application/json")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

    def test_header_contains(self):
        check = HeaderContains("Accept", "json")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "text/html, application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

    def test_header_startswith(self):
        check = HeaderStartswith("Accept", "application")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/xml"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

    def test_header_endswith(self):
        check = HeaderEndswith("Accept", "json")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "text/html, application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

    def test_user_has_perm(self):
        check = UserHasPerm("perm")
        self.assertTrue(check(FakeRequest(user=FakeUser(perms=["perm"]))))
        self.assertFalse(check(FakeRequest(user=FakeUser(perms=["other"]))))
        self.assertFalse(check(FakeRequest(user=FakeUser(perms=[]))))

    def test_user_authenticated(self):
        check = UserAuthenticated()
        self.assertTrue(check(FakeRequest(user=FakeUser(is_authenticated=True))))
        self.assertFalse(check(FakeRequest(user=FakeUser(is_authenticated=False))))

    def test_has_value(self):
        check = HasValue("key", "value", method="POST")
        self.assertTrue(check(FakeRequest(method="POST", data={"key": "value"})))
        self.assertFalse(check(FakeRequest(method="POST", data={"key": "other"})))
        self.assertFalse(check(FakeRequest(method="GET", data={"key": "value"})))

    def test_is_method(self):
        check = IsMethod("POST")
        self.assertTrue(check(FakeRequest(method="POST")))
        self.assertFalse(check(FakeRequest(method="GET")))

    def test_accepts(self):
        check = Accepts("application/json")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/*"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "text/html, application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

        check = Accepts("application/json", "application/xml")
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/json"})))
        self.assertTrue(check(FakeRequest(headers={"Accept": "application/xml"})))
        self.assertFalse(check(FakeRequest(headers={"Accept": "text/html"})))

    def test_content_type(self):
        check = ContentType("application/json")
        self.assertTrue(check(FakeRequest(headers={"Content-Type": "application/json"})))
        self.assertFalse(check(FakeRequest(headers={"Content-Type": "text/html"})))

    def test_lambda(self):
        check = Lambda(lambda request: request.method == "POST")
        self.assertTrue(check(FakeRequest(method="POST")))
        self.assertFalse(check(FakeRequest(method="GET")))

    def test_form_valid(self):
        self.assertTrue(FormValid(FakeForm(True))(FakeRequest()))
        self.assertFalse(FormValid(FakeForm(False))(FakeRequest()))

    def test_is_htmx(self):
        check = IsHtmx()
        self.assertTrue(check(FakeRequest(headers={HXRequest: "true"})))
        self.assertFalse(check(FakeRequest(headers={HXRequest: "false"})))
        self.assertFalse(check(FakeRequest()))

    def test_is_boosted(self):
        check = IsBoosted()
        self.assertTrue(check(FakeRequest(headers={HXBoosted: "true"})))
        self.assertFalse(check(FakeRequest(headers={HXBoosted: "false"})))
        self.assertFalse(check(FakeRequest()))

    def test_logical_combinations(self):
        check = \
        UserAuthenticated() \
        & (
            ContentType("application/json") 
            | Accepts("application/json")) \
        | ~IsHtmx() & IsBoosted()

        requests = [
            (FakeRequest(user=FakeUser(is_authenticated=True), headers={"Content-Type": "application/json"}), True),
            (FakeRequest(user=FakeUser(is_authenticated=True), headers={"Accept": "application/json"}), True),
            (FakeRequest(user=FakeUser(is_authenticated=True), headers={"Content-Type": "application/json", "Accept": "*/json"}), True),
            (FakeRequest(user=FakeUser(is_authenticated=True), headers={"Accept": "text/html"}), False),
            (FakeRequest(user=FakeUser(is_authenticated=False), headers={"Content-Type": "application/json"}), False),
            (FakeRequest(user=FakeUser(is_authenticated=True), headers={}), False),
            (FakeRequest(headers={HXRequest: "true", HXBoosted: "true"}), False),
            (FakeRequest(headers={HXRequest: "true", HXBoosted: "false"}), False),
            (FakeRequest(headers={HXRequest: "false", HXBoosted: "true"}), True),
        ]

        for request, expected in requests:
            self.assertEqual(check(request), expected)


