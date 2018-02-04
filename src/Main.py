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
    '/',                    'Index',              
    "/posts/(.+)",          'SinglePost',
    "/style/(.+)",          'Style',
    "/img/(.+)",            'Image',
    "/static-html/(.+)",    'StaticHtml',
    "/static-md/(.+)",      'StaticMd',    
)

# Debug flag.
web.config.debug = True

# Load templates directory.
render = web.template.render(Settings.Settings.webRoot + '/templates')


def Setup404Handler(app):
    """
    Add the 404 handler/template.
	TODO: doesn't seem to work quite right.
    
    @param app: The web.py application.
    """
    
    # Handler function.
    def Do404Template():
        return render.NotFound()

    # Set the app's function.
    web.notfound = Do404Template

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
        for postDate, post in allMeta["byDate"].iteritems():
        
            # Create entry in summary dictionary.
            summaryList.append( {
                "filename"  : post,
                "title"     : allMeta["byTitle"][post],
                "date"      : postDate,
                "tags"      : ", ".join(allMeta["perPostTags"][post]),   # Just want a comma sep'd string for now.
                "summary"   : allMeta["summaries"][post]
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
            "content"   : mdHtmlData,
            "hasMath"	: '$' in mdHtmlData 
            }
        
        # Render final output in template.
        data = render.SinglePost(templateParams)
        
        # Done!
        return data

class StaticMd:
    """
    Delegate for static .md-based pages -- don't have any metadata info.
    """

    def GET(self, pageTitle):

        # Open the selected file. 
        with open(Settings.Settings.webRoot + "/static-md/" + pageTitle, 'r') as myfile:
            mdFileContents = myfile.read()
        
        # Create md HTML and meta from current post.
        mdHtmlData, myMeta = Functions.Functions.CreateMarkdownFromText(mdFileContents)
        
        # Create template paramters dictionary.
        templateParams = {
            "siteName"  : Settings.Settings.siteName,
            "slogan"    : Settings.Settings.slogan,
            "twitterUrl": Settings.Settings.twitterUrl,
            "title"     : myMeta["title"], 
            "content"   : mdHtmlData,
            "hasMath"	: '$' in mdHtmlData
            }
                        
        # Render final output in template.
        data = render.StaticPage(templateParams)
        return data

        
class StaticHtml:
    """
    Return the contents of an HTML webpage stored at /html/
    """
    def GET(self, stylesheetName):
        return Functions.Functions.ReadFile("/static-html/" + stylesheetName);

        
class Style:
    """
    Don't fully understand this, but this helps us support loading stylesheets from style/
    """
    def GET(self, stylesheetName):
        return Functions.Functions.ReadFile("/style/" + stylesheetName);


class Image:
    """
    Don't fully understand this, but this helps us support loading images from img/
    """
    def GET(self, imageName):
        return Functions.Functions.ReadFile("/img/" + imageName);           
            
            
# Entry point.
if __name__ == "__main__":

    # Create the app.
    app = web.application(urls, globals())
    
    # Add the 404 handler.
    Setup404Handler(app)
    
    # Run the server.
    app.run()

