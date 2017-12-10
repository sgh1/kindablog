#
# MetaOps.py
# Operations for regenerating / loading metadata.  Loading is done as needed, but regenerating must
# be performed manually and periodically.  To do that, do python MetaOps.py
#


# Imports.
import collections
import os
import pickle
import pprint
import markdown2
import time
import datetime

import Settings

class MetaOps(object):

    @staticmethod
    def RegenerateMetaData():
        """
        Updates metadata pickle for fast access to post meta-data.  The goal is to avoid 
        reading all the .md files in full every time we want to do some operation that requires
        all the metadata.
        """

        # Get the posts.
        posts = os.listdir(Settings.Settings.webRoot + "/posts/")     
        
        # Create meta data dictionary.
        metaInfo = {}
        
        # Grouped by tag.  Key is tag, value is list of post md files with tag.
        metaInfo["byTag"] = {}
        
        # Title/filename map. Key is filename, value is post title.
        metaInfo["byTitle"] = {}
        
        # Sorted by date. Value is list of all articles sorted by date.
        metaInfo["byDate"] = {}
            
        # Collect the data.
        for postFile in posts:
        
            # Open the selected file. 
            with open(Settings.Settings.webRoot + "/posts/" + postFile, 'r') as myfile:

                # Create markdown.
                markedDownText = markdown2.markdown(myfile.read(), extras=["fenced-code-blocks", "metadata"])

                # Get meta info.
                meta = markedDownText.metadata
                
                # Add title map entry.
                metaInfo["byTitle"][postFile] = meta["title"]
                
                # Get list of tags.
                tags = [x.strip() for x in meta["tags"].split(',')]
                
                # Add to tag lists.
                for tag in tags:
                    metaInfo["byTag"].setdefault(tag, [])
                    metaInfo["byTag"][tag].append(postFile)
                
                # The date is . separated in Y.M.D format.
                dt = datetime.datetime.strptime(meta["date"], '%Y.%m.%d')
                
                # Pretty severe limitation since we use dates as keys, we can't do two posts
                # created on the same day.  Warn about it for now.
                if dt in metaInfo["byDate"]:
                    print "WARNING: already have a post with this date.  The old one will not be in the by-date meta dictionary."
                    
                # Add it.
                metaInfo["byDate"][datetime.datetime.strptime(meta["date"], '%Y.%m.%d')] = postFile
                
        
        # Store the by-date information as a stored dictionary.
        #metaInfo["byDate"] = collections.OrderedDict(sorted(metaInfo["byDate"].items()))
        # Can't pickle an ordered dict? We will have to sort when we retrieve.
        
        # Print the meta data for use inspection.   
        pprint.pprint(metaInfo)         
        
        # Create the pickle.
        with open(Settings.Settings.webRoot + "/meta/meta.pickle", 'wb') as handle:
            pickle.dump(metaInfo, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Test the pickle.
        with open(Settings.Settings.webRoot + "/meta/meta.pickle", 'rb') as handle:
            b = pickle.load(handle)
        
        # Print the meta data for use inspection.   
        pprint.pprint(b)         
          
    @staticmethod
    def LoadMetaData():
        """
        Updates metadata pickle for fast access to post meta-data.  The goal is to avoid 
        reading all the .md files in full every time we want to do some operation that requires
        all the metadata.
        """
        
        # Test the pickle.
        with open(Settings.Settings.webRoot + "/meta/meta.pickle", 'rb') as handle:
            metaInfo = pickle.load(handle)

        # Sort the by-date entries.
        metaInfo["byDate"] = collections.OrderedDict(sorted(metaInfo["byDate"].items(), reverse=True))
        
        return metaInfo 
    
            
# Entry point.
if __name__ == "__main__":
    MetaOps.RegenerateMetaData()
