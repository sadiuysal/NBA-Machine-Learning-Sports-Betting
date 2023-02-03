from src.DataProviders.TwitterDataProvider import queryTweets
import pandas as pd
import time
from src.Utils.PrepareTeamMatchesData import divideDataIntoTeams


#divideDataIntoTeams()


#queryTweets()

data = pd.read_excel('Datasets/DataSet-2021-22.xlsx')
data_new = pd.read_excel('Datasets/2022-2023.xlsx')
# data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU', 'OU-Cover'], axis=1, inplace=True)
# data_new.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU', 'OU-Cover'], axis=1, inplace=True)

#concat
data = pd.concat([data, data_new], ignore_index=True)
#Need to add odds to the new data



# remove last len(data_new) from data rows
#data = data[:-len(data_new)]

#save to excel
data.to_excel('Datasets/DataSet-2021-22.xlsx', index=False)






#margin = data['Home-Team-Win']
#data.drop(['Score', 'Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'],
          #axis=1, inplace=True)

#data = data.values

#data = data.astype(float)






