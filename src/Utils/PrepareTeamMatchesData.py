import pandas as pd
import os
import openpyxl

#struct for team match data
class TeamMatchData:
    def __init__(self, away_team, date):
        self.away_team = away_team
        self.date = date

    #serialize as json
    def serializeToDataframe(self):
        temp = {
            'date': self.date,
            'away_team': self.away_team
        }
        return pd.DataFrame(temp,index=['date'])

    # deserialize the data
    def deserialize(self, data):
        self.away_team = data['away_team']
        self.date = data['date']


def divideDataIntoTeams():

    # mycwd = os.getcwd()
    # os.chdir("../")
    # os.chdir("../")
    # os.chdir("Datasets/")
    # do stuff in parent directory

    fileDir = 'DataSets/TeamMatches/'

    # check directory exist or not
    if not os.path.isdir(fileDir):
        os.mkdir(fileDir)
    else:
        #remove all files in the directory
        for file in os.listdir(fileDir):
            os.remove(os.path.join(fileDir, file))


    #read excel files sequentially in the directory Team-Data/2022-23
    # convention '/' + '{}-{}-{}'.format(str(int(x[1])), str(int(x[2])), season1) + '.xlsx'


    df = pd.read_excel('Datasets/DataSet-2021-22.xlsx', header=0, usecols=['TEAM_NAME', 'TEAM_NAME.1', 'Date'],
                         index_col='Date')

    #iterate through the rows
    for row in df.itertuples():

        # get the team name and check if the file exist
        home_team = row[1]
        away_team = row[2]
        date = row.Index

        # print(home_team)
        # print(away_team)
        # print(date)

        homeTeamMatchData = TeamMatchData(away_team, date)
        awayTeamMatchData = TeamMatchData(home_team, date)

        # create the filename in the DataSets folder
        filename_home = home_team + '.xlsx'
        filename_away = away_team + '.xlsx'
        write_team_data(fileDir,filename_home, homeTeamMatchData)
        write_team_data(fileDir,filename_away, awayTeamMatchData)


#method to write team data into excel file
def write_team_data(fileDir,fileName, teamMatchData):

    #check file exist or not
    file = os.path.join(fileDir,fileName)

    dataRow = teamMatchData.serializeToDataframe()


    try:
        # Try to read the file, if it doesn't exist it will raise an error
        df = pd.read_excel(file)
        df = pd.concat([pd.DataFrame(df),dataRow])
    except FileNotFoundError:
        # If the file doesn't exist, create it and write the data
        df = pd.DataFrame(dataRow)


    #writer.book = openpyxl.load_workbook(file)
    df.to_excel(file, sheet_name='MatchesSheet', index=False, header=True)
    #writer.save()

    #os.chdir(mycwd)
