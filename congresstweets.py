import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import datetime

data = pd.read_csv("/Users/ishaanbakhle/Desktop/Projects/MemberStatements/memberTwitter/MemberHandles.csv")
handles = list(data["Handle"])
handles


url_list = []
for i in handles:
    url_list.append("https://www.twitter.com/" + i)


def getSource(url):
    browser = webdriver.Chrome("/Applications/chromedriver")
    browser.get(url)

    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(.5)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    source_data = browser.page_source
    soup = bs(source_data, "lxml")

    return((soup.body))



user_ids = []
user_screen_names = []
user_names = []
date_spans = []
tweet_text = []
like_spans = []
reply_spans = []
retweet_spans = []

for i in url_list:
    source = getSource(i)
    tweet_data = source.find_all("li", class_='js-stream-item')

    for li in tweet_data:
    # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
            if 'data-item-id' not in li.attrs:
                continue

            else:
                # tweet = {
                #     'tweet_id': li['data-item-id'],
                #     'text': None,
                #     'user_id': None,
                #     'user_screen_name': None,
                #     'user_name': None,
                #     'created_at': None,
                #     'retweets': 0,
                #     'likes': 0,
                #     'replies': 0
                # }

                # Tweet Text
                text_p = li.find("p", class_="tweet-text")
                if text_p is not None:
                    tweet_text.append(text_p.get_text())

                # Tweet User ID, User Screen Name, User Name
                user_details_div = li.find("div", class_="tweet")
                if user_details_div is not None:
                    user_ids.append(user_details_div['data-user-id'])
                    user_screen_names.append(user_details_div['data-screen-name'])
                    user_names.append(user_details_div['data-name'])

                # Tweet date
                date_span = li.find("span", class_="_timestamp")
                if date_span is not None:
                    date_spans.append(((float(date_span['data-time-ms']))))

                # Tweet Retweets
                retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
                if retweet_span is not None and len(retweet_span) > 0:
                     retweet_spans.append(int(retweet_span[0]['data-tweet-stat-count']))

                # Tweet Likes
                like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
                if like_span is not None and len(like_span) > 0:
                    like_spans.append(int(like_span[0]['data-tweet-stat-count']))

                # Tweet Replies
                reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
                if reply_span is not None and len(reply_span) > 0:
                    reply_spans.append(int(reply_span[0]['data-tweet-stat-count']))



dict = {"User ID":user_ids, "Screen Name":user_screen_names, "Username":user_names, "Date Span":date_spans, "Tweet Text":tweet_text, "Like Span":like_spans, "Reply Spans":reply_spans, "Retweet Spans":retweet_spans}


results_df = pd.DataFrame(dict)

# results_df.to_excel("crawl_1.xlsx")
