#!/usr/bin/env python3
"""
Read Gmail items for Claudia from local CLI OAuth profiles.

This local helper can read the UCSD mailbox through the separate gcloud OAuth
profile at ~/.config/claudia/gmail-second/. The personal Gmail connector lives
inside Codex, so it must still be supplied as JSON by the orchestrator when
available.
"""

import argparse
import base64
import json
import os
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GMAIL_API = "https://gmail.googleapis.com/gmail/v1"
DEFAULT_GCLOUD_CONFIG = Path.home() / ".config/claudia/gmail-second/gcloud"
DEFAULT_CLIENT_ID_FILE = Path.home() / ".config/claudia/gmail-second/client_secret.json"
GCLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
ACCOUNTS = {
    "ucsd": {
        "email": "eagunias@ucsd.edu",
        "gcloud_config": DEFAULT_GCLOUD_CONFIG,
        "client_id_file": DEFAULT_CLIENT_ID_FILE,
    }
}


def ssl_context():
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read Gmail through Claudia's local gcloud OAuth profiles."
    )
    parser.add_argument("--out", default="")
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--newer-than", default="7d")
    parser.add_argument("--gcloud-config", default="")
    subparsers = parser.add_subparsers(dest="command")

    profile = subparsers.add_parser("profile", help="Show the authenticated mailbox.")
    profile.add_argument("--account", default="ucsd", choices=sorted(ACCOUNTS))

    search = subparsers.add_parser("search", help="Search a mailbox.")
    search.add_argument("query")
    search.add_argument("--account", default="ucsd", choices=sorted(ACCOUNTS))
    search.add_argument("--max-results", type=int, default=None)
    search.add_argument("--full", action="store_true", help="Include decoded text bodies.")

    read = subparsers.add_parser("read", help="Read a message by Gmail message id.")
    read.add_argument("message_id")
    read.add_argument("--account", default="ucsd", choices=sorted(ACCOUNTS))

    dispatch = subparsers.add_parser("dispatch", help="Emit daily-dispatch email JSON.")
    dispatch.add_argument("--max-results", type=int, default=None)
    dispatch.add_argument("--newer-than", default=None)
    dispatch.add_argument(
        "--ucsd-query",
        default="in:inbox is:unread newer_than:{newer_than} -in:spam -in:trash",
    )

    parser.add_argument(
        "--ucsd-query",
        default="in:inbox is:unread newer_than:{newer_than} -in:spam -in:trash",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def clean(value):
    return " ".join(str(value or "").split())


def account_config(account_name, gcloud_override=""):
    account = dict(ACCOUNTS[account_name])
    if gcloud_override:
        account["gcloud_config"] = Path(gcloud_override)
    return account


def run_gcloud_token(config_dir):
    cmd = ["gcloud", "auth", "application-default", "print-access-token"]
    try:
        env = os.environ.copy()
        env["CLOUDSDK_CONFIG"] = config_dir
        completed = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )
    except FileNotFoundError:
        return None, "gcloud is not installed or not on PATH."
    except subprocess.CalledProcessError as exc:
        message = clean(exc.stderr or exc.stdout)
        return None, message or "gcloud could not refresh the Gmail OAuth token."
    return completed.stdout.strip(), ""


def reauth_command(config_dir, client_id_file=DEFAULT_CLIENT_ID_FILE):
    parts = [
        f'CLOUDSDK_CONFIG="{config_dir}"',
        "gcloud auth application-default login",
    ]
    if Path(client_id_file).exists():
        parts.append(f'--client-id-file="{client_id_file}"')
    parts.append(f"--scopes={GCLOUD_PLATFORM_SCOPE},{GMAIL_READONLY_SCOPE}")
    return " ".join(parts)


def gmail_request(token, path, params=None):
    url = f"{GMAIL_API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as response:
        return json.loads(response.read().decode("utf-8"))


def header(headers, name):
    wanted = name.lower()
    for item in headers:
        if item.get("name", "").lower() == wanted:
            return item.get("value", "")
    return ""


def gmail_ts(internal_date):
    if not internal_date:
        return ""
    try:
        stamp = datetime.fromtimestamp(int(internal_date) / 1000, tz=timezone.utc)
    except (TypeError, ValueError):
        return ""
    return stamp.isoformat()


def decode_body(data):
    if not data:
        return ""
    padding = "=" * (-len(data) % 4)
    try:
        return base64.urlsafe_b64decode(data + padding).decode("utf-8", errors="replace")
    except (ValueError, TypeError):
        return ""


def collect_text_parts(part):
    mime_type = part.get("mimeType", "")
    body = part.get("body", {})
    parts = part.get("parts", [])
    if parts:
        texts = []
        for child in parts:
            texts.extend(collect_text_parts(child))
        return texts
    if mime_type == "text/plain":
        text = clean(decode_body(body.get("data", "")))
        return [text] if text else []
    return []


def message_text(message):
    texts = collect_text_parts(message.get("payload", {}))
    if texts:
        return "\n\n".join(texts)
    return clean(message.get("snippet"))


def message_to_item(message, include_body=False):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    subject = clean(header(headers, "Subject") or "(no subject)")
    sender = clean(header(headers, "From"))
    snippet = clean(message.get("snippet"))
    labels = message.get("labelIds", [])
    action = snippet or "Review"
    item = {
        "subject": subject,
        "from": sender,
        "to": clean(header(headers, "To")),
        "date": clean(header(headers, "Date")),
        "action": action,
        "confidence": "api",
        "timestamp": gmail_ts(message.get("internalDate")),
        "labels": labels,
        "message_id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
    }
    if include_body:
        item["body"] = message_text(message)
    return item


def fetch_message(token, message_id, full=False):
    params = {"format": "full" if full else "metadata"}
    if not full:
        params["metadataHeaders"] = ["From", "To", "Subject", "Date"]
    return gmail_request(token, f"/users/me/messages/{message_id}", params)


def collect_messages(token, query, max_results, full=False):
    search = gmail_request(
        token,
        "/users/me/messages",
        {"q": query, "maxResults": max_results},
    )
    messages = []
    for item in search.get("messages", []):
        message = fetch_message(token, item["id"], full=full)
        messages.append(message_to_item(message, include_body=full))
    return messages


def auth_for_account(account_name, gcloud_override=""):
    account = account_config(account_name, gcloud_override)
    config_dir = str(account["gcloud_config"])
    token, error = run_gcloud_token(config_dir)
    return account, config_dir, token, error


def emit_json(result, out=""):
    output = json.dumps(result, indent=2)
    if out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output + "\n", encoding="utf-8")
        print(path)
    else:
        print(output)


def main():
    args = parse_args()
    command = args.command or "dispatch"

    if command in {"profile", "search", "read"}:
        account, config_dir, token, error = auth_for_account(args.account, args.gcloud_config)
        result = {
            "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
            "account": args.account,
            "expected_email": account["email"],
            "diagnostics": [],
        }
        if not token:
            result["diagnostics"].append(f"Gmail blocked: {error}")
            result["reauth_command"] = reauth_command(config_dir, account["client_id_file"])
            emit_json(result, args.out)
            return
        try:
            profile = gmail_request(token, "/users/me/profile")
            result["profile"] = profile
            if command == "search":
                result["query"] = args.query
                max_results = args.max_results if args.max_results is not None else 8
                result["messages"] = collect_messages(token, args.query, max_results, full=args.full)
            elif command == "read":
                message = fetch_message(token, args.message_id, full=True)
                result["message"] = message_to_item(message, include_body=True)
            result["diagnostics"].append(f"Gmail OK: {profile.get('emailAddress', '')}.")
        except Exception as exc:
            result["diagnostics"].append(f"Gmail API failed: {type(exc).__name__}: {exc}")
        emit_json(result, args.out)
        return

    newer_than = args.newer_than or "7d"
    max_results = args.max_results if args.max_results is not None else 8
    query = args.ucsd_query.format(newer_than=newer_than)
    account, config_dir, token, error = auth_for_account("ucsd", args.gcloud_config)
    result = {
        "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
        "ucsd_query": query,
        "ucsd": [],
        "personal": [],
        "diagnostics": [],
    }

    if token:
        try:
            profile = gmail_request(token, "/users/me/profile")
            result["ucsd_profile"] = profile.get("emailAddress", "")
            result["ucsd"] = collect_messages(token, query, max_results)
            result["diagnostics"].append(
                f"UCSD Gmail OK: {result['ucsd_profile']} ({len(result['ucsd'])} matching unread inbox messages)."
            )
        except Exception as exc:
            result["diagnostics"].append(f"UCSD Gmail API failed: {type(exc).__name__}: {exc}")
    else:
        result["ucsd"].append(
            {
                "subject": "UCSD Gmail re-auth needed",
                "action": f"Run: {reauth_command(config_dir, account['client_id_file'])}",
                "confidence": "blocked",
            }
        )
        result["diagnostics"].append(f"UCSD Gmail blocked: {error}")

    result["personal"].append(
        {
            "subject": "Personal Gmail connector is not script-accessible",
            "action": "Supply personal Gmail results from the Codex Gmail connector as --email-json when available.",
            "confidence": "connector-only",
        }
    )

    emit_json(result, args.out)


if __name__ == "__main__":
    main()
