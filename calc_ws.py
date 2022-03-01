import csv
import numpy

import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':
    players_df = pd.read_csv('playerDB.csv')
    draft_df = pd.read_csv('draftDB.csv')

    # load externel link dataset
    link_df = pd.read_csv('NBA_Player_IDs.csv',  encoding= 'unicode_escape')
    link_df = link_df[pd.notna(link_df['NBAID'])]
    link_df.loc[:,'NBAID'] = link_df.loc[:,'NBAID'].astype(int)

    # Only consider first 2 rounds
    draft_df = draft_df[draft_df['numberRound']<=2]
    # Limit to the 3-pt era
    draft_df = draft_df[draft_df['yearDraft']>=1979]
    # Only consider players with 4 years of data
    draft_df = draft_df[draft_df['yearDraft']<=2015]
    num_drafts = len(draft_df.yearDraft.unique())

    # Get year from season string
    players_df.loc[:,'year'] = players_df['Season'].apply(lambda season: int(season.split('-')[0]))

    curr_miss = draft_df[draft_df.basketball_reference_url.isna()]
    print(f'Missing {len(curr_miss)} links between player and draft')

    # Merge draft and link dataframe
    draft_df = draft_df.merge(link_df, how='left', left_on='idPlayer', right_on='NBAID')
    draft_df.loc[:,'urlID'] = draft_df.loc[:,'BBRefID'] 

    curr_miss = draft_df[draft_df.urlID.isna()]
    print(f'Missing {len(curr_miss)} links between player and draft')

    # Add combine player and draft
    combined_df = players_df.merge(draft_df, how='inner', on='urlID')

    num_players_yrs = len(combined_df)
    num_players = len(combined_df.urlID.unique())

    print(f'{num_players} distinct players with {num_players_yrs} player-seasons of data')

    # Limit to 4 seasons
    only_4_years = combined_df[(combined_df['year']-combined_df['yearDraft'])<=3]

    # Sum up winshares, divide by number of years in dataset
    avg_rookie_ws = only_4_years.groupby('numberPickOverall')['WS'].sum()/num_drafts
    avg_rookie_ws.to_csv('avg_rookie_winshare.csv')

