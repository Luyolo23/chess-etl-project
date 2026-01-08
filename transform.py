import json
import pandas as pd
import math

def transform():

    records = []

    with open("raw_games.ndjson") as f:
        for line in f:
            game = json.loads(line)

            if game.get("source") == "friend":

                players = game["players"]
                white = players["white"]
                black = players["black"]

                record = {
                    "game_id": game["id"],
                    "rated": game["rated"],
                    "speed": game["speed"],
                    "game_outcome": game["status"],
                    "time_control": game["clock"]["initial"],
                    "white_player": white["user"]["name"],
                    "black_player": black["user"]["name"],
                    "white_rating": white["rating"],
                    "black_rating": black["rating"],
                    "winner": game["winner"],
                    "moves_count": math.ceil(len(game.get("moves", "").split()) / 2)
                }

                records.append(record)

        df = pd.DataFrame(records)

        df.to_csv("games.csv", index=False)
        print("CSV file created!")