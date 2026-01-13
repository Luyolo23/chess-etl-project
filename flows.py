from prefect import flow, task
from prefect import get_run_logger
import requests
import json
import pandas as pd
import psycopg2
import math

username = "Larry23"


@task(retries=3, retry_delay_seconds=5)
def extract(username):
    logger = get_run_logger()
    url = f"https://lichess.org/api/games/user/{username}"

    params = {
        "max": 50,
        "moves": True,
        "pgnInJson": True
    }

    headers = {
        "Accept": "application/x-ndjson"
    }

    logger.info(f"Downloading games for {username}")

    response = requests.get(url, params=params, headers=headers)

    with open("raw_games.ndjson", "w") as f:
        f.write(response.text)

    return "raw_games.ndjson"


@task
def transform(file_path):
    records = []

    with open(file_path) as f:
        for line in f:

            if not line:
                continue

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
                    "winner": game.get("winner", "unknown"),
                    "moves_count": math.ceil(len(game.get("moves", "").split()) / 2)
                }

                records.append(record)

    df = pd.DataFrame(records)
    df.to_csv("games.csv", index=False)

    return "games.csv"


@task
def load(csv_file):
    df = pd.read_csv(csv_file)

    conn = psycopg2.connect(
        dbname="chessdb",
        user="chessuser",
        password="chesspass",
        host="localhost"
    )

    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
                    INSERT INTO games (game_id, rated, speed, game_outcome, time_control, white_player, black_player, white_rating, black_rating, winner, moves_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (game_id) DO NOTHING;
                    """,(
                            row["game_id"],
                            row["rated"],
                            row["speed"],
                            row["game_outcome"],
                            row["time_control"],
                            row["white_player"],
                            row["black_player"],
                            row["white_rating"],
                            row["black_rating"],
                            row["winner"],
                            row["moves_count"]
                            ))

    conn.commit()
    cur.close()
    conn.close()


@flow(name="chess-pipeline")
def chess_pipeline(username):
    raw_file = extract(username)
    csv_file = transform(raw_file)
    load(csv_file)


if __name__ == "__main__":
    chess_pipeline()
