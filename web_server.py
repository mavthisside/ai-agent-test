from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path

from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.agent.agent import Agent


# ---------------------------------------------------------
# Load the existing agent exactly the same way as test_agent.py
# ---------------------------------------------------------

documents = load_knowledge_base("knowledge-base")
chunks = chunk_documents(documents)
agent = Agent(chunks)


# ---------------------------------------------------------
# Web server
# ---------------------------------------------------------

class ChatHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(body)

    def _send_html(self):
        html_path = Path(__file__).parent / "web" / "index.html"

        try:
            html = html_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.send_error(500, "web/index.html not found")
            return

        body = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send_html()
            return

        self.send_error(404)

    def do_POST(self):
        if self.path != "/chat":
            self.send_error(404)
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode("utf-8"))

            message = data.get("message", "").strip()

            if not message:
                self._send_json(
                    {"error": "Message cannot be empty."},
                    status=400,
                )
                return

            response = agent.handle_message(message)

            self._send_json(
                {
                    "response": response,
                    "trace": agent.last_trace,
                }
            )

        except Exception as exc:
            self._send_json(
                {
                    "error": str(exc)
                },
                status=500,
            )

    def log_message(self, format, *args):
        print(f"[WEB] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(
        ("127.0.0.1", 8000),
        ChatHandler,
    )

    print()
    print("=" * 60)
    print("Aster & Row AI Support Agent")
    print("=" * 60)
    print("Open: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    print("=" * 60)
    print()

    server.serve_forever()