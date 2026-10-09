"""Full site build: generate all pages + ads.txt + robots.txt + sitemap.xml."""
import os
import generate
from static_pages import ADSENSE_CLIENT

OUTPUT_DIR = generate.OUTPUT_DIR
BASE_URL = generate.BASE_URL

# IndexNow key. The matching docs/<key>.txt must be live before a ping is accepted.
INDEXNOW_KEY = "76d6dde281440a0e9d4cae208a03d913"


def build_ads_txt():
    pub_id = ADSENSE_CLIENT.replace("ca-pub-", "pub-")
    content = f"google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n"
    with open(os.path.join(OUTPUT_DIR, "ads.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("ads.txt written")


def build_robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {BASE_URL}/sitemap.xml",
        "",
    ]
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("robots.txt written")


def build_indexnow_key():
    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)
    print("indexnow key file written")


def build_sitemap():
    urls = [
        f"{BASE_URL}/{fname}"
        for fname in sorted(os.listdir(OUTPUT_DIR))
        if fname.endswith(".html")
    ]
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>"""
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"sitemap.xml written ({len(urls)} URLs)")


def main():
    generate.main()
    build_ads_txt()
    build_robots_txt()
    build_indexnow_key()
    build_sitemap()


if __name__ == "__main__":
    main()
