#
# Functions.py
# Some helper functions to keep clutter out of Main.py.
#

# Imports
import Settings
import markdown2
from markdown2Mathjax import sanitizeInput, reconstructMath
import pprint

class Functions(object):

    @staticmethod
    def GetRelatedPostsByTag(allMetaDataDict, tags):
        """
        Get related posts by tags.
        
        @param allMetaDataDict: Meta data from the meta pickle.
        @param tags: Dictionary of tags for which we want related articles.
        @return: Dictionary of filenames : titles of related articles.
        """
        
        pprint.pprint(tags)
        
        # Create dictionary for related articles.
        relatedArticlesDict = {}
        
        # Get related articles from meta data.
        for tag in tags:
        
            print "tag: " + tag
        
            # See if the tag is in the meta data.  In theory there should be at least 'this' article, but 
            # we don't explicitly enforce updating the meta info, so it might not be.
            if tag in allMetaDataDict["byTag"]:
            
                # Create filename / title entry in dictionary
                for relatedArticle in allMetaDataDict["byTag"][tag]:
                    print "adding: " + relatedArticle 
                    relatedArticlesDict[relatedArticle] = allMetaDataDict["byTitle"][relatedArticle] 
        
                    # Break if we have enough related articles.
                    if len(relatedArticlesDict) >= Settings.Settings.relatedArticleListSize:
                        break 

            # Break if we have enough related articles.
            if len(relatedArticlesDict) >= Settings.Settings.relatedArticleListSize:
                break
                
        return relatedArticlesDict
                
    @staticmethod
    def CreateMarkdownFromText(text):
        """
        Create markdown from raw text that was read from file.
        
        @param text: Raw text from .md file.
        @return: HTML string containing processed markdown text, and metadata from .md file.
        """
        
        # Do mathjax sanitizeInput idiom. 
        # Note, this seems broken, so it is worthless right now.
        tmp = sanitizeInput(text)

        # Create markdown.
        markedDownText = markdown2.markdown(tmp[0], extras=["fenced-code-blocks", "metadata"])

        # Load just this post's meta data.
        myMeta = markedDownText.metadata
        
        # Create final output ... md + mathjax.
        finalOutput = reconstructMath(markedDownText,tmp[1])
        
        return (finalOutput, myMeta)
        
    
