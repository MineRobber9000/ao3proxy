#!/usr/bin/python3
import utils, os, sys, textwrap

def eightycol(s):
	paragraphs=s.splitlines()
	out = ""
	for para in paragraphs:
		out+=textwrap.fill(para,80)
		out+="\n"
	return out.strip()

# start by parsing the query string
qs = utils.parse_qs(os.environ["QUERY_STRING"])
try:
	# Each assertion in here will trigger the usage message on failure.
	assert "user" in qs, "Must supply a user to search!"
	assert len(qs["user"])==1, "Can't supply more than one user!"
	user = next(iter(qs["user"]))
except AssertionError as e:
	print("Content-Type: text/plain")
	print()
	print(e.args[0])
	print("Usage: {}://{}{}{}?user={{user to list}}".format(os.environ["REQUEST_SCHEME"],os.environ["HTTP_HOST"],(":"+os.environ["SERVER_PORT"] if not utils.on_normal_port() else ""),os.environ["REQUEST_URI"]))
	sys.exit()

if "page" in qs:
	page = next(iter(qs["page"]))
	url = utils.USER_WORKS_PAGED_URL.format(user,page)
else:
	url = utils.USER_WORKS_URL.format(user)

try:
	# Grab the URL and soup it
	soup = utils.get(url,True)
except utils.HTTPError: # the request failed
	print("Content-Type: text/plain")
	print()
	print("The request failed, for some reason. Maybe the user you're looking for doesn't exist?")
	print("Usage: {}://{}{}{}?user={{user to list}}".format(os.environ["REQUEST_SCHEME"],os.environ["HTTP_HOST"],(":"+os.environ["SERVER_PORT"] if not utils.on_normal_port() else ""),os.environ["REQUEST_URI"]))
	sys.exit()

# Print headers and top of page
print("Content-Type: text/html; charset="+utils.last_request_encoding)
print()
print("""<!doctype html>
<html>
<head>
<title>Works under user "{0}"</title>
</head>
<body>
<h1>Works under user "{0}"</h1>
<hr>""".format(user))

# This could be moved over the above, but meh
include_adult=False
if "include_adult" in qs and next(iter(qs["include_adult"])).lower() in "yes true y".split():
	include_adult=True

for work in soup.find_all("li",class_="work"):
	# If we haven't indicated that we want adult ratings, then Mature/Explicit results are skipped over
	# In a perfect world, I'd only have to make this remove Explicit ratings (and then I could just
	# not click on Mature results), but people sometimes tag naughty shit with Mature as well. I mean,
	# even only giving G and T rating results still opens me up to some stuff, but definitely much less
	# than what I could run into otherwise.
	if work.find("span",class_="rating").text in "Mature Explicit".split() and not include_adult:
		print("<p>Work skipped ("+work.find("span",class_="rating").text+" rating)</p><hr>")
		continue
	# title is the first link
	title = work.find("a")
	# authors are links with rel="author"
	author = ", ".join([tag.text for tag in work.find_all("a",rel="author")])
	# if no such links exist, then the author is Anonymous
	# this happens when the author submits a work to a collection with the attribute of submissions being anonymous
	if not work.find("a",rel="author"):
		author = "Anonymous"
	print("<p><a href='work.cgi?work={}'>{}</a> by {}<br>".format(title.attrs["href"].split("/")[-1],title.text,author))
	# the 4 box things; rating, warnings, category, status
	print("Rating: "+work.find("span",class_="rating").text+"<br>")
	print("Warnings: "+work.find("span",class_="warnings").text+"<br>")
	print("Category(s): "+work.find("span",class_="category").text+"<br>")
	print("Status: "+work.find("span",class_="iswip").text+"<br>")
	# now comes the fun part
	print("Tags:",end=" ")
	# let's make a list of all of the tags this work has
	# it can't contain warnings (since we've already put those above), and we don't really want to have
	# to make links for them, so we can just take text
	tags = [tag.text for li in work.find_all("li") if (tag:=li.find("a",class_="tag")) and "warnings" not in li.attrs.get("class",[])]
	print(", ".join(tags)+"<br>")
	print("Summary:<br>")
	# now we're gonna do some hacky shit
	# we're gonna turn the summary into HTML source again, manually turn break tags into newlines, and
	# then turn it back into a BeautifulSoup object and textify it
	summary = str(work.blockquote)
	summary = summary.replace("<br/>","\n")
	summary = utils.BeautifulSoup(summary,"lxml").get_text(separator="\n\n")
	print("<pre>"+eightycol(summary.strip())+"</pre><br>")
	stats = work.dl.text.strip()
	stats = stats.replace(":\n",": ").replace("\n","<br>")
	print(stats)
	print("</p><hr>")

user=next(iter(qs["user"]))
if "page" not in globals():
	page = 1
page = int(page)
params = dict(user=user, page=page+1)
if include_adult:
	params["include_adult"]="true"
print("<p><a href='./list.cgi?{1}'>Page {0!s} (if it exists)</a></p>".format(page+1,utils.urlencode(params)))
print("""</body>
</html>""")
