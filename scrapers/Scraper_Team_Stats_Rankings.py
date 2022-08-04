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
                url = f"https://www.pro-football-reference.com/teams/buf/2000/gamelog/"
                html = urlopen(url)
                soup = BeautifulSoup(html, features="lxml")
                tables = soup.find_all('table')  # create list of tables
                
                # Define headers
                game_log_headers = ['week', 'day_of_week', 'date', 'boxscore', 'win_loss', 'overtime', 'home_away', 'opponent',
                                    'points_scored', 'points_allowed', 'pass_complete', 'pass_attempt',
                                    'pass_yds', 'pass_td', 'pass_int', 'sacked', 'sack_yds', 'yards_per_pass_att',
                                    'net_yds_per_pass_att', 'completion_pct', 'qb_rating', 'rush_att',
                                    'rush_yds', 'rush_yds_per_att', 'rush_td', 'field_goal_made', 'field_goal_att',
                                    'extra_point_made', 'extra_point_att', 'punt', 'punt_yds', 'thirddown_conv',
                                    'thirddown_att', 'fourthdown_conv', 'fourthdown_att', 'home_time_of_possession_min']

                # extract data - Game Logs
                game_log = pd.read_html(str(tables), header=None)[0]

                # flatten multiindex
                game_log.reset_index(inplace=True, drop = True)

                # assign new headers
                game_log.columns = game_log_headers

                # define team and year
                game_log['site_code'] = 'buf'#rmteam
                game_log['year'] = 2000#rm yr

                # set OT Coding
                game_log['overtime'] = np.where(game_log.overtime == 'OT', 1, 0)

                # set home_away
                game_log['home_away'] = np.where(
                    game_log.home_away == "@", "A", "H")

                # Convert time of possession to min
                game_log['home_time_of_possession_min'] = game_log.home_time_of_possession_min.apply(
                    lambda x: (int(x[:-3]) / 60) + int(x[-2:]))

                # Drop unwanted boxscore
                game_log.drop(['boxscore'], axis = 1, inplace = True)

                # Convert date - need to figure out
                f#rom dateutil.parser import parse
                #game_log.['date'] = pd.to_datetime(parse(game_log.date + ", " + game_log.year.astype(str)))
                
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
