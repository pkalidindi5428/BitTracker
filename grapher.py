import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pymongo import MongoClient


# Mongo DB
client = MongoClient()
db = client["cryto_trading_bot"]

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple())) - 18000

def get_twitter_dataset(start, end):

    tweets = db.bitcoin_sentiment.find(
            {}
            )

    df = pd.DataFrame(
            list(tweets)
            )

    df = df.set_index('created')

    compound = df['s_compound']
    compound = compound.resample("5T").mean().fillna(0)

    return compound


def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    twitter_ds = get_twitter_dataset(start, end)


    if (not twitter_ds.empty):
       ax1 = twitter_ds.plot(
                kind='line',
                color='blue')
       ax1.set_ylabel('Twitter Sentiment', color='b')
       ax2 = ax1.twinx()
       plt.show()
    else:
        print('Not enough data for that timeline')

if __name__ == '__main__':
   # if (len(sys.argv) != 3):
     #   print ("ERROR: Usage tweet_sentient.py <start date> <end date>")
    #else:
      #  main(sys.argv[1], sys.argv[2])
    main("2017-12-06 14:00:00", "2017-12-06 16:00:00")

