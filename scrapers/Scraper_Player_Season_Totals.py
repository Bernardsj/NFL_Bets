# To Do:
# 1. Add ability to import next seasons data to MySQL Database following end of season
# 2. Set up automatic run at end of season

# Script is designed to scrape player level data following each season.
# * Based on https://github.com/pvicks585/NFL-WebScrape/blob/main/Webscraping%20NFL%20Player%20Data.ipynb

# author: Jake Bernards

# Import library
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def player_legacy(start_year, end_year):
    years = np.array(range(start_year, end_year))

    for yr in years:
        # set up soup
        # string formatting to manipulate the url by a given year
        url = f"https://www.pro-football-reference.com/years/{yr}/fantasy.htm"
        html = urlopen(url)
        soup = BeautifulSoup(html, features='html.parser')

        # define headers
        headers = ['Player', 'Team', 'FantasyPos',
                   'Age', 'Games_Played', 'Games_Started',
                   'Pass_Completed', 'Pass_Attempt', 'Pass_Yds',
                   'Pass_TD', 'Pass_Int', 'Rush_Att', 'Rush_Yds',
                   'Rush_Yds_Per_Att', 'Rush_TD', 'Pass_Target',
                   'Catch', 'Catch_Yds', 'Catch_Yds_Per_Att',
                   'Catch_TD', 'Fumbles_Total', 'Fumbels_Lost',
                   'TD_Total', 'TwoPoint_Made', 'TwoPoint_Pass',
                   'Fantsey_Points', 'PPR_Points', 'DraftKing_Points',
                   'FanDuel_Points', 'VBD_Points', 'Rank_Position',
                   'Rank_Total']

        # extract data
        # Here we grab all rows that are not classed as table header rows - football reference throws in a table header row everyy 30 rows
        rows = soup.findAll(
            'tr', class_=lambda table_rows: table_rows != "thead")
        player_stats = [[td.getText() for td in rows[i].findAll('td')]  # get the table data cell text from each table data cell
                        for i in range(len(rows))]  # for each row
        player_stats = player_stats[2:]

        # create df and remove season award characters (* or +)
        player_stats_annual_yr = pd.DataFrame(player_stats, columns=headers)
        player_stats_annual_yr['Player'] = player_stats_annual_yr.Player.str.replace(
            '+', "", regex=False).str.replace('*', "", regex=False)
        player_stats_annual_yr['Year'] = yr

        # combine dfs
        if yr == start_year:
            player_stats_annual = player_stats_annual_yr
        else:
            player_stats_annual = pd.concat(
                [player_stats_annual, player_stats_annual_yr], axis=0, join='outer')
    return player_stats_annual 