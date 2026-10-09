"""
Pings IndexNow so Bing (and the other participating engines - Yandex, Seznam, Naver, ...) recrawl
new or changed pages right away. Bing's index is also what ChatGPT search and Copilot draw on.
Google doesn't support IndexNow - for Google, resubmit the sitemap / use URL Inspection in
Search Console.

Usage: push the site, wait for GitHub Pages to deploy (1-2 minutes), then run
    python indexnow.py                                  # every URL in sitemap.xml
    python indexnow.py index.html guides.html           # just these pages

The key file (docs/<INDEXNOW_KEY>.txt) must already be live, or the ping is rejected.
"""
import json
import re
import sys
import urllib.error
import urllib.request

from build import INDEXNOW_KEY, OUTPUT_DIR, BASE_URL

ENDPOINT = "https://api.indexnow.org/indexnow"  # shared with every participating engine


def sitemap_urls():
    with open(f"{OUTPUT_DIR}/sitemap.xml", encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def main(files):
    urls = [f"{BASE_URL}/{f}" for f in files] if files else sitemap_urls()
    payload = json.dumps({
        "host": BASE_URL.removeprefix("https://"),
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }).encode("utf-8")

    req = urllib.request.Request(
        ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"{ENDPOINT} -> {resp.status} ({len(urls)} URLs)")  # 200/202 = accepted
    except urllib.error.HTTPError as e:
        print(f"{ENDPOINT} -> {e.code} {e.read().decode('utf-8', 'replace')[:200]}")


if __name__ == "__main__":
    main(sys.argv[1:])
