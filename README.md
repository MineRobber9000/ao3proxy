# ao3proxy

A proxy I wrote so I could read AO3 stories at school.

## Requirements

 - FastCGI or other CGI server, with Python 3 support
 - `pip3 install -r requirements.txt`

## Notes

Don't spam AO3 with requests. 1 page per second, no more, no less. I didn't build any sort of rate-limiting into this, since it's supposed to be something you set up for personal use. As such, I'm not running a public version of this, since it'd get abused into the ground almost instantly.

The reason I wrote this with Python CGI, rather than with PHP, is because frankly, I hate PHP. I'm much more comfortable writing Python, and my hosting situation will let me write Python, so Python I shall write.

If AO3 changes its layout, this *will* break. Therefore, I make no guarantees that any of this will work later down the line. However, I do guarantee that if I am still using this when that happens, I'll try to fix it to the best of my ability.

If you want to change the tags available on the index page, just add entries to the `tags` list. The first item of each entry is the name, and the second entry is the tag itself.
