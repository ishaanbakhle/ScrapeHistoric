import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd

browser = webdriver.Chrome("/Applications/chromedriver")

# Tell Selenium to get the URL you're interested in.
browser.get("https://twitter.com/cspan/lists/members-of-congress/members")

# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

# Now that the page is fully scrolled, grab the source code.
source_data = browser.page_source
soup = bs(source_data, "lxml")
member_data = (soup.findAll("div", {"class": "account js-actionable-user js-profile-popup-actionable "}))
ex = str(member_data[10]).split("<div")

trial_col = []
for i in ex:
    trial_col.append(i)
a = pd.DataFrame({"Item":trial_col})
a
a["Item"][5].split("<div")

def parseMember(ht):
    item = str(ht).split("<div")[5]
    split_item = item.split("class")

    # Extract the full name
    # name = split_item[4].split(">")[1].split("<")[0]
    for i in split_item:
        if "username u-dir" in i:
            handle = i.split("<b>")[1].split("<")[0]
        if "fullname" in i:
            name = i.split(">")[1].split("<")[0]
    return([name,handle])


names = []
handles = []

for member in member_data:
    parsed = parseMember(member)
    names.append(parsed[0])
    handles.append(parsed[1])


dict = {"Name":names, "Handle":handles}
df = pd.DataFrame(dict)
df.to_csv("MemberHandles.csv")
