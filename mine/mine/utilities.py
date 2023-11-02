from scrapy_selenium import SeleniumRequest

from urllib.parse import urlencode
from w3lib.html import replace_tags

import re, uuid, html


# NETWORK
#
def make_selenium_request(url, callback, meta=None):
    meta = meta or {}
    retrying = meta.get("retrying", False)
    return SeleniumRequest(url=url, callback=callback, meta=meta, dont_filter=retrying)


def get_proxy_api_url(url, api_key, endpoint, country=None, bypass=None, render_js=False):
    payload = {
        "api_key": api_key,
        "url": url,
    }
    if country:
        payload.update({"country": country})
    if bypass:
        payload.update({"bypass": bypass})
    if render_js:
        payload.update({"render_js": render_js})

    proxy_url = f"{endpoint}?{urlencode(payload)}"
    return proxy_url


# DATA CLEANING
#
def string_clean(value, to_clean=None, clean_within=False):
    if value:
        if to_clean:
            value = value.replace(to_clean, "")
        if clean_within:
            value = re.sub(r"\s+", " ", value)
        return value.strip()
    else:
        return value


def number_clean(value, to_type=None, to_keep=""):
    if value:
        try:
            cleaned_number = "".join(re.findall(f"[0-9{to_keep}]", value))
            cleaned_number = cleaned_number.replace(to_keep if to_keep else ",", ".")

            if to_type:
                if to_type == "float":
                    cleaned_number = float(cleaned_number)
                elif to_type == "int" or to_type == "integer":
                    cleaned_number = int(cleaned_number)

            else:
                if "." in cleaned_number:
                    cleaned_number = float(cleaned_number)
                else:
                    cleaned_number = int(cleaned_number)

            return cleaned_number

        except ValueError as e:
            print("value that errored: ", value)
            print("error: ", e)
            return None

    else:
        return value


# HTML and ITEMS
def replace_tags_with_space(value):
    return replace_tags(value, token=" ")


# Merge the child item loaders into the parent 'fiverr' loader.
def merge_child_item_with_parent_item(parent_loader, child_loader, prefix):
    child_item = child_loader.load_item()
    for key, value in child_item.items():
        parent_loader.add_value(f"{prefix}_{key}", value)


# -----------
# Other
def generate_random_id(chars=None, no_special=False, print_id=False):
    ran_id = str(uuid.uuid4())

    if chars:
        try:
            ran_id = ran_id[:chars]
        except Exception as e:
            print(e)

    if no_special:
        ran_id = ran_id.replace("-", "")

    if print_id:
        print("New ID:", ran_id)

    return ran_id


def decode_html_entities(value):
    return html.unescape(value)
