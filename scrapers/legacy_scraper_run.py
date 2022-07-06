# Annual & Legacy Scraper
# First Run is set to collect all legacy data
# Scheduler is designed to scrape weekely and season totals
# author: Jake Bernards


# To Do:
# 1. Set up mysql and push data there
# 2. Decide if two run scripts are needed (weekely and annual) or if I can build it into once file

import numpy as np

# Scrape season totals
#import Scraper_Player_Season_Totals as ps

#player_legacy_df = ps.player_legacy(2000, 2022)
# print(player_legacy_df.head())

# Scrape data for each week
import Scraper_Team_Stats_Rankings as ts
# Define team code


team_codes = ['buf', 'nwe', 'mia', 'nyj',  # aft east
              'cin', 'pit', 'cle', 'rav',  # afc north
              'oti', 'clt', 'htx', 'jax',  # afc south
              'kan', 'rai', 'sdg', 'den',  # afc west
              'dal', 'phi', 'was', 'nyg',  # nfc east
              'gnb', 'min', 'chi', 'det',  # nfc north
              'tam', 'nor', 'atl', 'car',  # nfc south
              'ram', 'crd', 'sfo', 'sea']  # nfc west

# Define years you wish to pull data from
years = np.array(range(2019, 2022))

# Scrape Data
team_game_legacy_df = ts.game_scrapper(team_codes, years)

team_game_legacy_df.to_csv("Data/Legacy Team Data_00-21.csv")
