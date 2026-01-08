import psycopg2
import pandas as pd


def load():
    
    df = pd.read_csv("games.csv")

    conn = psycopg2.connect(
        dbname = "chessdb",
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

    print("Data loaded into PostgreSQL")