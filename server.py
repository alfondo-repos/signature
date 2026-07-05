#!/usr/bin/env python3
"""Servidor de desarrollo: regenera firmas al editar team.json y preview en vivo."""
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from generate import TEAM_FILE, generate

PORT = 8765
ROOT = Path(__file__).parent
GENERATE_FILE = ROOT / "generate.py"

VERSION = {"token": "init"}


def bump_version():
    team_mtime = TEAM_FILE.stat().st_mtime if TEAM_FILE.exists() else 0
    gen_mtime = GENERATE_FILE.stat().st_mtime if GENERATE_FILE.exists() else 0
    VERSION["token"] = f"{team_mtime}-{gen_mtime}-{time.time():.3f}"


def watch_and_generate():
    last_team_mtime = None
    last_gen_mtime = None

    while True:
        try:
            team_mtime = TEAM_FILE.stat().st_mtime if TEAM_FILE.exists() else 0
            gen_mtime = GENERATE_FILE.stat().st_mtime if GENERATE_FILE.exists() else 0

            if team_mtime != last_team_mtime or gen_mtime != last_gen_mtime:
                count = generate(verbose=False)
                bump_version()
                print(f"↻ {count} firmas actualizadas")
                last_team_mtime = team_mtime
                last_gen_mtime = gen_mtime
        except Exception as exc:
            print(f"⚠ Error al regenerar: {exc}")

        time.sleep(0.4)


class DevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] == "/__dev/version":
            payload = json.dumps(VERSION).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        if "/__dev/version" in (args[0] if args else ""):
            return
        super().log_message(format, *args)


def main():
    generate(verbose=True)
    bump_version()

    watcher = threading.Thread(target=watch_and_generate, daemon=True)
    watcher.start()

    with ThreadingHTTPServer(("", PORT), DevHandler) as httpd:
        print(f"\nPreview en vivo → http://localhost:{PORT}/index.html")
        print("Edita team.json y guarda — se actualiza solo en ~1s.")
        print("Ctrl+C para detener.\n")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
