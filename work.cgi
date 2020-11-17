#!/usr/bin/python3
import utils, os, sys, time

# start by parsing the query string
qs = utils.parse_qs(os.environ["QUERY_STRING"])
try:
	# Each assertion in here will trigger the usage message on failure.
	assert "work" in qs, "Must supply a work to grab!"
	assert len(qs["work"])==1, "Can't grab more than one work at a time!"
	id = next(iter(qs["work"]))
	assert id.isdigit(), "Work ID should be a number!"
except AssertionError as e:
	print("Content-Type: text/plain")
	print()
	print(e.args[0])
	print("Usage: {}://{}{}{}?work={{work to get}}".format(os.environ["REQUEST_SCHEME"],os.environ["HTTP_HOST"],(":"+os.environ["SERVER_PORT"] if not utils.on_normal_port() else ""),os.environ["REQUEST_URI"]))
	sys.exit(0)

format = "html"
if "format" in qs:
	format = next(iter(qs["format"])).lower()

FORMATS = {
	"html": "text/html",
	"azw3": "application/x-mobi8-ebook",
	"mobi": "application/x-mobipocket-ebook",
	"epub": "application/epub+zip",
	"pdf": "application/pdf"
}

if format not in FORMATS:
	print("Content-Type: text/plain")
	print()
	print("Illegal format! Must be one of {}".format(", ".join([repr(k) for k in FORMATS.keys()])))
	print("Usage: {}://{}{}{}?work={{work to get}}".format(os.environ["REQUEST_SCHEME"],os.environ["HTTP_HOST"],(":"+os.environ["SERVER_PORT"] if not utils.on_normal_port() else ""),os.environ["REQUEST_URI"]))
	sys.exit(0)

url = utils.WORK_DOWNLOAD_URL.format(id,format,round(time.time()-0.5))

req = utils.requests.get(url)
if req.status_code!=200:
	print("Content-Type: text/plain")
	print()
	print("Error! Request returned status code {}".format(req.status_code))
	sys.exit(0)

print("Content-Type: "+FORMATS[format])
print()
sys.stdout.flush()
sys.stdout.buffer.write(req.content)
