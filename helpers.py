import numpy as np
import pandas as pd
import seaborn as sns
import sqlite3
conn = sqlite3.connect('database.sqlite')

"""
function team_names adds team names to dataframe based on team_id and has three arguments presented below
dataframe - dataframe
team_id_column - column with team_ids
team_column_name - how to name a column
"""
def team_names(dataframe, team_id_column, team_column_name):
    
    teams_df = pd.read_sql("SELECT team_api_id, team_long_name FROM team", conn, index_col = "team_api_id")
    
    dataframe = dataframe.merge(
        teams_df,
        left_on = team_id_column,
        right_index = True,
        how = "left"
    )
    dataframe = dataframe.rename(
        columns = {"team_long_name" : team_column_name}
    )
    return dataframe
        

def result(dataframe):
    conditions = [
        (dataframe["home_team_goal"] > dataframe["away_team_goal"]),
        (dataframe["home_team_goal"] < dataframe["away_team_goal"]),
        (dataframe["home_team_goal"] == dataframe["away_team_goal"])
    ]
    choices = ['home_win', 'away_win', 'draw']
    dataframe['result'] = np.select(conditions, choices, default='Unknown')
    return dataframe