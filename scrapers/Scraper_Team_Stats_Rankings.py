# To Do:
# 2. Define loop to pull data from each team and each year
# author: Jake Bernards

# Install dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def game_scrapper(team_codes, years):
    for team in team_codes:
        for yr in years:
            try:
                # Pull up team/year web pages
                url = f"https://www.pro-football-reference.com/teams/{team}/{yr}/gamelog/"
                html = urlopen(url)
                soup = BeautifulSoup(html, features="lxml")
                tables = soup.find_all('table')  # create list of tables
                
                # Define headers
                game_log_headers = ['Week', 'Day', 'Date', 'boxscore', 'Win_Loss', 'OT', 'Home_Away', 'Opponent',
                                    'Points_Scored', 'Points_Allowed', 'Pass_Complete', 'Pass_Attempt',
                                    'Pass_Yds', 'Pass_TD', 'Pass_Int', 'Sacked', 'Sack_Yds', 'Yards_Per_Pass_Att',
                                    'Net_Yds_Per_Pass_Att', 'Completion_Pct', 'QB_Rating', 'Rush_Att',
                                    'Rush_Yds', 'Rush_Yds_Per_Att', 'Rush_TD', 'Field_Goal_Made', 'Field_Goal_Att',
                                    'Extra_Point_Made', 'Extra_Point_Att', 'Punt', 'Punt_Yds', '3rd_Down_Conv',
                                    '3rd_Down_Att', '4th_Down_Conv', '4th_Down_Att', 'Home_Time_of_possession_min']

                # extract data - Game Logs
                game_log = pd.read_html(str(tables), header=None)[0]

                # flatten multiindex
                game_log.reset_index(inplace=True, drop = True)

                # assign new headers
                game_log.columns = game_log_headers

                # define team and year
                game_log['Team'] = team
                game_log['Year'] = yr

                # set OT Coding
                game_log['OT'] = np.where(game_log.OT == 'OT', 1, 0)

                # set home_away
                game_log['Home_Away'] = np.where(
                    game_log.Home_Away == "@", "Away", "Home")

                # Convert time of possession to min
                game_log['Home_Time_of_possession_min'] = game_log.Home_Time_of_possession_min.apply(
                    lambda x: int(x[:-3]) * 60 + int(x[-2:]))

                # Drop unwanted boxscore
                game_log.drop(['boxscore'], axis = 1, inplace = True)
                
            except ValueError:
                print(f"Error scraping {team}: {yr}")

            else:
                # Create df is first call
                if all([yr == min(years), team == team_codes[0]]):
                    team_game_stats = game_log
                # combine dfs
                else:
                    team_game_stats = pd.concat(
                        [team_game_stats, game_log], axis=0, join='outer')

    return team_game_stats
