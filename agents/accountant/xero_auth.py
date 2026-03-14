#!/usr/bin/env python3
"""Xero OAuth2 Authorization Flow - One-time setup"""

import http.server
import urllib.parse
import urllib.request
import json
import base64
import sys
import os
import webbrowser
import threading

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'xero_credentials.json')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'config', 'xero_tokens.json')

with open(CONFIG_PATH) as f:
    config = json.load(f)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']
SCOPES = config['scopes']

PORT = 18790

# Build authorization URL
auth_url = (
    f"https://login.xero.com/identity/connect/authorize"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&state=openclaw_auth"
)

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if '/xero/callback' in self.path:
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params:
                code = params['code'][0]
                print(f"\n✅ Authorization code received!")
                
                # Exchange code for tokens
                token_url = "https://identity.xero.com/connect/token"
                
                auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
                
                data = urllib.parse.urlencode({
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                }).encode()
                
                req = urllib.request.Request(token_url, data=data, headers={
                    'Authorization': f'Basic {auth_header}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                })
                
                try:
                    resp = urllib.request.urlopen(req)
                    tokens = json.loads(resp.read().decode())
                    
                    # Save tokens
                    with open(TOKEN_PATH, 'w') as f:
                        json.dump(tokens, f, indent=2)
                    
                    print(f"✅ Tokens saved to {TOKEN_PATH}")
                    print(f"   Access token expires in: {tokens.get('expires_in', '?')} seconds")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"""
                    <html><body style="font-family:sans-serif;text-align:center;padding:60px;">
                    <h1>Connected to Xero!</h1>
                    <p>You can close this tab and go back to OpenClaw.</p>
                    </body></html>
                    """)
                    
                    # Shutdown after success
                    threading.Thread(target=self.server.shutdown).start()
                    
                except Exception as e:
                    print(f"❌ Token exchange failed: {e}")
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<html><body><h1>Error</h1><p>{e}</p></body></html>".encode())
            else:
                error = params.get('error', ['unknown'])[0]
                print(f"❌ Authorization denied: {error}")
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"<html><body><h1>Authorization denied</h1><p>{error}</p></body></html>".encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

if __name__ == '__main__':
    print(f"🔗 Opening Xero authorization in your browser...")
    print(f"   URL: {auth_url[:80]}...")
    print(f"\n⏳ Waiting for callback on port {PORT}...")
    
    # Open browser
    webbrowser.open(auth_url)
    
    # Start callback server
    server = http.server.HTTPServer(('localhost', PORT), CallbackHandler)
    server.serve_forever()
    print("\n✅ Done! Xero is connected.")
