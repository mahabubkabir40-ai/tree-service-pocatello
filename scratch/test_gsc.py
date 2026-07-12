import os
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import googleapiclient
except ImportError:
    print("Installing google-api-python-client...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client"])

try:
    import google_auth_oauthlib
except ImportError:
    print("Installing google-auth-oauthlib...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-auth-oauthlib"])

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Define the GSC Read-Only Scope
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def main():
    # Get the project root directory
    scratch_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(scratch_dir)
    
    client_secret_path = os.path.join(root_dir, 'client_secret.json')
    token_path = os.path.join(root_dir, 'token.json')
    
    print(f"Looking for client_secret.json at: {client_secret_path}")
    
    if not os.path.exists(client_secret_path):
        print(f"Error: client_secret.json not found at {client_secret_path}!")
        return
        
    creds = None
    # Load existing token if it exists
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Starting authentication flow...")
            print("This will open a browser tab asking you to log into your Google Account.")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            # Run the local server to handle OAuth callback
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            print(f"Saved token to: {token_path}")

    # Build the Search Console API service
    service = build('searchconsole', 'v1', credentials=creds)
    
    # List GSC properties to test
    print("\nConnecting to Google Search Console...")
    try:
        site_list = service.sites().list().execute()
        print("\n--- Verified Properties in Your Account ---")
        if 'siteEntry' in site_list:
            for site in site_list['siteEntry']:
                print(f"- URL: {site['siteUrl']} (Permission: {site['permissionLevel']})")
        else:
            print("No verified sites found in this account.")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == '__main__':
    main()
