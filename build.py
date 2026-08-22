"""Full site build: generate all pages + ads.txt + sitemap.xml."""
import os
import generate
from static_pages import ADSENSE_CLIENT

OUTPUT_DIR = generate.OUTPUT_DIR
BASE_URL = generate.BASE_URL


def build_ads_txt():
    pub_id = ADSENSE_CLIENT.replace("ca-pub-", "pub-")
    content = f"google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n"
    with open(os.path.join(OUTPUT_DIR, "ads.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("ads.txt written")


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
    build_sitemap()


if __name__ == "__main__":
    main()
