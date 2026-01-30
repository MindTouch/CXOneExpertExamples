# Webhook Setup Script

This Python script automates the setup of webhooks using a free unique URL service with CXOne Expert.

## Features

1. **Generates a unique webhook URL** using webhook.site (free service, no registration required)
2. **Authenticates with the target site** using cookie-based authentication
3. **Creates a webhook** via the target site's API at `@api/deki/webhooks`
4. **Adds a page_create event** to the webhook using PUT request

## Requirements

```bash
pip install requests
```

## Usage

1. Make the script executable (optional):
   ```bash
   chmod +x webhook_setup.py
   ```

2. Run the script:
   ```bash
   python webhook_setup.py
   ```

3. Enter your target site's base URL when prompted (e.g., `https://example.com`)

## What the Script Does

### Step 1: Generate Unique Webhook URL
The script uses webhook.site to create a free, unique URL that can receive webhook payloads. This URL is temporary but perfect for testing.

### Step 2: Authenticate with Site
The script authenticates with the target site using basic authentication credentials and saves the session cookies to `cookies.txt` for subsequent requests.

### Step 3: Create Webhook
Makes a POST request to `{base_url}/@api/deki/webhooks` with XML body:
```xml
<webhook>
    <webhook-url>{unique-url}</webhook-url>
    <authorization-header>Bearer imp_1754952744_ce363a4d138b88ff815a8d3e32924cd</authorization-header>
</webhook>
```
**NOTE:** This authorization header does not actually serve as authorizing, rather it is for validation for the end user listening to the Webhook.

### Step 4: Add Event
Makes a PUT request to `{base_url}/@api/deki/webhooks/{id}/events/page_create` to configure the webhook to receive page creation events, using cookie-based authentication.

### Step 5: Listen for Incoming Requests (Optional)
After setup, you can choose to listen for incoming webhook requests in real-time. The script will:
- Poll the webhook.site API every 2 seconds for new requests
- Display incoming requests with timestamps, headers, and body content
- Pretty-print JSON payloads for easier reading
- Continue listening until you press Ctrl+C

## Authentication

The script uses basic authentication for the target site:

1. **Basic Authentication Required**: The script uses basic authentication credentials (username/password) to authenticate with the target site
2. **Credentials Configuration**: You must update the `auth_credentials` tuple in the `webhook_setup.py` file at line 52:
   ```python
   auth_credentials = ("YOUR_USERNAME", "YOUR_PASSWORD")
   ```
3. **Cookie-based Session**: After authentication, the script saves session cookies to `cookies.txt` for subsequent API requests

**Important**: Before running the script, you must edit `webhook_setup.py` and replace the REDACTED values with your actual username and password.

## Customization

- **Modify authentication credentials**: Update the `auth_credentials` tuple in the `authenticate_with_expert()` function
- **Adjust polling interval**: Change the `poll_interval` parameter in `listen_to_webhook()` (default is 2 seconds)
- **Add more events**: Create additional functions similar to `add_page_create_event()` for other event types such as:
 -  page_copy, page_move, page_restore, page_delete, pagetag_update, pageproperty_create, pageproperty_delete, pageproperty_update, pagedisplayname_update, pagerestriction_update, pagegrant_create, pagegrant_delete, pagecontent_update, pagecontenttype_update, attachment_restore, attachment_copy, attachment_move, attachment_delete, attachment_update, attachment_create, attachmentproperty_update, attachmentproperty_create, attachmentproperty_delete, user_update, user_create, pagecontent_contentreuseupdate



## Viewing Webhook Requests

After setup, the script provides a URL to view incoming webhook requests in real-time. This is useful for:
- Testing webhook payloads
- Debugging webhook configurations
- Monitoring event triggers

## Error Handling

The script includes comprehensive error handling for:
- Network failures
- API errors
- XML parsing issues
- Missing webhook IDs

## Example Output

```
============================================================
Webhook Setup Script
============================================================

Enter the base URL of your target site: https://example.com

Generating unique webhook URL...
Webhook URL created: https://webhook.site/abc123...
   View requests at: https://webhook.site/#!/abc123...

Creating webhook at https://example.com...
Webhook created successfully!
   Webhook ID: 42

Adding page_create event to webhook 42...
page_create event added successfully!

============================================================
Setup Complete!
============================================================
Webhook URL: https://webhook.site/abc123...
Webhook ID: 42

Your webhook is now configured to receive page_create events.
View incoming requests at: https://webhook.site/#!/abc123...

## Triggering the Webhook

To test the webhook and trigger a page_create event, you must:

1. **Log in to your target site** using the same credentials configured in the script
2. **Manually create a new page** in the site
3. The webhook will automatically trigger and send a payload to your webhook.site URL when the page is created

The webhook only responds to actual page creation events within the target site - it cannot be triggered programmatically through this script.

------------------------------------------------------------
Do you want to listen for incoming webhook requests? (y/n): y

============================================================
Webhook Listener Active
============================================================
Listening for incoming requests...
Press Ctrl+C to stop listening

============================================================
New Request Received!
   Time: 2024-01-29T10:30:45Z
   Method: POST
   Request ID: def456...

   Body:
      <event id="143c3406-fdfd-11f0-8674-aa9553f76750" datetime="2026-01-30T16:59:45Z" mt-epoch="1136393985653" type="page:create" wikiid="REDACTED" language="en-US" journaled="true" version="5"><request id="143c3406-fdfd-11f0-8674-2e3f57c9d8ea" seq="1" count="2"><signature>POST:pages/*/contents</signature></event>
============================================================

Stopped listening to webhook
```

## Troubleshooting

- **ID extraction fails**: The script will prompt you to manually enter the webhook ID from the response
- **Authentication errors**: Ensure your credentials are correct in the `auth_credentials` tuple and that `cookies.txt` is created successfully
- **403 Forbidden when creating webhook**: If you receive a 403 error when creating the webhook, the webhooks feature may not be enabled for your site. Contact your Customer Success Manager (CSM) or support to enable the webhooks feature
- **Missing cookies.txt**: The script will exit with an error if the cookie file is not found - make sure authentication succeeds first
- **Network issues**: Check your internet connection and target site availability
- **XML parsing errors**: Verify the API response format matches expectations
