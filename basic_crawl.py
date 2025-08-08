import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from logger import Colors, log_error, log_header, log_info, log_success, log_warning


def crawl_site(start_url, max_depth=2):
    visited = set()
    to_visit = [(start_url, 0)]
    domain = urlparse(start_url).netloc
    all_urls = []

    while to_visit:
        url, depth = to_visit.pop()
        if url in visited or depth > max_depth:
            continue

        try:
            response = requests.get(url, timeout=5)
            visited.add(url)
            all_urls.append(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                if urlparse(href).netloc == domain:
                    to_visit.append((href, depth + 1))

        except requests.RequestException:
            continue

    return sorted(set(all_urls))

if __name__ == "__main__":
    site_urls = crawl_site("https://medom-nekretnine.com/stan/", max_depth=1)
    log_success(
        f"Successfully crawled {len(site_urls)} URLs from site"
    )
    for url in site_urls:
        print(url)