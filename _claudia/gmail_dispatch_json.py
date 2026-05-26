#!/usr/bin/env python3
"""
Collect Gmail items for the Obsidian daily dispatch.

This local helper can read the UCSD mailbox through the separate gcloud OAuth
profile at ~/.config/claudia/gmail-second/. The personal Gmail connector lives
inside Codex, so it must still be supplied as JSON by the orchestrator when
available.
"""

import argparse
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


def ssl_context():
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="")
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--newer-than", default="7d")
    parser.add_argument(
        "--ucsd-query",
        default="in:inbox is:unread newer_than:{newer_than} -in:spam -in:trash",
    )
    parser.add_argument("--gcloud-config", default=str(DEFAULT_GCLOUD_CONFIG))
    return parser.parse_args()


def clean(value):
    return " ".join(str(value or "").split())


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


def reauth_command(config_dir):
    parts = [
        f'CLOUDSDK_CONFIG="{config_dir}"',
        "gcloud auth application-default login",
    ]
    if DEFAULT_CLIENT_ID_FILE.exists():
        parts.append(f'--client-id-file="{DEFAULT_CLIENT_ID_FILE}"')
    parts.append(f"--scopes={GCLOUD_PLATFORM_SCOPE},{GMAIL_READONLY_SCOPE}")
    return " ".join(parts)


def gmail_request(token, path, params=None):
    url = f"{GMAIL_API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
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


def message_to_item(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    subject = clean(header(headers, "Subject") or "(no subject)")
    sender = clean(header(headers, "From"))
    snippet = clean(message.get("snippet"))
    labels = message.get("labelIds", [])
    action = snippet or "Review"
    return {
        "subject": subject,
        "from": sender,
        "action": action,
        "confidence": "api",
        "timestamp": gmail_ts(message.get("internalDate")),
        "labels": labels,
        "message_id": message.get("id", ""),
    }


def collect_ucsd(token, query, max_results):
    search = gmail_request(
        token,
        "/users/me/messages",
        {"q": query, "maxResults": max_results},
    )
    messages = []
    for item in search.get("messages", []):
        message = gmail_request(
            token,
            f"/users/me/messages/{item['id']}",
            {"format": "metadata", "metadataHeaders": ["From", "Subject", "Date"]},
        )
        messages.append(message_to_item(message))
    return messages


def main():
    args = parse_args()
    query = args.ucsd_query.format(newer_than=args.newer_than)
    token, error = run_gcloud_token(args.gcloud_config)
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
            result["ucsd"] = collect_ucsd(token, query, args.max_results)
            result["diagnostics"].append(
                f"UCSD Gmail OK: {result['ucsd_profile']} ({len(result['ucsd'])} matching unread inbox messages)."
            )
        except Exception as exc:
            result["diagnostics"].append(f"UCSD Gmail API failed: {type(exc).__name__}: {exc}")
    else:
        result["ucsd"].append(
            {
                "subject": "UCSD Gmail re-auth needed",
                "action": f"Run: {reauth_command(args.gcloud_config)}",
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

    output = json.dumps(result, indent=2)
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output + "\n", encoding="utf-8")
        print(path)
    else:
        print(output)


if __name__ == "__main__":
    main()
