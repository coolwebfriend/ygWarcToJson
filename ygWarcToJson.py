#=============================================================================#
#=============================================================================#
#
#        Creates JSON file from WARC'd Yahoo Groups API response data.
#  This should make the data easier to display dynamically on a webpage later. 
#
#  Anthony D'Angelo | http://heythats.cool | https://github.com/coolwebfriend
#  Josh Gillner | https://github.com/jgillner
#
#
#=============================================================================#
#=============================================================================#

import os
import json
import html
import time

import urllib
from urllib.parse import urlparse

import email
from email import message, parser

import warcio
from warcio.archiveiterator import ArchiveIterator

from tqdm import tqdm


#=============================================================================#

def parse_records(stream):
    # Returns array of dicts containing data for next steps.
    print(f"Parsing WARC records...")
    
    records_array = []
    for record in tqdm (ArchiveIterator(stream)):
        
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
        
    print(f"Parsed {len(records_array)} records!")
    return records_array


#=============================================================================#

def marry_records(records_arr):
    #Returns list of dicts containing both "info" and "raw" metadata for each post
    
    print(f"Marrying {len(records_arr)} records... (this step can take some time)")

    unique_messages = list(set(map(lambda r: r["post_number"], records_arr)))

    married = []
    
    for msgId in tqdm (unique_messages):
        
        entry = {
            "post_number":msgId,
            "topic_id":"",
            "body":"",
            "info":"",
            "raw":""
        }
        
        for record in records_arr:
            if record["post_number"] == msgId:
                if record["suffix"] == "raw":
                    entry["raw"] = record["payload"]
                if record["suffix"] == "info":
                    entry["info"] = record["payload"]
                    
        entry["topic_id"] = entry["raw"]["topicId"]
        
        married.append(entry)
    
    for m in married:
        #Clean up the email blob
        email_blob = email.message_from_string(html.unescape(m["raw"]["rawEmail"]))
        
        if email_blob.is_multipart():
            # If the email is multipart, get the payload from the first part
            m["body"] = str(email_blob.get_payload()[0].get_payload())
        else:
            m["body"] = str(email_blob.get_payload())

    print(f"Marriage complete, made {len(married)} posts")
    
    return married

                    
#=============================================================================#

def get_roster(posts):
    
    print("Generating roster...")
    
    unique_author_tuples = list(set(map(lambda p: str(p["raw"]["userId"]) +\
                                        "~$$$~" + p["raw"]["authorName"], posts)))
    roster = []
    
    for author_tuple in tqdm (unique_author_tuples):
        
        userId = author_tuple.split("~$$$~")[0]
        authorName = author_tuple.split("~$$$~")[1]
        
        user_posts = list(set(filter(lambda p: p["raw"]["userId"] == userId and
                                                p["raw"]["authorName"] == authorName, posts)))
        
        user_post_ids = list(set(map(lambda p: p['post_number'], user_posts)))
        
        roster.append({ 
            "userId":userId,
            "authorName":authorName,
            "posts": user_post_ids
        })
 
    print("Roster complete!")
    
    return roster

  
#=============================================================================#
                    
def get_threads(posts):
    
    unique_topic_ids = list(set(map(lambda p: p["raw"]["topicId"], posts)))
    
    print(f"Generating {len(unique_topic_ids)} threads...")
    
    threads = []
    
    for tid in tqdm (unique_topic_ids):
        
        posts_in_thread = list(filter(lambda p: p["raw"]["topicId"] == tid, posts))
        
        threads.append({
            "topicId":int(tid),
            "postIds":posts_in_thread
        })
        
    return threads


#=============================================================================#
                  
def save_as_json(data,name):
    
    filename = f"{name}.json"
    
    with open(f"{filename}","w") as outfile:
        outfile.write(json.dumps(data, indent=4))
        
    size = round(os.path.getsize(f"{filename}")/(1024*1024), 2)
    
    print(f"Saved {filename} | Size: {size}MB")
    
        
#=============================================================================#
                  
def ygWarcToJson(input_path, export_posts, export_threads, export_roster):
    
    with open(input_path, 'rb') as stream:
        
        records = parse_records(stream)
        
        posts = marry_records(records)
        
        if export_posts == True:
            save_as_json(posts,"posts")
        if export_threads == True:
            save_as_json(get_threads(posts),"threads")
        if export_roster == True:
            save_as_json(get_roster(posts),"roster")
            
    print("Operation complete :~)")
    

#=============================================================================#
                  
def main():
    
    # Options
    input_path = "./videoblogging.warc"
    export_posts = True
    export_threads = True
    export_roster = True
    
    ygWarcToJson(input_path,export_posts,export_roster,export_threads)
    

 #=============================================================================#

main()
    

