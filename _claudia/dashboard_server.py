#!/usr/bin/env python3
"""
Local live server for the Claudia dashboard.

Usage:
    python3 _claudia/dashboard_server.py
"""

import json
import queue
import select
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from dashboard import DB_PATH, OUTPUT_PATH, generate_dashboard, get_dashboard_payload

HOST = "127.0.0.1"
PORT = 8765
WATCH_PATHS = [DB_PATH, DB_PATH.with_name(DB_PATH.name + "-wal"), DB_PATH.with_name(DB_PATH.name + "-shm")]
DEBOUNCE_SECONDS = 0.6
SLOW_CHECK_SECONDS = 20.0


class DashboardState:
    def __init__(self):
        self.lock = threading.Lock()
        self.clients = set()
        self.version = 0
        self.last_change = time.time()
        self.last_error = None
        self.last_event = "startup"
        self.file_signatures = self.signatures()

    def signatures(self):
        signatures = {}
        for path in WATCH_PATHS:
            try:
                st = path.stat()
                signatures[str(path)] = (st.st_mtime_ns, st.st_size)
            except FileNotFoundError:
                signatures[str(path)] = None
        return signatures

    def changed(self):
        latest = self.signatures()
        changed = latest != self.file_signatures
        if changed:
            self.file_signatures = latest
        return changed

    def add_client(self):
        client_queue = queue.Queue(maxsize=8)
        with self.lock:
            self.clients.add(client_queue)
            version = self.version
        client_queue.put({"type": "hello", "version": version})
        return client_queue

    def remove_client(self, client_queue):
        with self.lock:
            self.clients.discard(client_queue)

    def broadcast(self, payload):
        with self.lock:
            clients = list(self.clients)
        for client_queue in clients:
            try:
                client_queue.put_nowait(payload)
            except queue.Full:
                self.remove_client(client_queue)

    def refresh_dashboard(self, source, force=False):
        with self.lock:
            now = time.time()
            if now - self.last_change < DEBOUNCE_SECONDS:
                return False
            self.last_change = now
        time.sleep(DEBOUNCE_SECONDS)
        if not force and not self.changed() and source != "startup":
            return False
        try:
            generate_dashboard()
            payload = get_dashboard_payload()
            with self.lock:
                self.version += 1
                payload["version"] = self.version
                payload["event_source"] = source
                self.last_error = None
                self.last_event = source
            self.broadcast({"type": "dashboard-change", "payload": payload})
            return True
        except Exception as exc:
            with self.lock:
                self.last_error = str(exc)
            self.broadcast({"type": "dashboard-error", "payload": {"error": str(exc)}})
            return False


STATE = DashboardState()


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "ClaudiaDashboard/1.0"

    def log_message(self, fmt, *args):
        return

    def send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/dashboard.html"):
            self.serve_dashboard()
        elif path == "/api/dashboard":
            self.send_json(get_dashboard_payload())
        elif path == "/api/health":
            self.send_json(self.health_payload())
        elif path == "/events":
            self.serve_events()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def serve_dashboard(self):
        if not OUTPUT_PATH.exists():
            generate_dashboard()
        body = OUTPUT_PATH.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def health_payload(self):
        with STATE.lock:
            return {
                "ok": STATE.last_error is None,
                "host": HOST,
                "port": PORT,
                "version": STATE.version,
                "last_event": STATE.last_event,
                "last_error": STATE.last_error,
                "watched_paths": [str(path) for path in WATCH_PATHS],
            }

    def serve_events(self):
        client_queue = STATE.add_client()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        try:
            while True:
                try:
                    message = client_queue.get(timeout=15)
                    event_type = message["type"]
                    payload = json.dumps(message.get("payload", {}))
                    self.wfile.write(f"event: {event_type}\n".encode("utf-8"))
                    self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                except queue.Empty:
                    self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            pass
        finally:
            STATE.remove_client(client_queue)


def watched_file_descriptors():
    descriptors = []
    for path in WATCH_PATHS:
        try:
            descriptors.append(path.open("rb"))
        except FileNotFoundError:
            continue
    return descriptors


def watch_with_kqueue(stop_event):
    if not hasattr(select, "kqueue"):
        return False
    descriptors = watched_file_descriptors()
    if not descriptors:
        return False
    kq = select.kqueue()
    flags = select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR
    fflags = select.KQ_NOTE_WRITE | select.KQ_NOTE_EXTEND | select.KQ_NOTE_ATTRIB | select.KQ_NOTE_RENAME | select.KQ_NOTE_DELETE
    try:
        changes = [select.kevent(fd.fileno(), filter=select.KQ_FILTER_VNODE, flags=flags, fflags=fflags) for fd in descriptors]
        kq.control(changes, 0, 0)
        while not stop_event.is_set():
            events = kq.control(None, 8, SLOW_CHECK_SECONDS)
            if events:
                STATE.refresh_dashboard("filesystem", force=True)
                return True
            if STATE.changed():
                STATE.refresh_dashboard("slow-check", force=True)
    finally:
        kq.close()
        for fd in descriptors:
            fd.close()
    return True


def watch_loop(stop_event):
    while not stop_event.is_set():
        handled = watch_with_kqueue(stop_event)
        if not handled:
            time.sleep(SLOW_CHECK_SECONDS)
            if STATE.changed():
                STATE.refresh_dashboard("slow-check", force=True)


def main():
    generate_dashboard()
    stop_event = threading.Event()
    watcher = threading.Thread(target=watch_loop, args=(stop_event,), daemon=True)
    watcher.start()
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"Claudia dashboard server: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        server.server_close()


if __name__ == "__main__":
    main()
