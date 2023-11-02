# ...Add Your Title...

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

...add your intoduction...

## Features

- **Keyword-based Searches**: The spider can be configured to search based on a list of custom keywords.
- **Extensive Data Collection**: Captures a plethora of data including ..., and more.
- **Proxies & Headless Browsing**: Built-in support for using ScrapeOps or custom proxies, as well as Firefox for headless browsing.
- **Pagination Support**: Automatically navigates through pages up to a specified limit.
- **Output**: Stores the scraped data in a structured JSON format (or optionally CSV)

## Prerequisites

- python 3.x
- ``chromedriver.exe`` in the same directory as scrapy.cfg (and Google Chrome browser)
- proxy credentials or API e.g. Brightdata or ScrapeOps (make sure to use a service that renders JavaScript)

## Installation

First, clone the repository:

```
git clone https://github.com/emilrueh/scrapy-template
```

Navigate to the project directory and install the required packages:

```
cd mine
pip install -r requirements.txt
```

## Usage
#### Setup your ``.env`` file:
- by using ``.env.template`` and adding your proxy credentials.

#### Set your `FEEDS`:
- in the spider or your `settings.py` (disable in the spider), to choose JSON or CSV or both.

```python
# settings.py
FEEDS = {
    "output.json": {"format": "json", "overwrite": True},
    "backup.csv": {"format": "csv", "overwrite": False},
}
```

```python
# spiders/spider_name.py
custom_settings = {
    "FEEDS": {
        "data.json": {"format": "json", "overwrite": True},
        # "data.csv": {"format": "csv", "overwrite": True},
    },
    ...
}
```

#### Add geo tag to proxies in `settings.py`:
- to keep the package prices in a uniform currency
```python
# for scrapeops
SCRAPEOPS_PROXY_SETTINGS = {"country": "us", "render_js": True}

# or for brightdata
proxy_country = "us"
```

#### Configure pagination:
- Make sure to manually check how many pages your keyword has and input into the spider pagination settings! 
```python
# line 178 in spider_name.py
if self.page <= 20:
```

### To start the spider:
Navigate to the 'mine' directory (`cd mine`) and run:

```
scrapy crawl spider_name
```

This will generate a JSON (and or CSV) file in the project directory containing the scraped data.

## Contributing
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are welcome.


## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

