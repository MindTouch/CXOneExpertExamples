#!/usr/bin/env python3

import requests
import time
import sys
import json
from pprint import pprint

def get_unique_webhook_url():
    """
    Get a unique webhook URL from webhook.site (free service)
    Returns the unique URL that can receive webhook payloads
    """
    print("Generating unique webhook URL...")
    
    try:
        response = requests.post('https://webhook.site/token', timeout=10)
        response.raise_for_status()
        
        data = response.json()
        webhook_uuid = data['uuid']
        webhook_url = f"https://webhook.site/{webhook_uuid}"
        
        print(f"Webhook URL created: {webhook_url}")
        print(f"   View requests at: https://webhook.site/#!/{webhook_uuid}")
        return webhook_url
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating webhook URL: {e}")
        sys.exit(1)

def authenticate_with_expert(base_url):
    """
    Authenticate with the target system and save cookies for subsequent requests
    
    Args:
        base_url: Base URL of the target site (e.g., 'https://example.com')
    """
    print("Authenticating with target system...")
    
    auth_url = f"{base_url}/@api/deki/users/authenticate"
    auth_credentials = ("REDACTED", "REDACTED")

    try:
        auth_response = requests.get(auth_url, auth=auth_credentials, timeout=10)
        auth_response.raise_for_status()
        auth_cookies = auth_response.cookies

        with open('cookies.txt', 'w') as cookies_file:
            for cookie in auth_cookies:
                cookies_file.write(f"{cookie.name}={cookie.value}; ")
        
        print("Authentication successful - cookies saved to cookies.txt")
        
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        if e.response and hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        sys.exit(1)

def create_webhook(base_url, webhook_url, bearer_authorization_header):
    """
    Create a webhook in the target system
    
    Args:
        base_url: Base URL of the target site (e.g., 'https://example.com')
        webhook_url: The unique webhook URL to receive events
        bearer_authorization_header: The Bearer token for authorization in the webhook
    
    Returns:
        The webhook ID from the response
    """
    print(f"\nCreating webhook at {base_url}...")
    
    cookies = {}
    try:
        with open('cookies.txt', 'r') as cookies_file:
            cookie_string = cookies_file.read().strip()
            if cookie_string:
                for cookie in cookie_string.split('; '):
                    if '=' in cookie:
                        name, value = cookie.split('=', 1)
                        cookies[name] = value
    except FileNotFoundError:
        print("Error: cookies.txt not found. Please authenticate first.")
        sys.exit(1)
    
    xml_body = f"""<webhook>
    <webhook-url>{webhook_url}</webhook-url>
    <authorization-header>Bearer {bearer_authorization_header}</authorization-header>
</webhook>"""

    api_url = f"{base_url}/@api/deki/webhooks"
    
    headers = {
        'Content-Type': 'application/xml'
    }
    
    import xml.etree.ElementTree as ET
    
    try:
        response = requests.post(api_url, data=xml_body, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        
        response_text = response.text
        print(f"Webhook created successfully!")
        
        root = ET.fromstring(response_text)
        
        webhook_id = None
        id_element = root.find('.//id')
        if id_element is not None:
            webhook_id = id_element.text
        
        print(f"   Webhook ID: {webhook_id}")
        
        return webhook_id
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating webhook: {e}")
        if e.response and hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        sys.exit(1)

def add_page_create_event(base_url, webhook_id):
    """
    Add a page_create event to the webhook
    
    Args:
        base_url: Base URL of the target site
        webhook_id: The ID of the webhook to configure
    """
    print(f"\nAdding page_create event to webhook {webhook_id}...")
    
    cookies = {}
    try:
        with open('cookies.txt', 'r') as cookies_file:
            cookie_string = cookies_file.read().strip()
            if cookie_string:
                for cookie in cookie_string.split('; '):
                    if '=' in cookie:
                        name, value = cookie.split('=', 1)
                        cookies[name] = value
    except FileNotFoundError:
        print("Error: cookies.txt not found. Please authenticate first.")
        sys.exit(1)
    
    api_url = f"{base_url}/@api/deki/webhooks/{webhook_id}/events/page_create"
    
    headers = {
        'Content-Type': 'application/xml'
    }
    
    try:
        response = requests.put(api_url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        
        print(f"page_create event added successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error adding event: {e}")
        if e.response and hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        sys.exit(1)

def listen_to_webhook(webhook_uuid, poll_interval=2):
    """
    Listen for incoming webhook requests in real-time
    
    Args:
        webhook_uuid: The UUID from webhook.site
        poll_interval: How often to check for new requests (seconds)
    """
    print("\n" + "=" * 60)
    print("Webhook Listener Active")
    print("=" * 60)
    print(f"Listening for incoming requests...")
    print(f"Press Ctrl+C to stop listening\n")
    
    seen_request_ids = set()
    api_url = f"https://webhook.site/token/{webhook_uuid}/requests"
    
    try:
        while True:
            try:
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                
                requests_data = response.json()
                
                if requests_data.get('data'):
                    for req in reversed(requests_data['data']):
                        req_id = req.get('uuid')
                        
                        if req_id and req_id not in seen_request_ids:
                            seen_request_ids.add(req_id)
                            
                            timestamp = req.get('created_at', 'Unknown time')
                            method = req.get('method', 'Unknown')
                            content = req.get('content', '')
                            headers = req.get('headers', {})
                            
                            print("=" * 60)
                            print(f"New Request Received!")
                            print(f"   Time: {timestamp}")
                            print(f"   Method: {method}")
                            print(f"   Request ID: {req_id}")
                            
                            if content:
                                print(f"\n   Body:")
                                try:
                                    import json
                                    parsed = json.loads(content)
                                    print(f"     {json.dumps(parsed, indent=6)}")
                                except:
                                    if len(content) > 500:
                                        print(f"     {content[:500]}...")
                                        print(f"     (truncated, full length: {len(content)} chars)")
                                    else:
                                        print(f"     {content}")
                            else:
                                print(f"\n   Body: (empty)")
                            
                            print("=" * 60 + "\n")
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching requests: {e}")
            
            time.sleep(poll_interval)
            
    except KeyboardInterrupt:
        print("\n\nStopped listening to webhook")

def main():
    """Main execution function"""
    print("=" * 60)
    print("Webhook Setup Script")
    print("=" * 60)
    
    base_url = input("\nEnter the base URL of your target site (e.g., https://example.com): ").strip()
    
    if not base_url:
        print("Base URL is required")
        sys.exit(1)

    bearer_authorization_header = input("\nEnter the Bearer authorization token for your webhook (e.g., imp_xxxxx): ").strip()
    
    if not bearer_authorization_header:
        print("Bearer authorization token for your webhook is required")
        sys.exit(1)
    
    base_url = base_url.rstrip('/')
    
    webhook_url = get_unique_webhook_url()
    webhook_uuid = webhook_url.split('/')[-1]
    
    time.sleep(1)

    authenticate_with_expert(base_url)
    
    webhook_id = create_webhook(base_url, webhook_url, bearer_authorization_header)
    
    add_page_create_event(base_url, webhook_id)
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"Webhook URL: {webhook_url}")
    print(f"Webhook ID: {webhook_id}")
    print(f"\nYour webhook is now configured to receive page_create events.")
    print(f"View incoming requests at: https://webhook.site/#!/{webhook_uuid}")
    
    print("\n" + "-" * 60)
    listen = input("Do you want to listen for incoming webhook requests? (y/n): ").strip().lower()
    
    if listen in ['y', 'yes']:
        listen_to_webhook(webhook_uuid)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
