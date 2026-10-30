# Serves this folder on localhost:8000 so the lab page has a real origin.
import functools
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))  # the folder that holds this file


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # hide the per-request access log so there is no extra output


if __name__ == "__main__":
    handler = functools.partial(QuietHandler, directory=HERE)  # serve files from this folder
    ThreadingHTTPServer(("localhost", 8000), handler).serve_forever()  # bind to localhost only
