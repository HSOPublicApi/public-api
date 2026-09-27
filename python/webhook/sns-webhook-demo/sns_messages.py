"""Pure helpers for handling AWS SNS HTTP(S) subscription messages.

Kept free of Flask so each piece is trivially unit-testable. The three SNS
message types delivered to an HTTP(S) subscription are handled here:
  * SubscriptionConfirmation - confirm by visiting the SubscribeURL
  * Notification             - the actual published messages
  * UnsubscribeConfirmation  - sent when the subscription is removed

It also verifies each message's cryptographic signature so forged posts to the
public endpoint are rejected before they are acted on.
"""
from __future__ import annotations

import base64
import logging
import re
from functools import lru_cache
from typing import Callable
from urllib.parse import urlparse

import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

logger = logging.getLogger("sns_webhook")

# SNS sets this header on every delivery; it mirrors the body's "Type" field.
MESSAGE_TYPE_HEADER = "x-amz-sns-message-type"

SUBSCRIPTION_CONFIRMATION = "SubscriptionConfirmation"
NOTIFICATION = "Notification"
UNSUBSCRIBE_CONFIRMATION = "UnsubscribeConfirmation"

# A callable performing an HTTP GET and returning the status code. Injectable
# so tests can assert the SubscribeURL is fetched without real network I/O.
HttpGet = Callable[[str], int]

# The fields that make up the canonical "string to sign", in the exact order
# AWS specifies, per message type. Subject is only included when present.
_SIGNING_KEYS = {
    NOTIFICATION: ["Message", "MessageId", "Subject", "Timestamp", "TopicArn", "Type"],
    SUBSCRIPTION_CONFIRMATION: [
        "Message", "MessageId", "SubscribeURL", "Timestamp", "Token", "TopicArn", "Type",
    ],
    UNSUBSCRIBE_CONFIRMATION: [
        "Message", "MessageId", "SubscribeURL", "Timestamp", "Token", "TopicArn", "Type",
    ],
}

# The signing certificate must come from an AWS SNS host over HTTPS. This is the
# SSRF guard: it is checked BEFORE the certificate URL is ever fetched, so a
# forged message cannot make the app reach an attacker-controlled host.
_ALLOWED_CERT_HOST = re.compile(r"^sns\.[a-z0-9-]+\.amazonaws\.com(\.cn)?$")

# A callable that fetches the signing certificate PEM bytes for a URL.
CertFetch = Callable[[str], bytes]


class SignatureError(Exception):
    """Raised when an SNS message cannot be verified as authentic."""


def _default_http_get(url: str) -> int:
    return requests.get(url, timeout=10).status_code


def message_type(headers: dict, body: dict) -> str | None:
    """Resolve the SNS message type from the header, falling back to the body.

    The ``x-amz-sns-message-type`` header is authoritative; the body's ``Type``
    field carries the same value and is used when the header is absent.
    """
    if headers:
        for key, value in headers.items():
            if key.lower() == MESSAGE_TYPE_HEADER:
                return value
    return body.get("Type") if body else None


def _canonical_string(message: dict) -> bytes:
    """Build the exact byte string AWS signed, per the message type's field list."""
    msg_type = message.get("Type")
    keys = _SIGNING_KEYS.get(msg_type)
    if not keys:
        raise SignatureError(f"cannot verify unrecognized message type: {msg_type!r}")
    parts: list[str] = []
    for key in keys:
        if key == "Subject" and key not in message:
            continue  # Subject is optional; omitted from the signed string when absent
        if key not in message:
            raise SignatureError(f"message missing field required for signing: {key}")
        parts.append(key)
        parts.append(str(message[key]))
    return ("\n".join(parts) + "\n").encode("utf-8")


@lru_cache(maxsize=32)
def _fetch_certificate(cert_url: str) -> bytes:
    return requests.get(cert_url, timeout=10).content


def verify_signature(message: dict, fetch_cert: CertFetch | None = None) -> None:
    """Verify an SNS message's signature; raise SignatureError if it is not authentic.

    Supports SignatureVersion 1 (SHA1) and 2 (SHA256). The signing certificate
    URL is host-allow-listed to ``sns.<region>.amazonaws.com`` and only fetched
    after that check passes, so a forged message cannot trigger an outbound
    request to an arbitrary host.
    """
    cert_url = message.get("SigningCertURL", "") or ""
    parsed = urlparse(cert_url)
    if parsed.scheme != "https" or not _ALLOWED_CERT_HOST.match(parsed.netloc):
        raise SignatureError(f"untrusted SigningCertURL: {cert_url!r}")

    signature_b64 = message.get("Signature")
    if not signature_b64:
        raise SignatureError("message has no Signature")
    try:
        signature = base64.b64decode(signature_b64)
    except Exception as exc:
        raise SignatureError(f"malformed Signature: {exc}") from exc

    version = str(message.get("SignatureVersion", "1"))
    if version == "1":
        algorithm: hashes.HashAlgorithm = hashes.SHA1()
    elif version == "2":
        algorithm = hashes.SHA256()
    else:
        raise SignatureError(f"unsupported SignatureVersion: {version!r}")

    fetch = fetch_cert or _fetch_certificate
    try:
        certificate = x509.load_pem_x509_certificate(fetch(cert_url))
    except Exception as exc:
        raise SignatureError(f"could not load signing certificate: {exc}") from exc

    try:
        certificate.public_key().verify(  # type: ignore[union-attr]
            signature, _canonical_string(message), padding.PKCS1v15(), algorithm
        )
    except SignatureError:
        raise
    except Exception as exc:  # cryptography.exceptions.InvalidSignature and friends
        raise SignatureError("signature verification failed") from exc


def confirm_subscription(message: dict, http_get: HttpGet = _default_http_get) -> int:
    """Confirm an SNS subscription by visiting its SubscribeURL.

    Returns the HTTP status code from that GET. A missing SubscribeURL raises
    ValueError so the caller can surface it instead of failing silently.
    """
    subscribe_url = message.get("SubscribeURL")
    if not subscribe_url:
        raise ValueError("SubscriptionConfirmation message has no SubscribeURL")
    logger.info("Confirming subscription via SubscribeURL: %s", subscribe_url)
    status = http_get(subscribe_url)
    logger.info("SubscribeURL responded with HTTP %s", status)
    return status


def format_notification(message: dict) -> str:
    """Render a Notification for human-readable console logging."""
    fields = {
        "MessageId": message.get("MessageId"),
        "TopicArn": message.get("TopicArn"),
        "Subject": message.get("Subject"),
        "Timestamp": message.get("Timestamp"),
        "Message": message.get("Message"),
    }
    body = "\n".join(f"  {name}: {value}" for name, value in fields.items())
    return "Notification received:\n" + body
