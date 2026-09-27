import base64
import datetime

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

from sns_messages import (
    SignatureError,
    _canonical_string,
    confirm_subscription,
    format_notification,
    message_type,
    verify_signature,
)


# --- message_type -----------------------------------------------------------


def test_message_type_prefers_header():
    headers = {"X-Amz-Sns-Message-Type": "Notification"}
    body = {"Type": "SubscriptionConfirmation"}
    assert message_type(headers, body) == "Notification"


def test_message_type_falls_back_to_body():
    assert message_type({}, {"Type": "SubscriptionConfirmation"}) == "SubscriptionConfirmation"


def test_message_type_none_when_absent():
    assert message_type({}, {}) is None


# --- confirm_subscription ----------------------------------------------------


def test_confirm_subscription_visits_subscribe_url():
    seen = {}

    def fake_get(url):
        seen["url"] = url
        return 200

    status = confirm_subscription(
        {"SubscribeURL": "https://sns.example/confirm?x=1"}, http_get=fake_get
    )
    assert status == 200
    assert seen["url"] == "https://sns.example/confirm?x=1"


def test_confirm_subscription_without_url_raises():
    with pytest.raises(ValueError):
        confirm_subscription({}, http_get=lambda url: 200)


# --- format_notification -----------------------------------------------------


def test_format_notification_includes_key_fields():
    message = {
        "MessageId": "abc-123",
        "TopicArn": "arn:aws:sns:us-east-1:111122223333:demo",
        "Subject": "Hello",
        "Timestamp": "2026-01-01T00:00:00.000Z",
        "Message": "the payload",
    }
    out = format_notification(message)
    for expected in ("abc-123", "arn:aws:sns:us-east-1:111122223333:demo", "Hello", "the payload"):
        assert expected in out


# --- signature verification --------------------------------------------------


def _make_key_and_cert():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "sns.us-east-1.amazonaws.com")])
    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=1))
        .sign(key, hashes.SHA256())
    )
    return key, cert.public_bytes(serialization.Encoding.PEM)


def _sign(key, message, version="1"):
    algorithm = hashes.SHA1() if version == "1" else hashes.SHA256()
    signature = key.sign(_canonical_string(message), padding.PKCS1v15(), algorithm)
    message["SignatureVersion"] = version
    message["Signature"] = base64.b64encode(signature).decode()
    return message


def _notification():
    return {
        "Type": "Notification",
        "MessageId": "m-1",
        "Subject": "hi",
        "Timestamp": "2026-01-01T00:00:00.000Z",
        "TopicArn": "arn:aws:sns:us-east-1:111122223333:demo",
        "Message": "the payload",
        "SigningCertURL": "https://sns.us-east-1.amazonaws.com/cert.pem",
    }


@pytest.mark.parametrize("version", ["1", "2"])
def test_verify_signature_accepts_valid(version):
    key, cert_pem = _make_key_and_cert()
    message = _sign(key, _notification(), version)
    # Should not raise.
    verify_signature(message, fetch_cert=lambda url: cert_pem)


def test_verify_signature_rejects_tampered_message():
    key, cert_pem = _make_key_and_cert()
    message = _sign(key, _notification(), "1")
    message["Message"] = "tampered after signing"
    with pytest.raises(SignatureError):
        verify_signature(message, fetch_cert=lambda url: cert_pem)


def test_verify_signature_rejects_untrusted_cert_url_without_fetching():
    """SSRF guard: a non-AWS cert host is rejected and never fetched."""
    fetched = []

    def fetch(url):
        fetched.append(url)
        return b""

    message = _notification()
    message["SigningCertURL"] = "https://evil.example.com/cert.pem"
    message["Signature"] = base64.b64encode(b"whatever").decode()
    with pytest.raises(SignatureError):
        verify_signature(message, fetch_cert=fetch)
    assert fetched == []  # the attacker-controlled URL was never contacted


def test_verify_signature_rejects_non_https_cert_url():
    message = _notification()
    message["SigningCertURL"] = "http://sns.us-east-1.amazonaws.com/cert.pem"
    message["Signature"] = base64.b64encode(b"whatever").decode()
    with pytest.raises(SignatureError):
        verify_signature(message, fetch_cert=lambda url: b"")
