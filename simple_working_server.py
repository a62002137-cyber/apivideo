from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
import uuid
import urllib.request
from datetime import datetime

# Simple data storage
users = {
    'admin': {
        'password': 'admin123',
        'api_key': str(uuid.uuid4())
    }
}

jobs = {}
clips = {}

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            admin_key = users['admin']['api_key']
            html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral Clip API</title>
    <style>
        body {{background: #181818; color: #fff; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0;}}
        .container {{max-width: 600px; margin: 40px auto; background: #23272f; border-radius: 12px; box-shadow: 0 4px 24px #0008; padding: 32px 28px 18px 28px;}}
        h1 {{color: #ffb347; margin-bottom: 0.2em;}}
        h2 {{color: #7fff7f; margin-top: 0;}}
        code, pre {{background: #111; color: #ffb347; border-radius: 6px; padding: 2px 6px;}}
        .footer {{margin-top: 2em; font-size: 0.95em; color: #aaa; text-align: center;}}
        a {{ color: #ffb347; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 WORKING VIRAL CLIP API</h1>
        <h2>✅ Server Status: ONLINE</h2>
        <h3>🔑 Admin API Key:</h3>
        <code>{admin_key}</code>
        <h3>🧪 Test Commands:</h3>
        <pre># Test 1: Login
curl -X POST http://localhost:8000/login -d '{{"username": "admin", "password": "admin123"}}' -H "Content-Type: application/json"

# Test 2: Get API Key
curl http://localhost:8000/apikey?user=admin

# Test 3: Create Job
curl -X POST http://localhost:8000/job -d '{{"video_url": "https://example.com/video.mp4", "settings": {{}}}}' -H "x-api-key: {admin_key}" -H "Content-Type: application/json"
        </pre>
        <p><strong>Server Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="footer">
            &copy; {datetime.now().year} Viral Clip API &mdash; <a href="https://apivideo.com">apivideo.com</a>
        </div>
    </div>
</body>
</html>
            '''
            self.wfile.write(html.encode())
        else:
            self.send_error(404, "Not Found")
