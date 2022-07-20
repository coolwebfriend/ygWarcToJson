# ygWarcToJson.py
Creates JSON from WARC'd Yahoo Groups API response data. 
This should make the data easier to display dynamically on a webpage later. 

# About
I was doing some research on a Yahoo Group called videoblogging. 
Thankfully Archive Team backed up all the posts from the group.
But the archive, in WARC format, only contained JSON from the Groups API. 
No navigable hierarchy or forum interface. Just a bunch of JSON objects, 
two per post (and "info" object and a "raw" object). Not very readable :(

The first step towards rebuilding a readable, navigable version of the group
is to ditch the WARC format headers and marry the "info" and "raw" JSON
into a single "post" object. 

# Notes
- I'm a hobbyist and this code is probly far less than optimal. 
- The resulting file is somehow larger than the WARC file? Lots of quotes and brackets I guess. 


# Next Steps
- Figure out how to reconstruct a thread based on an object's metadata.
