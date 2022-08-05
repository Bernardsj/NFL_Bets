team_game_legacy_df['date'] = team_game_legacy_df['date'] + "," + team_game_legacy_df['year'].astype(str)
team_game_legacy_df['date'] = team_game_legacy_df['date'].astype(date)
