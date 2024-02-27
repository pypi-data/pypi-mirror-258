from unittest import TestCase
from ..request import (
    is_htmx,
    is_boosted,
    hx_current_url,
    hx_history_restore_request,
    hx_prompt,
    hx_target,
    hx_trigger,
    hx_trigger_name,
    HXRequest,
    HXBoosted,
    HXCurrentURL,
    HXHistoryRestoreRequest,
    HXPrompt,
    HXTarget,
    HXTrigger,
    HXTriggerName,
)
from .fakes import (
    FakeRequest,
)

class TestRequest(TestCase):
    def test_is_htmx(self):
        self.assertFalse(is_htmx(FakeRequest()))
        self.assertTrue(is_htmx(FakeRequest(headers={HXRequest: "true"})))
        self.assertTrue(is_htmx(FakeRequest(headers={HXRequest: "1"})))
        self.assertFalse(is_htmx(FakeRequest(headers={HXRequest: "false"})))
        self.assertFalse(is_htmx(FakeRequest(headers={HXRequest: "0"})))
        self.assertFalse(is_htmx(FakeRequest(headers={HXRequest: "wrong"})))

    def test_is_boosted(self):
        self.assertFalse(is_boosted(FakeRequest()))
        self.assertTrue(is_boosted(FakeRequest(headers={HXBoosted: "true"})))
        self.assertTrue(is_boosted(FakeRequest(headers={HXBoosted: "1"})))
        self.assertFalse(is_boosted(FakeRequest(headers={HXBoosted: "false"})))
        self.assertFalse(is_boosted(FakeRequest(headers={HXBoosted: "0"})))
        self.assertFalse(is_boosted(FakeRequest(headers={HXBoosted: "wrong"})))

    def test_hx_current_url(self):
        self.assertIsNone(hx_current_url(FakeRequest()))
        self.assertEqual(hx_current_url(FakeRequest(headers={HXCurrentURL: "/foo"})), "/foo")

    def test_hx_history_restore_request(self):
        self.assertFalse(hx_history_restore_request(FakeRequest()))
        self.assertTrue(hx_history_restore_request(FakeRequest(headers={HXHistoryRestoreRequest: "true"})))
        self.assertTrue(hx_history_restore_request(FakeRequest(headers={HXHistoryRestoreRequest: "1"})))
        self.assertFalse(hx_history_restore_request(FakeRequest(headers={HXHistoryRestoreRequest: "false"})))
        self.assertFalse(hx_history_restore_request(FakeRequest(headers={HXHistoryRestoreRequest: "0"})))
        self.assertFalse(hx_history_restore_request(FakeRequest(headers={HXHistoryRestoreRequest: "wrong"})))

    def test_hx_prompt(self):
        self.assertIsNone(hx_prompt(FakeRequest()))
        self.assertEqual(hx_prompt(FakeRequest(headers={HXPrompt: "foo"})), "foo")

    def test_hx_target(self):
        self.assertIsNone(hx_target(FakeRequest()))
        self.assertEqual(hx_target(FakeRequest(headers={HXTarget: "foo"})), "foo")

    def test_hx_trigger(self):
        self.assertIsNone(hx_trigger(FakeRequest()))
        self.assertEqual(hx_trigger(FakeRequest(headers={HXTrigger: "foo"})), "foo")

    def test_hx_trigger_name(self):
        self.assertIsNone(hx_trigger_name(FakeRequest()))
        self.assertEqual(hx_trigger_name(FakeRequest(headers={HXTriggerName: "foo"})), "foo")
