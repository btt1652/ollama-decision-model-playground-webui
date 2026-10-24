#!/usr/bin/env python3
"""Hot-reload dev server for the Decision Model Playground.

Watches project files for changes and prints a notification so you
can refresh the browser.  No external dependencies — uses only the
Python standard library.

Usage:
    python3 serve.py          # serves on http://localhost:8080
    python3 serve.py -p 3000  # custom port
"""

import http.server
import os
import sys
import threading
import time

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_file_mtimes(directory):
    """Return a dict of {filepath: mtime} for all files in directory."""
    mtimes = {}
    for root, _dirs, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            try:
                mtimes[path] = os.stat(path).st_mtime
            except OSError:
                pass
    return mtimes


def watch_for_changes(directory, interval=1.0):
    """Poll for file changes and print a notification."""
    mtimes = get_file_mtimes(directory)
    while True:
        time.sleep(interval)
        new_mtimes = get_file_mtimes(directory)
        changed = []
        for path, mtime in new_mtimes.items():
            if path not in mtimes or mtimes[path] != mtime:
                changed.append(os.path.relpath(path, directory))
        for path in mtimes:
            if path not in new_mtimes:
                changed.append(os.path.relpath(path, directory) + " (deleted)")
        if changed:
            # Bell character to get terminal attention
            sys.stdout.write("\a")
            sys.stdout.flush()
            print(f"\n[hot-reload] Changed: {', '.join(changed)}")
            print("  → Refresh your browser to see changes.\n")
        mtimes = new_mtimes


def main():
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    if "-p" in sys.argv:
        try:
            idx = sys.argv.index("-p")
            port = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            pass

    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = DIRECTORY

    # Start file watcher in a daemon thread
    watcher = threading.Thread(
        target=watch_for_changes,
        args=(DIRECTORY,),
        daemon=True,
    )
    watcher.start()

    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    print(f"Serving http://localhost:{port}/  (directory: {DIRECTORY})")
    print("Watching for file changes… (Ctrl+C to stop)\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
