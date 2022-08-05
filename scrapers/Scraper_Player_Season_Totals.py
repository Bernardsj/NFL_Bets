# To Do:
# 1. Add ability to import next seasons data to MySQL Database following end of season
# 2. Set up automatic run at end of season
# 3. Update col function at bottom

# Script is designed to scrape player level data following each season.
# * Based on https://github.com/pvicks585/NFL-WebScrape/blob/main/Webscraping%20NFL%20Player%20Data.ipynb

# author: Jake Bernards

# Import library
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def player_legacy(years):

    for yr in years:
        # set up soup
        # string formatting to manipulate the url by a given year
        url = f"https://www.pro-football-reference.com/years/{yr}/fantasy.htm"
        html = urlopen(url)
        soup = BeautifulSoup(html, features='html.parser')

        # define headers
        headers = ['player', 'team_code', 'fantasy_position',
                   'age', 'games_played', 'games_started',
                   'pass_completed', 'pass_attempt', 'pass_yds',
                   'pass_td', 'pass_int', 'rush_att', 'rush_yds',
                   'rush_yds_per_att', 'rush_td', 'pass_target',
                   'catches', 'catch_yds', 'catch_yds_per_att',
                   'catch_td', 'fumbles_total', 'fumbles_lost',
                   'td_total', 'twopoint_made', 'twopoint_pass',
                   'fantsey_points', 'ppr_points', 'draftking_points',
                   'fanduel_points', 'vbd_points', 'rank_position',
                   'rank_total']

        # extract data
        # Here we grab all rows that are not classed as table header rows - football reference throws in a table header row everyy 30 rows
        rows = soup.findAll(
            'tr', class_=lambda table_rows: table_rows != "thead")
        player_stats = [[td.getText() for td in rows[i].findAll('td')]  # get the table data cell text from each table data cell
                        for i in range(len(rows))]  # for each row
        player_stats = player_stats[2:]

        # create df and remove season award characters (* or +)
        player_stats_annual_yr = pd.DataFrame(player_stats, columns=headers)
        player_stats_annual_yr['player'] = player_stats_annual_yr.player.str.replace(
            '+', "", regex=False).str.replace('*', "", regex=False)
        player_stats_annual_yr['year'] = yr

        # Update cols to push to mysqldb
        update_cols = ['age', 'games_played', 'games_started',
               'pass_completed', 'pass_attempt', 'pass_yds',
               'pass_td', 'pass_int', 'rush_att', 'rush_yds',
               'rush_yds_per_att', 'rush_td', 'pass_target',
               'catches', 'catch_yds', 'catch_yds_per_att',
               'catch_td', 'fumbles_total', 'fumbles_lost',
               'td_total', 'twopoint_made', 'twopoint_pass',
               'fantsey_points', 'ppr_points', 'draftking_points',
               'fanduel_points', 'vbd_points', 'rank_position',
                   'rank_total']

        player_stats_annual_yr[update_cols] = player_stats_annual_yr[update_cols].apply(lambda x: pd.to_numeric(x, errors='coerce', downcast = 'integer').replace(np.nan, 0))

        # combine dfs
        if yr == years[0]:
            player_stats_annual = player_stats_annual_yr
        else:
            player_stats_annual = pd.concat(
                [player_stats_annual, player_stats_annual_yr], axis=0, join='outer')

    return player_stats_annual 

