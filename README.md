# ygWarcToJson.py
Outputs cleaned-up JSON from WARC'd Yahoo Groups API response data. 
This should make the data easier to display dynamically on a webpage later. 

# About
I (Anthony) was doing some research on a Yahoo Group called videoblogging. Thankfully Archive Team [backed up](https://archive.org/details/yahoo-groups-2017-05-23T02-01-34Z-c8358f) all the posts from the group. But the archive, in WARC format, only contained JSON from the Groups API. No forum interface or navigable hierarchy. Just a bunch of JSON objects, two per post (an "info" object and a "raw" object). Not very readable! :(

Turns out this is a very [common issue](https://github.com/anirvan/yahoo-group-archive-tools) for archived Yahoo Groups. 

This is the first step towards rebuilding a readable, navigable version of the group: ditching the WARC format headers and marrying the JSON from the /info and /raw URIs into a single "post" object. 

# Methods
- ygWarcToJson()
  - parse_records() - accepts a warcio.stream object and returns array of records.
  - marry_records() - accepts array of records, finds unique messages, and marries /raw and /info records for each. 
  - get_roster() - accepts array of married records and returns a dictionary of unique userIds and all posts by that userId.
  - get_threads() - accepts array of married records and returns dictionary of unique topicIds and all posts in that topic.
  - save_to_json() - accepts array of dicts and saves as JSON object in the current directory. 

# TODO
- Re-write as class instead of standalone method.
- Clean up get_roster() without funky delimiter. 
- Probly parse email bodies a bit more thoroughly. 
- Optimization / concurrence?
