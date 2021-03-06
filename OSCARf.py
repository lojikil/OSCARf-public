#!/usr/bin/env python

#External libraries needed to use oscar:
#twitter
#tweepy
#feedparser
#shodan
#readline
#beautifulsoup

#oscar will automatically try to import first.
#On exception it will alert the user
import urllib2

try:
    urllib2.urlopen("https://google.com", timeout=10)
except urllib2.URLError:
    print "[+]ERROR: Could not detect an active internet connection.",
    print "An internet connection is required to use OSCAR-F"
    exit()

import csv
import sys
import json
import os
import time
import re

try:
    import readline
except:
    pass

#################
# LOCAL IMPORTS #
#################
from plugins import pyscrape
from plugins import linked
from plugins import ipinfo
from plugins import newsfeed
from plugins import fblookup
from plugins import oscrtwitter
from plugins import oshodan
from plugins import portlook
from plugins import instag
from plugins import webscrape
from plugins import asciis

asciis.asciiart()


#----Why 2 twitter libs?----#
#The auth for the twitter lib is nicer as it can create an auth file
#to read from. the twitter auth will also open a browser window where
# you will accept the app to use your twitter account. Read and Write
#is what it requires. When accepted, you will get a pin to enter into
# the application. You will not be prompted for a pin after getting a
#token.
#----END----#
#imports for the streaming lib

try:
    import tweepy
    from tweepy import *
    from tweepy.streaming import *
except:
    print "[+]ERROR: Unable to import the tweepy library installed!!"
    print "You will not be able to use the twitter collection side of oscar!"

#Twitter lib for AUTH
try:
    import twitter
    from twitter.oauth import write_token_file, read_token_file
    from twitter.oauth_dance import oauth_dance
except:
    print "[+]ERROR: Unable to import the twitter library installed!"
    print "You will not be able to use the twitter collection side of oscar!"


try:
    #Open file for twitter app auth
    tappfile = open('auth/'+'twitter_app.dat', 'r')
    tappline = tappfile.readlines()
    APP_NAME = tappline[1].rstrip()
    CONSUMER_KEY = tappline[3].rstrip()
    CONSUMER_SECRET = tappline[5].rstrip()
    tappfile.close()

    #file that Oauth data is stored
    TOKEN_FILE = 'auth/'+'token.txt'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(TOKEN_FILE)
    except IOError, e:
        print "Please run the TWITTERSETUP.py file to get the token file!"
        exit()

    t_auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    t_auth.set_access_token(oauth_token, oauth_token_secret)
    t_api = tweepy.API(t_auth)
except:
    t_auth = None
    t_api = None


def main():
    try:
        print """
        OSCAR (Open Source Collection And Recon) Framework
        (CTRL+C returns back to main menu)
        -------------
        1. Social Networking
        -------------
        2. Shodan
        -------------
        3. News
        -------------
        4. Network Info
        -------------
        5. Pastebin Scraper
        -------------
        6. Web Source File Scraper
        -------------

        0. Exit OSCAR
        """
        opt = raw_input("Enter an option: ")
        if opt == "1":
            socialMenu()
        elif opt == "2":
            oscrShodan()
            main()
        elif opt == "3":
            news()
        elif opt == "4":
            networkMod()
        elif opt == "5":
            pasteScrape()
        elif opt == "6":
            wscrape()
        elif opt == "0":
            print "Thanks for using OSCAR!"
            sys.exit(0)
        else:
            print "You entered an invalid option!"
            main()
    except (KeyboardInterrupt):
            main()


###########################
#-- Social Media Menu   --#
###########################
def socialMenu():
    print """
    1. Twitter
    2. FaceBook
    3. LinkedIn
    4. Check username on instagram
    0. Return
    """
    opt = raw_input("Enter an option: ")
    if opt == "1":
        twitMenu()
    elif opt == "2":
        fbMenu()
    elif opt == "3":
        linkedin()
    elif opt == "4":
        instachek()
    elif opt == "0":
        main()
    else:
        print "You entered an invalid choice!"
        socialMenu()


###########################
#-- Twitter Collection -- #
###########################


def twitMenu():
    if t_auth is None or t_api is None:
        print "Twitter is disabled; please install an API key for twitter"
        return
    print """
    1. Live stream twitter (saved as csv)
    2. Live stream NO LOGGING!
    3. Gather last X tweets from user
    4. View recent follows
    5. View recent followers
    6. Get count of mentions of another user (last 200 tweets)
    7. Search for tweet
    8. Add user to sqlite db
    0. Return
    """
    opt = raw_input("Enter an option: ")
    if opt == "1":
        oscrtwitter.lv_stream(t_auth)
    elif opt == "2":
        oscrtwitter.lv_streamno(t_auth)
    elif opt == "3":
        oscrtwitter.hist_tweet(t_api)
        twitMenu()
    elif opt == "4":
        oscrtwitter.rcntFllw(t_api)
        twitMenu()
    elif opt == "5":
        oscrtwitter.rcntFllwrs(t_api)
        twitMenu()
    elif opt == "6":
        oscrtwitter.mentionCount(t_api)
        twitMenu()
    elif opt == "7":
        oscrtwitter.twitSearch(t_api)
        twitMenu()
    elif opt == "8":
        oscrtwitter.twitlookup(t_api)
        twitMenu()
    elif opt == "0":
        main()
    else:
        print "[+]ERROR: You entered an invalid option!"
        twitMenu()


########################
## --- FB Analysis -- ##
########################

def fbMenu():
    print """
    1. Get user info - Raw JSON Dump/Not Formatted
    2. Get user info - Formatted, Lookup multiple users
    0. Return
    """
    opt = raw_input("Enter an input: ")
    if opt == "1":
        fblookup.FBInfo()
        fbMenu()
    elif opt == "2":
        fblookup.FBUsr()
        fbMenu()
    elif opt == "0":
        main()
    else:
        print "You entered an invalid option"
        fbMenu()


def instachek():
    usernom = raw_input("Enter username: ")
    instag.checker(usernom)
    socialMenu()

#############################
#-- News Feed Integration --#
#############################


def news():
    newsfeed.newsStart()
    main()


###############
#-- IP Info --#
###############
def ipInfo():
    ip = raw_input("Enter IP: ")
    ip = ip.rstrip()
    ipinfo.lookup(ip)
    networkMod()


def prtLook():
    portlook.lookup()
    networkMod()


def networkMod():
    print """
    1. Lookup IP Address
    2. Port Lookup (SANS website)
    0. Return
    """
    opt = raw_input('Enter an option: ')
    if opt == "1":
        ipInfo()
    elif opt == "2":
        prtLook()
    elif opt == "0":
        main()
    else:
        print "Invalid option!"
        networkMod()


######################
#- Pastebin Scraper -#
######################
def pasteScrape():
    try:
        pyscrape.starter()
    except KeyboardInterrupt:
        pyscrape.stopper()
        main()


def linkedin():
    linked.start()
    time.sleep(5)
    if linked.saveout:
        linked.dupr(linked.saveout)
    main()


def oscrShodan():
    oshodan.menu()
    main()


def wscrape():
    webscrape.scrape()
    main()

if __name__ == "__main__":
    # users may wish to import part of this...
    main()
