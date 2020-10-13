#!/usr/bin/python3
from utils import urlencode

tags = [
#	["THIS IS THE NAME THAT SHOWS UP","THIS IS THE TAG THAT ACTUALLY GETS SEARCHED"]
	["Sonic", "Sonic the Hedgehog - All Media Types"],
	["Infidget", "Avatar | Custom Hero (Sonic Forces)/Infinite (Sonic the Hedgehog)"],
]

tags = "\n".join(['<li><a href="list.cgi?{}">{}</a></li>'.format(urlencode(dict(tag=x[1])),x[0]) for x in tags])

print("Content-Type: text/html")
print()
print("""<html>
<head>
<title>AO3Proxy</title>
</head>
<body>
<h1 id="ao3proxy">ao3proxy</h1>
<p>A proxy I wrote so I could read AO3 stories at school.</p>
<h2 id="chosen-few">The Chosen Few</h2>
<p>Some of the fandoms/other tags I follow:</p>
<ul>
{tags}
</ul>
<h2 id="get">Get a different tag</h2>
<form action="list.cgi">
<p><label for="tag">The tag you wish to list:</label>
<input type="text" name="tag" id="tag"></p>
<p><label for="include_adult">Include adult (Mature, Explicit) works?</label>
<input type="checkbox" name="include_adult" value="true" id="include_adult"></p>
<p><button type="submit">Submit</button></p>
</form>
</body>
</html>""".format(tags=tags))
