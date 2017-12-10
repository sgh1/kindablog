# kindablog

## What?

This is a blogging platform like Drupal or Wordpress, but much less feature-rich, and perhaps not as scalable. kindablog is a home-brew CMS written in python (using web.py), and blog posts are in markdown.

## Why?

Immediately, I one day realized I had 1000s of spam Drupal users on my blog, and I got too scared to do the database operation (don't know much about that stuff) required to fix that situation.  I am also always up against my webhost's resource limits, even though I serve about 1000 pageviews/month.

More generally, Drupal felt like I was trying to power a lightbulb with a nuclear reactor.  I wanted something small enough that when something went wrong, I could figure it out.  Some of the features of bigger platforms like Drupal were probably lost on me as a small-time blogger.

Also, this was fun.  I'm sure there are solutions similar to this but better out there...oh well.

The markdown supports code highlighting, and the default templates include mathjax.

## How?

This CMS is based on web.py, so refer to http://webpy.org/ for more information.

Here's a procedure for getting kindablog functioning, but some details might depend on your system or requirements.

I'm starting from a raw Amazon EC2 nano instance with Amazon Linux.  The security rules must accept HTTP/TCP traffic on port 80.

* cd
* sudo yum install git
* sudo pip install markdown2, web.py, markdown2Mathjax
* git clone https://github.com/sgh1/kindablog.git
* cd kindablog
* vi src/Settings.py (and edit your webRoot to your current working directory and change other settings as needed).
* Next we have to generate some metadata from the posts, which is a manual process is kindablog.  This should be done everytime a new post is added.
* To update the metadata, python src/MetaOps.py
* To start the server, sudo python src/Main.py 80 (you can cat to file and tail or whatever you please.)
* You should be able to navigate to your blog now.
