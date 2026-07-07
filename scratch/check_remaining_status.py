import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "Storeboard": "https://www.storeboard.com/pocatellotreeservice",
    "Adpost Member Link": "https://www.adpost.com/members/pocatellotreeservice/",
    "AmericanTowns": "https://forms.americantowns.com/viewevent/67808821",
    "Tuugo Search (Attempt)": "https://www.tuugo.us/Search?q=Pocatello+Tree+Service",
    "Yellow Place Search (Attempt)": "https://yellow.place/en/search?q=Pocatello+Tree+Service",
    "CallUpContact (Attempt)": "https://www.callupcontact.com/search.php?q=Pocatello+Tree+Service"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Running status check on remaining links...\n")

for name, url in urls.items():
    print(f"Checking {name}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
            print(f"  HTTP Status: {response.status}")
            print(f"  Final URL: {response.geturl()}")
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error: {e.code} ({e.reason})")
    except urllib.error.URLError as e:
        print(f"  Network/URL Error: {e.reason}")
    except Exception as e:
        print(f"  Error: {str(e)}")
    print("-" * 50)
