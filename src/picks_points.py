import pandas as pd

class PicksPoints:
    def __enter__(self):
        return self
    
    def join_picks_and_points(self, picks, points):
        points_table = points[['Time', 'pts']]
        points_table.columns = ['pick', 'pts']

        merged_df = picks.merge(points_table, on='pick', how='left')

        return merged_df
    
    def create_point_per_player_table(self, merged_df):
        final_table = merged_df.groupby('player', as_index=False).sum(numeric_only=True)

        return final_table
    
    def __exit__(self, *args, **kwargs):
        return self