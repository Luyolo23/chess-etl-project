CREATE TABLE games (
    game_id TEXT PRIMARY KEY,
    rated BOOLEAN,
    speed TEXT,
    game_outcome TEXT,
    time_control INT,
    white_player TEXT,
    black_player TEXT,
    white_rating INT,
    black_rating INT,
    winner TEXT,
    moves_count INT
);