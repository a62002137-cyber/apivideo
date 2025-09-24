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
            html = f'''
            <h1>🔥 WORKING VIRAL CLIP API</h1>
            <h2>✅ Server Status: ONLINE</h2>
            
            <h3>🔑 Admin API Key:</h3>
            <code>{admin_key}</code>
            
            <h3>🧪 Test Commands:</h3>
            <pre>
# Test 1: Login
curl -X POST http://localhost:5000/api/login \\
  -H "Content-Type: application/json" \\
  -d '{{"username":"admin","password":"admin123"}}'

# Test 2: Generate (use API key from login)
curl -X POST http://localhost:5000/api/generate \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: {admin_key}" \\
  -d '{{"video_url":"https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"}}'
            </pre>
            
            <p><strong>Total Users:</strong> {len(users)}</p>
            <p><strong>Total Jobs:</strong> {len(jobs)}</p>
            <p><strong>Server Time:</strong> {datetime.now()}</p>
            '''
            
            self.wfile.write(html.encode())
            
        elif self.path.startswith('/api/download/'):
            filename = self.path.split('/')[-1]
            filepath = f'results/{filename}'
            
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename={filename}')
                self.end_headers()
                
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'File not found'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/login':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                username = data.get('username')
                password = data.get('password')
                
                if username in users and users[username]['password'] == password:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    
                    response = {
                        'success': True,
                        'api_key': users[username]['api_key'],
                        'message': f'Login successful! Welcome {username}',
                        'subscription': 'unlimited',
                        'is_admin': True
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid credentials'}).encode())
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                
        elif self.path == '/api/generate':
            try:
                # Check API key
                api_key = self.headers.get('X-API-Key')
                valid_user = None
                
                for username, user_data in users.items():
                    if user_data['api_key'] == api_key:
                        valid_user = username
                        break
                
                if not valid_user:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid API key'}).encode())
                    return
                
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                video_url = data.get('video_url')
                settings = data.get('settings', {})
                
                if not video_url:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'video_url required'}).encode())
                    return
                
                # Create job
                job_id = str(uuid.uuid4())
                
                print(f"🎬 Creating job {job_id} for video: {video_url}")
                
                # Simulate processing (create demo files)
                clips_info = []
                for i in range(1, 4):  # Create 3 demo clips
                    clip_name = f'viral_clip_{job_id}_{i:03d}.txt'
                    clip_path = f'results/{clip_name}'
                    
                    # Create demo file
                    with open(clip_path, 'w') as f:
                        f.write(f'''
VIRAL CLIP #{i}
==============
Job ID: {job_id}
Original Video: {video_url}
Created: {datetime.now()}
Settings: {json.dumps(settings, indent=2)}

This is a demo clip. In production, this would be an actual video file.
                        ''')
                    
                    file_size = os.path.getsize(clip_path)
                    
                    clips_info.append({
                        'clip_number': i,
                        'filename': clip_name,
                        'file_size_mb': round(file_size / (1024*1024), 3),
                        'duration': 30 + i * 10,  # Demo duration
                        'download_url': f'/api/download/{clip_name}',
                        'status': 'completed'
                    })
                
                # Save job
                jobs[job_id] = {
                    'user': valid_user,
                    'video_url': video_url,
                    'settings': settings,
                    'status': 'completed',
                    'created_at': datetime.now().isoformat(),
                    'clips': clips_info
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    'success': True,
                    'job_id': job_id,
                    'status': 'completed',
                    'message': f'Generated {len(clips_info)} viral clips!',
                    'clips_generated': len(clips_info),
                    'clips': clips_info,
                    'processing_time': '2.5 seconds (demo mode)'
                }
                self.wfile.write(json.dumps(response).encode())
                
                print(f"✅ Job {job_id} completed: {len(clips_info)} clips created")
                
            except Exception as e:
                print(f"❌ Generate error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(('0.0.0.0', 5000), APIHandler)
    
    print("\n🚀 SIMPLE VIRAL CLIP API")
    print("=" * 40)
    print("🌐 Server: http://localhost:5000")
    print(f"🔑 Admin API Key: {users['admin']['api_key']}")
    print("👤 Admin: admin / admin123")
    print("🎬 Mode: Demo (creates text files)")
    print("=" * 40)
    print("✅ Server starting...\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped")
        server.server_close()

if __name__ == '__main__':
    run_server()
