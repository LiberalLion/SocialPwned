#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, re
from core.colors import colors
from lib.TwitterAPI import Twitter


def getTweetEmailsFromHashtag(query,limit,year,since,until):
    print(
        f"{colors.good} Emails will be searched in the tweets of the hashtag #{query}{colors.end}"
    )
    results = []
    tweets = Twitter.getTweets(hashtags=True,limit=limit,search=query,year=year,until=until,since=since)
    return getEmailsFromTweets(tweets)

def getUserTweetsWithEmails(username,limit,year,since,until,profile_full,all_tw):
    Twitter.getUserInformation(username)
    print(
        f"{colors.good} User {username}'s tweets will be searched for emails{colors.end}"
    )
    results = []
    tweets = Twitter.getTweets(username=username,limit=limit,year=year,since=since,until=until,profile_full=profile_full,all_tweets=all_tw)
    return getEmailsFromTweets(tweets)

def getTweetEmailsFromListOfUsers(users,limit,year,since,until,profile_full,all_tw):

    results = []
    print(
        f"{colors.good} Emails will be searched in the Tweets of {len(users)} users :) {colors.end}"
    )
    for user in users:
        results.extend(getUserTweetsWithEmails(user,limit,year,since,until,profile_full,all_tw))

    return results

def getUserInformation(username):
    Twitter.getUserInformation(username)

def getFollowers(username,limit):
    print(f"{colors.good} Getting followers of the user: {username}{colors.end}")
    return Twitter.getFollowers(username,limit)

def getFollowings(username,limit):
    print(f"{colors.good} Getting followings of the user: {username}{colors.end}")
    return Twitter.getFollowers(username,limit)




def getEmailsFromTweets(tweets):
    results = []

    for tweet in tweets:
        user = tweet.get("username")
        userID = str(tweet.get("user_id"))
        if email := findEmail(tweet.get("tweet").split(" ")):
            results.append(json.dumps({"user":user,"userID":userID,"email":email}))
            print(
                f"{colors.good} Username: {colors.W}{user}{colors.B} UserID: {colors.W}{userID}{colors.B} Email: {colors.W}{email}{colors.end}"
            )

    return list(set(results))

def findEmail(tweet):
    for word in tweet:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',word):
            return word