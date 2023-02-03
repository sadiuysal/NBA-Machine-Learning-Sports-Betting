import tweepy
from textblob import TextBlob
import pandas as pd
import os
import time
import datetime
import pytz


#sentimentData struct
class SentimentData:
    def __init__(self, team, date, positive, negative, neutral):
        self.team = team
        self.date = date
        self.positive = positive
        self.negative = negative
        self.neutral = neutral

    #serialize as json
    def serializeToDataframe(self):
        temp = {
            'team': self.team,
            'date': self.date,
            'positive': self.positive,
            'negative': self.negative,
            'neutral': self.neutral
        }
        return pd.DataFrame(temp)

    # deserialize the data
    def deserialize(self, data):
        self.team = data['team']
        self.date = data['date']
        self.positive = data['positive']
        self.negative = data['negative']
        self.neutral = data['neutral']









def queryTweets():
    twitterAPI = getAPI()

    # read excel's rows after 14505 included
    data = pd.read_excel('Datasets/DataSet-2021-22.xlsx', header=0, usecols=['TEAM_NAME', 'TEAM_NAME.1', 'Date'],
                         index_col='Date', skiprows=lambda x: x != 0 and x < 18800)
    # print(data.columns.tolist())

    # get after 18005. row included
    # data = data[18800:]

    # , skiprows=lambda x: x == 0 or x < 18500  , usecols= "TEAM_NAME,TEAM_NAME.1,Date"
    # get after 14505. row included
    # data = data[14505:]
    # print data dimensions
    print(data.shape)
    # print(data.get('TEAM_NAME'))
    # print(data)

    # for every row in the dataset
    for row in data.itertuples():
        # print the row's index
        # print(row.Index)

        # get team names, and date
        home_team = row[1]
        away_team = row[2]
        date = row.Index
        # get the twitter data for the home team
        home_sentiments = get_tweets_sentiments(home_team, date, 10, twitterAPI)

        write_sentiment_data(home_sentiments)

        time.sleep(10)

        # get the twitter data for the away team
        away_sentiments = get_tweets_sentiments(away_team, date, 10, twitterAPI)
        # print sentiments in one line
        print("Sentiments: " + home_sentiments + " &&& " + away_sentiments)
        write_sentiment_data(away_sentiments)

        # slepp for 30 seconds
        time.sleep(10)


#convert date to timestamp


def convert_to_ISO8601(date_str,hour=0,minute=0,second=0):
    # Parse the input string into a datetime object
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    # Add the time information
    dt = dt.replace(hour=hour, minute=minute, second=second)
    # Convert to the UTC timezone
    utc = pytz.UTC
    dt = utc.localize(dt)
    # Format the datetime object as ISO 8601/RFC 3339
    return dt.isoformat()

##Get tweets before given date and team name in given amount
def get_tweets_sentiments(team, date, amount,api):

    #tweets = tweepy.Cursor(api.search, q=team, until=date).items(amount)
    #find until date and since date
    until_date = convert_to_ISO8601(date, hour=0, minute=0, second=0)
    since_date = convert_to_ISO8601(date, hour=3, minute=0, second=0)



    #TODOOOOOOOOOOO

    tweets = api.search_recent_tweets(query=team, max_results=amount, end_time=until_date,start_time=since_date)

    #return tweets

    # Search for tweets about the Warriors
    #  warriors_tweets = tweepy.Cursor(api.search, q='#Nets').items(100)

    # Perform sentiment analysis on tweets
    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            positive_tweets += 1
        elif analysis.sentiment.polarity < 0:
            negative_tweets += 1
        else:
            neutral_tweets += 1

    return SentimentData(team, date, positive_tweets, negative_tweets, neutral_tweets)

#method to write sentiment analysis data into excel file
def write_sentiment_data(sentimentData):

    # write the statistics as columns into excel data with the date and team name
    # create a new excel file for team if not exist
    # if exist, append the data to the end of the file

    #get the team name and check if the file exist
    team = sentimentData.team
    #create the filename in the DataSets folder
    filename = '../../Datasets/Sentiments/' + team + '.xlsx'



    dataRow = sentimentData.serializeToDataframe()
    if os.path.isfile(filename):
        #append the data to the end of the file
        writer = pd.ExcelWriter(filename, engine='openpyxl', mode='a')
        dataRow.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
        writer.save()
    else:
        #create a new excel file
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        dataRow.to_excel(writer, sheet_name='Sheet1', index=False, header=True)
        writer.save()
        print('File created for team: ' + team)

#method to get the twitter api
def getAPI():
    # Authenticate with Twitter API
    consumer_key = '5ajvt2waupJv1pjywW33aAEtA'
    consumer_secret = 'fF3bWLlowjydyc4sfyqCAjTjkGw3zJfGWZsu9qhEWwABx5dUIa'
    access_token = '597743062-sGXg8mSdIy6aih77ueIZGwSU2TgY9EuUDsL6U1Rt'
    access_token_secret = 'CLEtsJCpxlC5znS07u5k1iA4aRqNkh2v66kyTHOnlUHCY'
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAETHlQEAAAAAgJ7xT4oTnFgjZ%2BiEki4LIn%2Bncfg%3DUpavEhw7CZAXZtqIknAUlbOmFqDueIlfoQCCWtB09LIXCO4HBp'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    return tweepy.Client(bearer_token,consumer_key, consumer_secret, access_token, access_token_secret)
    #return tweepy.API(auth)