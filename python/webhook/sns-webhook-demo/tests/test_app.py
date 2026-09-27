import json

import pytest

import app as app_module
import sns_messages
from app import create_app
from sns_messages import SignatureError


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


@pytest.fixture(autouse=True)
def trust_signatures(monkeypatch):
    """Most endpoint tests exercise routing, not crypto, so treat signatures as
    valid by default. The dedicated signature tests live in test_sns_messages.py,
    and test_invalid_signature_returns_403 overrides this to force a failure."""
    monkeypatch.setattr(app_module, "verify_signature", lambda body: None)


def _post(client, message, msg_type):
    return client.post(
        "/sns",
        data=json.dumps(message),
        headers={"x-amz-sns-message-type": msg_type},
        content_type="application/json",
    )


def test_subscription_confirmation_triggers_confirm(client, monkeypatch):
    seen = {}

    def fake_get(url, timeout=None):
        seen["url"] = url
        return type("R", (), {"status_code": 200})()

    monkeypatch.setattr(sns_messages.requests, "get", fake_get)

    resp = _post(
        client,
        {"Type": "SubscriptionConfirmation", "SubscribeURL": "https://sns.example/c"},
        "SubscriptionConfirmation",
    )
    assert resp.status_code == 200
    assert seen["url"] == "https://sns.example/c"


def test_notification_is_logged_and_acked(client):
    resp = _post(client, {"Type": "Notification", "MessageId": "m1", "Message": "hi"}, "Notification")
    assert resp.status_code == 200


def test_unsubscribe_confirmation_acked(client):
    resp = _post(client, {"Type": "UnsubscribeConfirmation", "TopicArn": "arn:demo"}, "UnsubscribeConfirmation")
    assert resp.status_code == 200


def test_malformed_body_returns_400_not_500(client):
    resp = client.post("/sns", data="not json", content_type="application/json")
    assert resp.status_code == 400


def test_invalid_signature_returns_403(client, monkeypatch):
    def reject(body):
        raise SignatureError("bad signature")

    monkeypatch.setattr(app_module, "verify_signature", reject)
    resp = _post(client, {"Type": "Notification", "MessageId": "m1", "Message": "hi"}, "Notification")
    assert resp.status_code == 403
