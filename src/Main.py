#
# Main.py
# Contains map and classes for web.py-based delegating.
#

# External imports.
import web
import markdown2
import time
import datetime
import pprint

# My imports.
import Functions
import Settings
import MetaOps

# URL map.
urls = (
    '/',            'Index',              
    "/posts/(.+)",  'SinglePost',
    "/style/(.+)",  'Style',
    "/(.+)",        'Static',
    
)

# Load templates directory.
render = web.template.render(Settings.Settings.webRoot + '/templates')

#
# Index class.
#
class Index:
    """
    Delegate for main page. Create a list of blurbs to pass to the MainPage template.
    """
    
    def GET(self):

        # Load metadata pickle.
        allMeta = MetaOps.MetaOps.LoadMetaData()
        
        # Create dictionary of file : post data to render.
        summaryList = []
        
        # Iterate through post files.
        for _, post in allMeta["byDate"].iteritems():
        
            # Load the file
            with open(Settings.Settings.webRoot + "/posts/" + post, 'r') as myfile:
                mdFileContents = myfile.read()
                
            # Create md HTML and meta from current post.
            mdHtmlData, myMeta = Functions.Functions.CreateMarkdownFromText(
                mdFileContents[:Settings.Settings.indexSummarySize] + 
                    (mdFileContents[Settings.Settings.indexSummarySize:] and '...'))
            
            # Create entry in summary dictionary.
            summaryList.append( {
                "filename"  : post,
                "title"     : myMeta["title"],
                "date"      : datetime.datetime.strptime(myMeta["date"], '%Y.%m.%d'),
                "tags"      : myMeta["tags"],
                "summary"   : mdHtmlData
                } )
                
        # Create template parameters.
        templateParams = {
            "siteName"  : Settings.Settings.siteName,
            "slogan"    : Settings.Settings.slogan,
            "blurbs"    : summaryList,
            "twitterUrl": Settings.Settings.twitterUrl
            }

        # Render final output in template.
        data = render.MainPage(templateParams)        
        return  data

class SinglePost:
    """
    Delegate for page with a single blog post.
    """

    def GET(self, postTitle):
    
        # Open the selected file. 
        with open(Settings.Settings.webRoot + "/posts/" + postTitle, 'r') as myfile:
            mdFileContents = myfile.read()
        
        # Load metadata pickle.
        allMeta = MetaOps.MetaOps.LoadMetaData()
        
        # Create md HTML and meta from current post.
        mdHtmlData, myMeta = Functions.Functions.CreateMarkdownFromText(mdFileContents)
        
        # Get my tags.
        myTags = [x.strip() for x in myMeta["tags"].split(',')] 
                
        # Create dictionary for related articles.
        relatedArticlesDict = Functions.Functions.GetRelatedPostsByTag(allMeta, myTags)

        # Create template paramters dictionary.
        templateParams = {
            "siteName"  : Settings.Settings.siteName,
            "slogan"    : Settings.Settings.slogan,
            "twitterUrl": Settings.Settings.twitterUrl,
            "title"     : myMeta["title"],
            "date"      : datetime.datetime.strptime(myMeta["date"], '%Y.%m.%d'),
            "tags"      : ', '.join(myTags),
            "related"   : relatedArticlesDict,
            "content"   : mdHtmlData
            }
        
        # Render final output in template.
        data = render.SinglePost(templateParams)
        
        # Done!
        return data

class Static:
    """
    Delegate for static pages -- still use md format, but don't have any metadata info, I guess.
    We may consider removing this and just supporting dropping your own .html pages in static/
    instead.    
    """

    def GET(self, pageTitle):

        # Open the selected file. 
        with open(Settings.Settings.webRoot + "/static/" + pageTitle, 'r') as myfile:
            mdFileContents = myfile.read()
        
        # Create md HTML and meta from current post.
        mdHtmlData, myMeta = Functions.Functions.CreateMarkdownFromText(mdFileContents)
        
        # Create template paramters dictionary.
        templateParams = {
            "siteName"  : Settings.Settings.siteName,
            "slogan"    : Settings.Settings.slogan,
            "twitterUrl": Settings.Settings.twitterUrl,
            "title"     : myMeta["title"], 
            "content"   : mdHtmlData
            }
                        
        # Render final output in template.
        data = render.StaticPage(templateParams)
        return data

class Style:
    """
    Don't fully understand this, but this helps us support loading stylesheets from style/
    """
    def GET(self, stylesheetName):

        # Just return the text of the .css file. 
        with open(Settings.Settings.webRoot + "/style/" + stylesheetName, 'r') as myfile:
            return myfile.read()

            
# Entry point.
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
