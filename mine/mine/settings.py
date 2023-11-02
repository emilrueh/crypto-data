import random
from dotenv import load_dotenv
import os

from mine.utilities import generate_random_id

load_dotenv()


BOT_NAME = "mine"

SPIDER_MODULES = ["mine.spiders"]
NEWSPIDER_MODULE = "mine.spiders"

# Configure logging level
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s (line %(lineno)d): %(message)s"

RETRY_TIMES = 2  # Number of retries

# BROWSER-HEADERS
#
# choose one of the following options or None
#   "user_agent-manual"
#   "headers-manual"
#   "user_agent-middleware"
#   "headers-middleware"
##################################
headers_type = None  # <--- SWITCH
##################################

if headers_type == "user_agent-manual":
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

# ScrapeOps
SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")
SCRAPEOPS_ENDPOINT = os.getenv("SCRAPEOPS_HEADERS_ENDPOINT")

SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = SCRAPEOPS_ENDPOINT + "user-agents"
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = SCRAPEOPS_ENDPOINT + "browser-headers"
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True

SCRAPEOPS_NUM_RESULTS = 50

# PROXIES
##############################################
SCRAPEOPS_PROXY_ENABLED = False  # <--- SWITCH
##############################################
# Configure advanced settings integrated into the ScrapeOps proxy API
# See https://scrapeops.io/docs/proxy-aggregator/advanced-functionality/functionality-list/
# SCRAPEOPS_PROXY_SETTINGS = {"country": "de", "bypass": "cloudflare", "residential": True, "render_js": True}

# f"{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_ENDPOINT}:{PROXY_PORT}"
proxy_provider = "BRIGHTDATA" if not SCRAPEOPS_PROXY_ENABLED else "SCRAPEOPS"

#############################################################################
proxy_service = "BROWSER"  # "DATACENTER" "UNLOCKER" "BROWSER"  # <--- SWITCH
#############################################################################

PROXY_MIDDLEWARES_ACTIVATED = True if proxy_service != "BROWSER" else False  # <--- SWITCH

custom_proxies_activated = (
    False if PROXY_MIDDLEWARES_ACTIVATED or proxy_service == "BROWSER" else True
)

PROXY_ENDPOINT = os.getenv(f"{proxy_provider}_PROXY_ENDPOINT")
PROXY_PORT = os.getenv(
    f"{proxy_provider}_PORT"
    if proxy_service != "BROWSER"
    else f"{proxy_provider}_{proxy_service}_PORT"
)
PROXY_USER = os.getenv(f"{proxy_provider}_{proxy_service}_USER")
PROXY_PASSWORD = os.getenv(f"{proxy_provider}_{proxy_service}_PWORD")

SESSIONS_START_ID = generate_random_id(no_special=True, print_id=False)

# brightdata geo-tagging
proxy_country = "de"
if proxy_country and PROXY_USER and proxy_provider == "BRIGHTDATA":
    PROXY_USER = PROXY_USER + f"-country-{proxy_country}"

# HEADLESS BROWSERS FOR JS
HEADLESS_BROWSER = "selenium"  # <--- SWITCH

# SELENIUM
#######################################
use_remote_driver = True  # <--- SWITCH
#######################################

SELENIUM_DRIVER_NAME = "chrome"  # "remote" "firefox" "chrome"

SELENIUM_DRIVER_ARGUMENTS = []

if use_remote_driver and proxy_service == "BROWSER" and proxy_provider == "BRIGHTDATA":
    SELENIUM_COMMAND_EXECUTOR = (
        f"https://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_ENDPOINT}:{PROXY_PORT}"
    )

elif SELENIUM_DRIVER_NAME == "chrome":
    SELENIUM_DRIVER_ARGUMENTS.append("--headless")

elif SELENIUM_DRIVER_NAME == "firefox":
    SELENIUM_DRIVER_ARGUMENTS = ["-headless"]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = round(random.uniform(1, 3), 3)

# Override the default request headers:
if headers_type == "headers-manual":
    DEFAULT_REQUEST_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en",
    }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "mine.middlewares.MineDownloaderMiddleware": 543,
}
# BROWSER HEADERS MIDDLWARES
if headers_type == "headers-middleware":
    DOWNLOADER_MIDDLEWARES["mine.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware"] = 300
elif headers_type == "user_agent-middleware":
    DOWNLOADER_MIDDLEWARES["mine.middlewares.ScrapeOpsFakeUserAgentMiddleware"] = 300

# PROXY MIDDLEWARES
if PROXY_MIDDLEWARES_ACTIVATED:
    if SCRAPEOPS_PROXY_ENABLED:
        DOWNLOADER_MIDDLEWARES[
            "scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk"
        ] = 725
    else:
        DOWNLOADER_MIDDLEWARES["mine.middlewares.ProxyNetworkMiddleware"] = 500

if HEADLESS_BROWSER == "selenium":
    DOWNLOADER_MIDDLEWARES["scrapy_selenium.SeleniumMiddleware"] = 800

# Configure item pipelines
ITEM_PIPELINES = {
    "mine.pipelines.MinePipeline": 300,
}

# DATA STORAGE
FEEDS = {
    "output.json": {"format": "json", "overwrite": True},
    "backup.csv": {"format": "csv", "overwrite": False},
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
