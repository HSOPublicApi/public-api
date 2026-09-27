# SNS Webhook Subscriber Demo

The smallest useful example of the **subscriber side** of AWS SNS: a Flask app
exposing one endpoint that (1) confirms an SNS subscription and (2) receives the
notifications SNS pushes to it. It is a self-contained learning reference you
can clone and run in a few minutes.

## What it does (and doesn't)

- **Does:** verifies each message's **SNS signature** (rejecting forgeries with
  HTTP 403), then `POST /sns` handles `SubscriptionConfirmation` (by GETting the
  message's `SubscribeURL`) and `Notification` (logs it), and acks
  `UnsubscribeConfirmation`. Always returns 200 for accepted, authentic messages.
- **Doesn't:** create the topic or subscription, or persist anything. Those are
  intentionally out of scope to keep it minimal.

## Run it

```bash
cd sns-webhook-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py            # listens on 0.0.0.0:5000 (override with HOST/PORT)
```

## Point a real SNS topic at it

SNS must reach your local app over public HTTPS, so expose it with a tunnel:

```bash
ngrok http 5000          # gives you https://<something>.ngrok-free.app
```

Then, in AWS (console or CLI — this app does none of this for you):

1. Create/choose an SNS topic.
2. Create an **HTTPS** subscription whose endpoint is `https://<tunnel>/sns`.
3. SNS immediately POSTs a `SubscriptionConfirmation`; the app confirms it by
   visiting the `SubscribeURL`, and the subscription becomes `Confirmed`.
4. Publish to the topic; each message arrives at `/sns` and is logged.

## Test it

```bash
cd sns-webhook-demo
pip install pytest
python -m pytest tests -v
```

## Security

- **Signature verification is on.** Every message is checked against its SNS
  signature (SignatureVersion 1 and 2) before the app acts on it; anything that
  fails is rejected with HTTP 403. The signing certificate is only fetched from
  an `sns.<region>.amazonaws.com` host over HTTPS, which also closes the SSRF
  path a forged `SubscriptionConfirmation` would otherwise open.
- **Not hardened for production.** It runs Flask's development server and logs
  full message bodies. Before real production use, run it behind a proper WSGI
  server (e.g. gunicorn) + TLS, and redact/limit logging if your messages carry
  sensitive data.
