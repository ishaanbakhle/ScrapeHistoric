import pandas as pd
import numpy as np



handle_data = pd.read_csv("/Users/ishaanbakhle/Desktop/Projects/MemberStatements/memberTwitter/MemberHandles.csv")
tweet_data = pd.read_excel("/Users/ishaanbakhle/Desktop/crawl_1.xlsx")
handles_list = list(handle_data["Handle"])
tweet_data

tweet_bodies = list(tweet_data["Tweet Text"])


def dfsearch(term, dataframe, get_rts = False):
    boolean_list = []
    if get_rts == False:
        for i in list(tweet_data["Tweet Text"]):
            if (term.lower() in str(i).lower()):
                boolean_list.append(True)
            else:
                boolean_list.append(False)
    elif get_rts == True:
        for i in np.arange(0,413832+1,1):
            if t
    return(dataframe[boolean_list])
