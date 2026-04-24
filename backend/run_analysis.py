import argparse
import json
import os
import urllib.request


def send_resume(file_path: str, api_url: str):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = [
        f"--{boundary}",
        'Content-Disposition: form-data; name="file"; filename="resume.pdf"',
        "Content-Type: application/pdf",
        "",
    ]
    body_bytes = "\r\n".join(body).encode("utf-8") + b"\r\n" + file_data + b"\r\n" + f"--{boundary}--\r\n".encode("utf-8")

    request = urllib.request.Request(api_url, data=body_bytes, headers=headers)
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.status, response.read().decode("utf-8", "replace")


def main():
    parser = argparse.ArgumentParser(description="Run a resume analyze request against the Flask backend.")
    parser.add_argument("--file", default="../ML-EXPERIMENT-3.pdf", help="Path to the resume PDF file")
    parser.add_argument("--url", default="http://127.0.0.1:5000/api/analyze", help="Analyze endpoint URL")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"Resume file not found: {args.file}")

    status, payload = send_resume(args.file, args.url)
    print(f"STATUS {status}")
    try:
        data = json.loads(payload)
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print(payload)


if __name__ == "__main__":
    main()
