# ygWarcToJson.py
Outputs cleaned-up JSON from WARC'd Yahoo Groups API response data.  
This should make the data easier to display dynamically on a webpage later. 

# About
I (Anthony) was doing some research on a Yahoo Group called videoblogging. Thankfully Archive Team [backed up][1] all the posts from the group. But the archive, in [WARC format][2], only contained JSON from the Groups API. No forum interface or navigable hierarchy. Just a bunch of JSON objects, two per post (an "info" object and a "raw" object). Not very readable! :(

Turns out this is a very [common issue][3] for archived Yahoo Groups. 

The first step towards rebuilding a readable, navigable version of the group is ditching the WARC format headers and marrying the JSON from each message's /info and /raw records into a single object. 

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


[1]: https://archive.org/details/yahoo-groups-2017-05-23T02-01-34Z-c8358f
[2]: https://iipc.github.io/warc-specifications/specifications/warc-format/warc-1.0/
[3]: https://github.com/anirvan/yahoo-group-archive-tools#4-yahoo-groups-api-issues-and-how-we-work-around-them
