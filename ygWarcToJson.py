# Creates JSON file from WARC'd Yahoo Groups API response data.
# This should make the data easier to display dynamically on a webpage later. 
#
# Anthony D'Angelo http://heythats.cool
#

import urllib
from urllib.parse import urlparse
import json
import warcio
from warcio.archiveiterator import ArchiveIterator
         
def ygWarcToJson(input_path):
   
    with open(input_path, 'rb') as stream:
        
        records_array = []
        for record in ArchiveIterator(stream):

            # Parse the URI to get the group name, post number, 
            # and suffix. (Suffix should always be either "info" or "raw").
            uri = urlparse(record.rec_headers.get_header('WARC-Target-URI'))
            path = uri.path
            
            gn_index = path.index("group/")+len("group/")
            pn_index = path.index("message/")+len("message/")
            gn = path[gn_index:path.index("message/")-1]
            
            path = path.replace(gn,"")
            pn_index = path.index("message/")+len("message/")
            
            if "info" in path: 
                suffix = "info"
            elif "raw" in path:
                suffix = "raw"
            else: suffix = "error"
            pn = path[pn_index:path.index(suffix)-1]
            
            thisRecord = {
                "uri":uri,
                "suffix":suffix,
                "post_number":pn,
                "payload":json.loads(record.raw_stream.read())
            }
            records_array.append(thisRecord)

        # Make an array of the unique post numbers.
        op_key = "post_number"
        res = []
        for i in records_array:
            res.append(i[op_key])
        msg_ids = list(set(res))
        
        # Make an array of all posts: their ID, info payload, and raw payload.
        posts = []
        for i in msg_ids:
            entry = {
                "post_number":i,
                "info":"",
                "raw":""
            }
            for j in records_array:
                if i == j["post_number"]:
                    if j["suffix"] == "raw":
                        entry["raw"] = j["payload"]
                    elif j["suffix"] == "info":
                        entry["info"] = j["payload"]
            posts.append(entry)
            print("item added: " entry["post_number"])

        return posts


def main():

    input_path = "path/to/file.warc"
    output_filename = "archive.json"

    posts = ygWarcToJson(input_path)

    with open(output_filename, "w") as outfile:
        outfile.write(json.dumps(posts, indent=4))
   

            
main()      
    
    
