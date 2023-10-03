import pandas as pd

class CreateNflTable:
    def __init__(self):
        self.nfl_teams_data = [
            {"Time": "Arizona Cardinals", "Divisão": "NFC Oeste", "Liga": "NFC"},
            {"Time": "Atlanta Falcons", "Divisão": "NFC Sul", "Liga": "NFC"},
            {"Time": "Baltimore Ravens", "Divisão": "AFC Norte", "Liga": "AFC"},
            {"Time": "Buffalo Bills", "Divisão": "AFC Leste", "Liga": "AFC"},
            {"Time": "Carolina Panthers", "Divisão": "NFC Sul", "Liga": "NFC"},
            {"Time": "Chicago Bears", "Divisão": "NFC Norte", "Liga": "NFC"},
            {"Time": "Cincinnati Bengals", "Divisão": "AFC Norte", "Liga": "AFC"},
            {"Time": "Cleveland Browns", "Divisão": "AFC Norte", "Liga": "AFC"},
            {"Time": "Dallas Cowboys", "Divisão": "NFC Leste", "Liga": "NFC"},
            {"Time": "Denver Broncos", "Divisão": "AFC Oeste", "Liga": "AFC"},
            {"Time": "Detroit Lions", "Divisão": "NFC Norte", "Liga": "NFC"},
            {"Time": "Green Bay Packers", "Divisão": "NFC Norte", "Liga": "NFC"},
            {"Time": "Houston Texans", "Divisão": "AFC Sul", "Liga": "AFC"},
            {"Time": "Indianapolis Colts", "Divisão": "AFC Sul", "Liga": "AFC"},
            {"Time": "Jacksonville Jaguars", "Divisão": "AFC Sul", "Liga": "AFC"},
            {"Time": "Kansas City Chiefs", "Divisão": "AFC Oeste", "Liga": "AFC"},
            {"Time": "Las Vegas Raiders", "Divisão": "AFC Oeste", "Liga": "AFC"},
            {"Time": "Los Angeles Chargers", "Divisão": "AFC Oeste", "Liga": "AFC"},
            {"Time": "Los Angeles Rams", "Divisão": "NFC Oeste", "Liga": "NFC"},
            {"Time": "Miami Dolphins", "Divisão": "AFC Leste", "Liga": "AFC"},
            {"Time": "Minnesota Vikings", "Divisão": "NFC Norte", "Liga": "NFC"},
            {"Time": "New England Patriots", "Divisão": "AFC Leste", "Liga": "AFC"},
            {"Time": "New Orleans Saints", "Divisão": "NFC Sul", "Liga": "NFC"},
            {"Time": "New York Giants", "Divisão": "NFC Leste", "Liga": "NFC"},
            {"Time": "New York Jets", "Divisão": "AFC Leste", "Liga": "AFC"},
            {"Time": "Philadelphia Eagles", "Divisão": "NFC Leste", "Liga": "NFC"},
            {"Time": "Pittsburgh Steelers", "Divisão": "AFC Norte", "Liga": "AFC"},
            {"Time": "San Francisco 49ers", "Divisão": "NFC Oeste", "Liga": "NFC"},
            {"Time": "Seattle Seahawks", "Divisão": "NFC Oeste", "Liga": "NFC"},
            {"Time": "Tampa Bay Buccaneers", "Divisão": "NFC Sul", "Liga": "NFC"},
            {"Time": "Tennessee Titans", "Divisão": "AFC Sul", "Liga": "AFC"},
            {"Time": "Washington Commanders", "Divisão": "NFC Leste", "Liga": "NFC"},
        ]

        self.columns = ['team', 'pts']

    def __enter__(self):
        return self

    def create_nfl_table(self):
        try:
            nfl_teams_df = pd.DataFrame(self.nfl_teams_data)

        except Exception as e:
            print(e)

        else:    
            return nfl_teams_df
    
    def calcular_pontos(self, row):
        diferenca_pontos = row['pts_winner'] - row['pts_loser']
        
        if diferenca_pontos > 0:
            return 1  # 1 pontos para a equipe vencedora
        elif diferenca_pontos == 0:
            return 0.5  # 0.5 ponto para um empate
        else:
            return 0  # 0 pontos para a equipe perdedora
        
        # (wins + 0.5 x ties) / games
    
    def create_score_table(self, nfl_df):
        try:
            df = nfl_df[['Week', 'Winner/tie', 'Loser/tie', 'Pts Scored', 'Pts Allowed']]
            df.columns = ['week', 'winner', 'loser', 'pts_winner', 'pts_loser']
            df['pts_winner'] = df['pts_winner'].astype('int')
            df['pts_loser'] = df['pts_loser'].astype('int')

            df["Pontos"] = df.apply(self.calcular_pontos, axis=1)

            df_winner = df[df['Pontos'] == 1].reset_index(drop=True)
            df_ties = df[df['Pontos'] == 0.5].reset_index(drop=True)

            df_winner_final = df_winner.groupby('winner', as_index=False).sum()[['winner', 'Pontos']]
            df_winner_final.columns = self.columns

            df_1 = df_ties[['winner', 'Pontos']]
            df_1.columns = self.columns

            df_2 = df_ties[['loser', 'Pontos']]
            df_2.columns = self.columns

            df_ties_final = df_1.append(df_2)

            df_final = df_winner_final.append(df_ties_final).groupby('team', as_index=False).sum()
            df_final['pts'] = df_final['pts'] / len(df['week'].unique())

        except Exception as e:
            print(e)

        else:
            return df_final
    
    def create_final_score_table(self, score_table, nfl_table):
        try:
            nfl_df = nfl_table.merge(score_table, left_on='Time', right_on='team', how='left').fillna(0).drop('team', axis=1)

        except Exception as e:
            print(e)

        else:
            return nfl_df
    
    def __exit__(self, *args, **kwargs):
        return self