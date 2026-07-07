import urllib.request
import urllib.error
import re
import ssl

# Bypass SSL certificate verification for simple fetching
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "Houzz": "https://www.houzz.com/pro/webuser-501299159/__public",
    "Manta": "https://www.manta.com/c/mk2yh6b/pocatello-tree-service",
    "Spoke": "https://www.spoke.com/companies/pocatello-tree-service-6159ef4f3853d8f9c2046c51",
    "Storeboard": "https://www.storeboard.com/pocatellotreeservice",
    "Lacartes": "http://www.lacartes.com/business/Pocatello-Tree-Service/1940296",
    "Cybo": "https://www.cybo.com/US-biz/pocatello-tree-service_20",
    "AmericanTowns Form": "https://forms.americantowns.com/viewevent/67808821"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Starting live audit of current citation links...\n")

for name, url in urls.items():
    print(f"Checking {name}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            status = response.status
            
            # Check for phone number
            has_phone = "208-417-7993" in html or "208) 417-7993" in html
            # Check for zipcode
            has_zip_83204 = "83204" in html
            has_zip_83201 = "83201" in html
            # Check for street address
            has_address = "228 Center" in html or "228 East Center" in html
            
            print(f"  HTTP Status: {status}")
            print(f"  Phone (208-417-7993): {'Found' if has_phone else 'Not Found'}")
            print(f"  Zip Code 83204: {'Found' if has_zip_83204 else ('Found 83201 (Old)' if has_zip_83201 else 'Not Found')}")
            print(f"  Street Address (228 Center St): {'Found' if has_address else 'Not Found'}")
            
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error: {e.code} ({e.reason})")
    except urllib.error.URLError as e:
        print(f"  Network/URL Error: {e.reason}")
    except Exception as e:
        print(f"  Unexpected Error: {str(e)}")
    print("-" * 50)
