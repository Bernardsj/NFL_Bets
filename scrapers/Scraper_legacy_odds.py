# To Do:
# author: Jake Bernards

# Install dependencies
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.error import HTTPError


def odds_scrapper(team_codes, years):
    for team in team_codes:
        for yr in years:
            try:
                # Pull up team/year web pages
                url = f"https://www.pro-football-reference.com/teams/{team}/{yr}_lines.htm"
                html = urlopen(url)
                soup = BeautifulSoup(html, features="lxml")
                tables = soup.find_all('table')  # create list of tables
                
                # Define headers
                bet_log_headers = ['game_num', 'opponent_code', 'spread', 'ou', 'result', 'line_result', 'ou_result']

                # extract data - Game Logs
                bet_log = pd.read_html(str(tables), header=None)[0]

                # flatten multiindex
                bet_log.reset_index(inplace=True, drop = True)

                # assign new headers
                bet_log.columns = bet_log_headers

                # define team and year
                bet_log['site_code'] = team
                bet_log['year'] = yr

                # set home_away
                bet_log['home_away'] = np.where(bet_log.opponent_code.str.contains('@'), "A", "H")

                # clean opponent_code column
                bet_log['opponent_code'] = bet_log.opponent_code.str.strip('@')

                # create score columns
                score = bet_log.result.str.strip('W,|L,|T,').str.split("-", n=1, expand = True)
                bet_log['team_score'] = score[0].astype(int)
                bet_log['opp_score'] = score[1].astype(int)

                # game w/l column
                conditions = [
                    bet_log.line_result == 'Won', 
                    bet_log.line_result == 'Lost',
                    bet_log.line_result == 'Push'
                ]
                values = ['W', 'L', 'P']

                bet_log['line_result'] = np.select(conditions, values)

                # clean result col
                bet_log['game_result'] = bet_log.result.map(lambda x: x[0:1])

                # drop messy columns
                bet_log.drop(columns = 'result', axis = 1, inplace=True)
            
            except ValueError:
                print(f"Error scraping {team}: {yr}")

            except HTTPError:
                print(f"HTTP Error scraping {team}: {yr}")
            else:
                # Create df on first call
                if all([yr == min(years), team == team_codes[0]]):
                    bet_log_archive = bet_log
                
                # combine dfs
                else:
                    bet_log_archive = pd.concat(
                        [bet_log_archive, bet_log], axis=0, join='outer')

                    print(f"Scraping: {team}/{yr}")
    return bet_log_archive