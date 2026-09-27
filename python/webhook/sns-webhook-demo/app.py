"""Minimal Flask app that acts as an AWS SNS HTTP(S) subscription endpoint.

It does exactly two things, and nothing else:
  1. Confirms the subscription when SNS posts a SubscriptionConfirmation
     (by visiting the message's SubscribeURL).
  2. Receives and logs the Notification messages SNS pushes afterwards.

It does NOT create the topic or subscription, verify message signatures, or
persist anything. See README.md.
"""
from __future__ import annotations

import logging
import os

from flask import Flask, request

from sns_messages import (
    NOTIFICATION,
    SUBSCRIPTION_CONFIRMATION,
    UNSUBSCRIBE_CONFIRMATION,
    SignatureError,
    confirm_subscription,
    format_notification,
    message_type,
    verify_signature,
)

logger = logging.getLogger("sns_webhook")


def create_app() -> Flask:
    app = Flask(__name__)

    @app.post("/sns")
    def sns_webhook():
        # SNS posts JSON with Content-Type text/plain, so parse it directly and
        # tolerate a malformed body without crashing the process.
        body = request.get_json(force=True, silent=True)
        if not isinstance(body, dict):
            logger.warning("Rejected malformed SNS payload")
            return {"error": "expected a JSON SNS message object"}, 400

        # Verify authenticity BEFORE acting on the message (confirming a
        # subscription or logging a notification). This rejects forged posts and
        # blocks the SSRF vector where a fake SubscriptionConfirmation would make
        # the app fetch an attacker-controlled SubscribeURL.
        try:
            verify_signature(body)
        except SignatureError as exc:
            logger.warning("Rejected SNS message with invalid signature: %s", exc)
            return {"error": "signature verification failed"}, 403

        msg_type = message_type(dict(request.headers), body)

        if msg_type == SUBSCRIPTION_CONFIRMATION:
            try:
                confirm_subscription(body)
            except ValueError as exc:
                logger.error("Could not confirm subscription: %s", exc)
                return {"error": str(exc)}, 400
            except Exception as exc:  # surface network/HTTP failures, don't swallow
                logger.error("Error reaching SubscribeURL: %s", exc)
                return {"error": "failed to reach SubscribeURL"}, 502
            return {"status": "subscription confirmed"}, 200

        if msg_type == NOTIFICATION:
            logger.info(format_notification(body))
            return {"status": "notification received"}, 200

        if msg_type == UNSUBSCRIBE_CONFIRMATION:
            logger.info("Unsubscribe confirmation for TopicArn: %s", body.get("TopicArn"))
            return {"status": "unsubscribe acknowledged"}, 200

        logger.warning("Unknown SNS message type: %s", msg_type)
        return {"error": f"unknown SNS message type: {msg_type}"}, 400

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app


app = create_app()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    logger.info("Starting SNS webhook subscriber on %s:%s", host, port)
    app.run(host=host, port=port)
