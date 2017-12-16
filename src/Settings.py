#
# Settings.py
# This file has most of the site-specific variables.  Modify these to get things
# working with your site.
#

class Settings(object):

    # Root of website. Contains src/ posts/ static/ img/, etc.
    webRoot = "/home/ec2-user/kinda-private/"

    # Name of the website.
    siteName = "My Internet Weblog"
    
    # Slogan.
    slogan = "...brought to you by Carl's Jr."
    
    # Twitter URL.
    twitterUrl = "https://twitter.com/AnotherBlogTwit"
    
    # Number of related articles to show.
    relatedArticleListSize = 5
    
    # Number of characters per article to show on homepage.
    # There will be trouble if this is shorter than a metadata entry.
    indexSummarySize = 400
    
    
