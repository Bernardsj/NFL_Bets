# Annual & Legacy Scraper
# First Run is set to collect all legacy data
# Scheduler is designed to scrape weekely and season totals
# author: Jake Bernards


# To Do:
# 2. Decide if two run scripts are needed (weekely and annual) or if I can build it into one file

import numpy as np
import Scrapers.Scraper_Player_Season_Totals as ps # Scrape season totals
import Scrapers.Scraper_Team_Stats_Rankings as ts # Scrape totals for each week
import Scrapers.Scraper_legacy_odds as odds # Scrape totals for each week

# Define team code
team_codes = [
    'buf', 'nwe', 'mia', 'nyj',  # aft east
    'cin', 'pit', 'cle', 'rav',  # afc north
    'oti', 'clt', 'htx', 'jax',  # afc south
    'kan', 'rai', 'sdg', 'den',  # afc west
    'dal', 'phi', 'was', 'nyg',  # nfc east
    'gnb', 'min', 'chi', 'det',  # nfc north
    'tam', 'nor', 'atl', 'car',  # nfc south
    'ram', 'crd', 'sfo', 'sea'  # nfc west
]

# Define years you wish to pull data from
years = np.array(range(2000, 2022))

# Scrape Data
player_fantsey_legacy_df = ps.player_legacy(years)
team_game_legacy_df = ts.game_scrapper(team_codes, years)
odds_line_legacy_df = odds.odds_scrapper(team_codes, years)

# Push data to MySQL database
## Connect to DB
from sqlalchemy import create_engine
engine = create_engine("mysql://root:eK5ERE<Sqv+j[0o@localhost/nfl_bets")

# Push scraped data
player_fantsey_legacy_df.to_sql(con = engine, name = 'player_stats_annual', if_exists='append',index=False)
team_game_legacy_df.to_sql(con = engine, name = 'team_stats_weekly', if_exists='append',index=False)
odds_line_legacy_df.to_sql(con = engine, name = 'vegas_odds', if_exists='append',index=False)

# Save csv backup
player_fantsey_legacy_df.to_csv("Data/Legacy Player Data_00-21.csv")
team_game_legacy_df.to_csv("Data/Legacy Team Data_00-21.csv")
odds_line_legacy_df.to_csv("Data/Odds_00-21.csv")