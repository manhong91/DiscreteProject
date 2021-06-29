import pandas as pd
import numpy as np

def get_average_goals(index, teamName, df, year):
    # select data for <teamName> and <year> only
    isTeamName_home = df['HomeTeamName'] == teamName
    isTeamName_away = df['AwayTeamName'] == teamName
    isYear = df['Year'] == year
    
    home = df[:index][isTeamName_home & isYear]['HomeTeamGoals']
    away = df[:index][isTeamName_away & isYear]['AwayTeamGoals']
    
    # calculate average goals
    both_home_away = pd.concat([home, away])
    av_decimal = np.mean(both_home_away)
    if av_decimal < 0.9:
        return 'Low'
    elif av_decimal < 1.5:
        return 'Mid'
    elif av_decimal >= 1.5:
        return 'High'
    else:
        return 'NoGamePlayed'
    
def last5game(index, teamName, dataFrame, year):
    
    numberOfLastGames = 0
    won_lost_count = 0
    
    while numberOfLastGames != 5:
        if index == 0:
            break
        
        index -= 1 # go up to previous row
        row = dataFrame.loc[index]
        
        # Break if year is different 
        # Because we are going upward and 
        # the data frame is sorted by year.
        if  row['Year'] != year:
            break
        
        # teamName is in HomeTeamName
        if(row['HomeTeamName'] == teamName):
            if row['Result'] == 'Won':
                won_lost_count += 1
                numberOfLastGames += 1
            elif row['Result'] == 'Lost':
                won_lost_count -= 1
                numberOfLastGames +=1
            else:
                numberOfLastGames +=1
        
        # teamName is in AwayTeamName
        elif (row['AwayTeamName'] == teamName):
            if row['Result'] == 'Lost':
                won_lost_count += 1
                numberOfLastGames += 1
            elif row['Result'] == 'Won':
                won_lost_count -= 1
                numberOfLastGames +=1
            else:
                numberOfLastGames +=1
    
    if won_lost_count > 0:
        return 'Good'
    elif won_lost_count == 0:
        return 'Neutral'
    else:
        return 'Bad'
    
    
def countResult(name, df):
    won_count = 0
    lost_count = 0
    draw_count = 0
    for index, row in df.iterrows():
        if name in row['HomeTeamName']:
            if row['Result'] == 'Won':
                won_count += 1
            elif row['Result'] == 'Lost':
                lost_count += 1
            else:
                draw_count += 1
        elif name in row['AwayTeamName']:
            if row['Result'] == 'Lost':
                won_count += 1
            elif row['Result'] == 'Won':
                lost_count += 1
            else:
                draw_count += 1
    return won_count, lost_count, draw_count

def getResultAllTeam(df):
    # convert HomeTeamName and AwayTeamName to set to remove all duplicated names
    allTeamNames = list(df['HomeTeamName'])
    allTeamNames.extend(list(df['AwayTeamName']))
    allTeamNames = list(set(allTeamNames))
    
    # get results for each TeamName
    resultAllTeams = {}
    for name in allTeamNames:
        results = countResult(name, df)
        resultAllTeams[name] = results
        
    # rename columns    
    resultsDf = pd.DataFrame.from_dict(resultAllTeams, 'index')
    resultsDf = resultsDf.rename(columns={0: 'Won', 1: 'Lost', 2: 'Draw' })
    
    return resultsDf