#!/usr/bin/env python3
"""Xero API helper for updates (POST/PUT)"""

import json
import urllib.request
import urllib.error
from xero_api import load_tokens, refresh_access_token, get_tenant_id, save_tokens

def api_post(endpoint, data, method='POST', tenant_id=None):
    """POST or PUT to Xero API"""
    tokens = load_tokens()
    if not tenant_id:
        tenant_id, _ = get_tenant_id()
    
    url = f"https://api.xero.com/api.xro/2.0/{endpoint}"
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=json_data, method=method, headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            # Token expired, refresh and retry
            tokens = refresh_access_token()
            req = urllib.request.Request(url, data=json_data, method=method, headers={
                'Authorization': f'Bearer {tokens["access_token"]}',
                'Xero-Tenant-Id': tenant_id,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read().decode())
        else:
            # Read error body
            error_body = e.read().decode() if e.fp else 'No error body'
            raise Exception(f"HTTP {e.code}: {error_body}")

def api_put(endpoint, data, tenant_id=None):
    """PUT to Xero API"""
    return api_post(endpoint, data, method='PUT', tenant_id=tenant_id)
