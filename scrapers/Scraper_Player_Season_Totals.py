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
                   'catch_td', 'fumbles_total', 'fumbels_lost',
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

        # combine dfs
        if yr == years[0]:
            player_stats_annual = player_stats_annual_yr
        else:
            player_stats_annual = pd.concat(
                [player_stats_annual, player_stats_annual_yr], axis=0, join='outer')
    return player_stats_annual 

# Figure out how to wrap and apply in a function
# follow this structor
#cols = ['date1','date2']
#df[cols] = df[cols].apply(pd.to_datetime)

# Maybe: 
# df[cols] = df[cols].apply(lambda x: pd.to_numeric(player_fantsey_legacy_df.x, errors='coerce', downcast = 'integer').replace(np.nan, 0))

player_fantsey_legacy_df['twopoint_pass'] = pd.to_numeric(player_fantsey_legacy_df.twopoint_pass, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['catch_yds_per_att'] = pd.to_numeric(player_fantsey_legacy_df.catch_yds_per_att, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['twopoint_made'] = pd.to_numeric(player_fantsey_legacy_df.twopoint_made, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['rush_yds_per_att'] = pd.to_numeric(player_fantsey_legacy_df.rush_yds_per_att, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['vbd_points'] = pd.to_numeric(player_fantsey_legacy_df.vbd_points, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_target'] = pd.to_numeric(player_fantsey_legacy_df.pass_target, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['fumbles_total'] = pd.to_numeric(player_fantsey_legacy_df.fumbles_total, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['fantsey_points'] = pd.to_numeric(player_fantsey_legacy_df.fantsey_points, errors='coerce', downcast = 'integer').replace(np.nan, 0)

player_fantsey_legacy_df['games_played'] = pd.to_numeric(player_fantsey_legacy_df.games_played, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['games_started'] = pd.to_numeric(player_fantsey_legacy_df.games_started, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_completed'] = pd.to_numeric(player_fantsey_legacy_df.pass_completed, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_attempt'] = pd.to_numeric(player_fantsey_legacy_df.pass_attempt, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_yds'] = pd.to_numeric(player_fantsey_legacy_df.pass_yds, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_td'] = pd.to_numeric(player_fantsey_legacy_df.pass_td, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['rush_td'] = pd.to_numeric(player_fantsey_legacy_df.rush_td, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['pass_int'] = pd.to_numeric(player_fantsey_legacy_df.pass_int, errors='coerce', downcast = 'integer').replace(np.nan, 0)

player_fantsey_legacy_df['rush_att'] = pd.to_numeric(player_fantsey_legacy_df.rush_att, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['rush_yds'] = pd.to_numeric(player_fantsey_legacy_df.rush_yds, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['catches'] = pd.to_numeric(player_fantsey_legacy_df.catches, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['catch_yds'] = pd.to_numeric(player_fantsey_legacy_df.catch_yds, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['catch_td'] = pd.to_numeric(player_fantsey_legacy_df.catch_td, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['fumbles_lost'] = pd.to_numeric(player_fantsey_legacy_df.fumbels_lost, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['td_total'] = pd.to_numeric(player_fantsey_legacy_df.td_total, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['ppr_points'] = pd.to_numeric(player_fantsey_legacy_df.ppr_points, errors='coerce', downcast = 'integer').replace(np.nan, 0)

player_fantsey_legacy_df['draftking_points'] = pd.to_numeric(player_fantsey_legacy_df.draftking_points, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['fanduel_points'] = pd.to_numeric(player_fantsey_legacy_df.fanduel_points, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['rank_position'] = pd.to_numeric(player_fantsey_legacy_df.td_total, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['rank_total'] = pd.to_numeric(player_fantsey_legacy_df.rank_total, errors='coerce', downcast = 'integer').replace(np.nan, 0)
player_fantsey_legacy_df['age'] = pd.to_numeric(player_fantsey_legacy_df.age, errors='coerce', downcast = 'integer').replace(np.nan, 0)
