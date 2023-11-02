# SCRAPY
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from mine.items import TemplateItem

# PROXY
try:
    from mine.settings import PROXY_ENDPOINT, PROXY_USER, PROXY_PASSWORD
except ImportError:
    PROXY_ENDPOINT = None
    PROXY_USER = None
    PROXY_PASSWORD = None

from mine.settings import SCRAPEOPS_API_KEY, custom_proxies_activated

# SELENIUM
from mine.settings import HEADLESS_BROWSER

if HEADLESS_BROWSER == "selenium":
    use_selenium = True
    from mine.utilities import make_selenium_request
else:
    use_selenium = False

# EXTRA
from urllib.parse import urljoin
from random import randint

from mine.utilities import get_proxy_api_url

import json, time, logging


class TemplateSpider(Spider):
    name = "template"

    allowed_domains = ["emilrueh.github.io"]
    custom_settings = {
        "FEEDS": {
            "fiverr.json": {"format": "json", "overwrite": True},
            # "fiverr.csv": {"format": "csv", "overwrite": True},
        },
        "SCRAPEOPS_PROXY_SETTINGS": {
            "render_js": True,
            "country": "de",
            "bypass": "cloudflare",
        }
        if PROXY_ENDPOINT and SCRAPEOPS_API_KEY
        else None,
    }

    # adding proxy url as allowed domain
    if PROXY_ENDPOINT:
        allowed_domains.append(
            PROXY_ENDPOINT.split("/")[2] if "/" in PROXY_ENDPOINT else PROXY_ENDPOINT
        )
        logging.info(f"Allowed Domains:\n{allowed_domains}")

    def __init__(self):
        # SET KEYWORDS
        self.keywords = ["hero", "about", "projects", "contact"]
        # SET START URLS
        self.start_urls = [f"https://emilrueh.github.io/#{keyword}" for keyword in self.keywords]

        # sub utilities
        self.current_start_url = "empty"
        self.proxy = (
            f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_ENDPOINT}"
            if custom_proxies_activated
            else None
        )
        self.custom_meta = {"proxy": self.proxy}

        # check for pagination
        self.seen_content = set()
        self.page = 1
        self.test_url_counter = 0
        # check for previous scraper returns
        self.check_previous_file = False
        self.previous_file = r"C:\Users\{user}\path\to\previously\scraped\file.json"
        self.previous_links = set()

    def start_requests(self):
        # CHECKING for previously scraped data
        try:
            if self.check_previous_file:
                with open(self.previous_file, encoding="utf-8") as f:
                    previous_file = json.load(f)
                for item in previous_file:
                    self.previous_links.add(item["gig_link"])
        except FileNotFoundError:
            logging.warning(
                "No path for file with previously scraped data given. Continuing without..."
            )

        # START
        for url in self.start_urls:
            self.current_start_url = url

            # scrapeops proxy api endpoint
            if custom_proxies_activated and PROXY_ENDPOINT:
                self.current_start_url = get_proxy_api_url(
                    url, SCRAPEOPS_API_KEY, PROXY_ENDPOINT, render_js=True
                )

            if use_selenium:
                yield make_selenium_request(url, self.parse, self.custom_meta)
            else:
                yield Request(url=url, callback=self.parse, meta=self.custom_meta)

    def parse(self, response):
        new_content = set()

        # DISCOVERY
        # ---------+
        items = response.css("div.template")

        for i in items:
            # CREATE ITEM URL:
            item_url = urljoin(i.css(""))

            if use_selenium:
                yield make_selenium_request(item_url, self.parse_item, self.custom_meta)
            else:
                yield response.follow(item_url, callback=self.parse_item)

        # # PAGINATION
        # # ----------+
        max_pages = 20  # set maximum of pages to scrape manually

        self.page += 1
        if self.page <= max_pages:
            next_page = f"{self.current_start_url}{self.page}"

            # setting proxy api endpoint
            if custom_proxies_activated and PROXY_ENDPOINT:
                next_page = get_proxy_api_url(
                    next_page, SCRAPEOPS_API_KEY, PROXY_ENDPOINT, render_js=True
                )

            logging.info(f"\nNext page:\n{next_page}\n")

            if use_selenium:
                yield make_selenium_request(next_page, self.parse, self.custom_meta)
            else:
                yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        retry_count = response.meta.get("retry_count", 0)
        if response.status == 403 and retry_count > 0:
            raise CloseSpider("403 Forbidden. Stopping spider...")

        item = ItemLoader(item=TemplateItem(), response=response)

        # EXTRACTION
        # ----------+
        item.add_css("key", "selector")

        # CONSTRUCTION
        # ------------+
        full_data = item.load_item()

        yield full_data
