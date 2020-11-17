# requests lib
import requests
# BeautifulSoup
from bs4 import BeautifulSoup
# HTTP error (raised by Response.raise_for_status)
from requests.exceptions import HTTPError
# Query string parser and url encoder
from urllib.parse import parse_qs, quote, urlencode

last_request_encoding=""

def get(url,soup=False):
	"""Get URL and return the result as a BeautifulSoup object if soup is True."""
	global last_request_encoding
	r = requests.get(url)
	r.raise_for_status()
	last_request_encoding=r.encoding
	if soup:
		return BeautifulSoup(r.text,"lxml")
	else:
		return r.text

def quote_tag(tag):
	"""Quotes {tag} as a tag, suitable for insertion into the tag works URL."""
	return quote(tag,"()").replace("%2F","*s*")

import os
def on_normal_port():
	if os.environ["REQUEST_SCHEME"]=="http":
		return os.environ["SERVER_PORT"]=="80"
	if os.environ["REQUEST_SCHEME"]=="https":
		return os.environ["SERVER_PORT"]=="443"

# Utility definitions
TAG_WORKS_URL = "https://archiveofourown.org/tags/{}/works"
TAG_WORKS_PAGED_URL = "https://archiveofourown.org/tags/{}/works?page={}"
WORK_DOWNLOAD_URL = "https://archiveofourown.org/downloads/{0}/{0}.{1}?updated_at={2}"
USER_WORKS_URL = "https://archiveofourown.org/users/{}/works"
USER_WORKS_PAGED_URL = "https://archiveofourown.org/users/{}/works?page={}"
