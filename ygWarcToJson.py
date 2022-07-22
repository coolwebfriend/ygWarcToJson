#=============================================================================#
#        Creates JSON file from WARC'd Yahoo Groups API response data.
#  This should make the data easier to display dynamically on a webpage later. 
#
#  Anthony D'Angelo | http://heythats.cool | https://github.com/coolwebfriend
#
#=============================================================================#

import os
import json
import html
import urllib
from urllib.parse import urlparse
import warcio
from warcio.archiveiterator import ArchiveIterator
         
def ygWarcToJson(input_path):
    # Return a dictionary containing metadata and payloads of each WARC record.
    
    with open(input_path, 'rb') as stream:
        
        print("Getting WARC records...")
        records_array = []
        for record in ArchiveIterator(stream):
            uri = urlparse(record.rec_headers.get_header('WARC-Target-URI'))
            path = uri.path
            if "info" in path[-5:]: 
                suffix = "info"
            elif "raw" in path[-5:]: 
                suffix = "raw"
            else: suffix = "error"
            pn_index = path.index("message/")+len("message/")
            pn = path[pn_index:path.index(suffix)-1]
            gn_index = path.index("group/")+len("group/")
            gn = path[gn_index:path.index("message/")-1]
            
            thisRecord = {
                "uri":uri,
                "suffix":suffix,
                "post_number":pn,
                "payload":json.loads(record.raw_stream.read())
            }
            records_array.append(thisRecord)

        print("Getting Unique Post IDs...")
        op_key = "post_number"
        msg_ids = []
        for i in records_array:
            msg_ids.append(i[op_key])
        
        print("Marrying records... (this step takes time)")
        posts = []
        for i in list(set(msg_ids)):
            entry = {
                "post_number":i,
                "topic_id":"",
                "info":"",
                "raw":""
            }
            for j in records_array:
                if i == j["post_number"]:
                    if j["suffix"] == "raw":
                        entry["raw"] = j["payload"]
                    elif j["suffix"] == "info":
                        entry["info"] = j["payload"]
            entry["topic_id"] = entry["raw"]["topicId"]
            posts.append(entry)
        print("Record marriage complete!")
        return posts
    
def getRoster(posts):
        roster = []
        print("Generating roster...")
        for post in posts:
            member = { 
                "userId":post["raw"]["userId"],
                "authorName":post["raw"]["authorName"],
                "posts":[]
            }
            if member not in roster:
                roster.append(member)
        for member in roster:
            for post in posts:
                if post["raw"]["userId"] == member["userId"]:
                    member["posts"].append(post["post_number"])
        print("Roster complete!")
        return roster

def main():
    input_path = "./assets/june2004throughfeb2006.warc"
    posts = ygWarcToJson(input_path)
    roster = getRoster(posts)
    
    with open("posts.json", "w") as outfile:
        outfile.write(json.dumps(posts, indent=4))
    size = os.path.getsize("posts.json")/(1024*1024)
    print(f"Saved posts.json - {size}MB")
    
    with open("roster.json", "w") as outfile:
        outfile.write(json.dumps(roster, indent=4))
    size = os.path.getsize("roster.json")/(1024*1024)
    print(f"Saved roster.json - {size}MB")
    
    print("Operation complete :~)")
            
main()  
