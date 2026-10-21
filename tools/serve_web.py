"""Local preview with byte ranges, which Safari needs for MP4 streaming."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import re


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range = None
        path = Path(self.translate_path(self.path))
        header = self.headers.get("Range")
        if not header or not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", header)
        if not match or not any(match.groups()):
            self.send_error(416)
            return None
        start, end = match.groups()
        first = int(start) if start else max(0, size - int(end))
        last = min(int(end), size - 1) if start and end else size - 1
        if first > last or first >= size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None
        stream = path.open("rb")
        stream.seek(first)
        self.byte_range = (first, last)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {first}-{last}/{size}")
        self.send_header("Content-Length", str(last - first + 1))
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        if self.byte_range is None:
            return super().copyfile(source, outputfile)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        while remaining > 0:
            chunk = source.read(min(65536, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8043)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "dist/web"
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(root)))
    print(f"Local preview: http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()
