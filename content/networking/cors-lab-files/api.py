# CORS lab API on localhost:9000. Python 3 standard library only.
import json
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # turn off the default access log so only our own line prints

    def reply(self, status, body, headers=()):
        data = json.dumps(body).encode()  # the JSON body as bytes
        self.send_response(status)
        self.send_header("Content-Type", "application/json")  # tells the browser the body is JSON
        self.send_header("Content-Length", str(len(data)))  # exact body size in bytes
        for name, value in headers:
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        origin = self.headers.get("Origin", "-")  # '-' when the request has no Origin header
        print(f"GET {self.path} Origin={origin}", flush=True)  # the one line we print per request

        if self.path == "/api/open":
            self.reply(200, {"route": "open"})  # no CORS headers: the browser hides this response from the page

        elif self.path == "/api/allow":
            self.reply(200, {"route": "allow"}, [
                ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
            ])

        elif self.path == "/api/allow-creds":
            self.reply(200, {"route": "allow-creds"}, [
                ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
                ("Access-Control-Allow-Credentials", "true"),  # lets the browser send and accept cookies
            ])

        elif self.path == "/api/wildcard-creds":
            # Deliberately wrong: browsers block '*' when credentials are used.
            self.reply(200, {"route": "wildcard-creds"}, [
                ("Access-Control-Allow-Origin", "*"),  # any origin may read it, but not with credentials
                ("Access-Control-Allow-Credentials", "true"),  # asks for credentials, which the '*' breaks
            ])

        elif self.path == "/api/login":
            self.reply(200, {"logged_in": True}, [
                ("Set-Cookie", "session=demo123; Path=/; SameSite=Lax"),  # the browser stores this cookie
                ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
                ("Access-Control-Allow-Credentials", "true"),  # lets the browser keep the cookie from this call
            ])

        elif self.path == "/api/me":
            jar = SimpleCookie(self.headers.get("Cookie", ""))  # parse the Cookie request header
            session = jar["session"].value if "session" in jar else None  # the demo cookie, or None
            self.reply(200, {"cookie_seen": session is not None, "cookie": session}, [
                ("Access-Control-Allow-Origin", "http://localhost:8000"),  # only this page origin may read the response
                ("Access-Control-Allow-Credentials", "true"),  # lets the browser send the cookie and read this
            ])

        else:
            self.reply(404, {"error": "not found"})  # unknown path: no CORS headers


if __name__ == "__main__":
    HTTPServer(("localhost", 9000), Handler).serve_forever()  # serve until stopped
