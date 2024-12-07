import sqlite3
from contextlib import closing
from business import Game, Gamelog

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "gamelog_db.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_game(row):
    return Game(row["gameName"], row["genre"],
                  row["platform"], row["length"], row["timePlayed"],
                  row["status"], row["developer"], row["releaseYear"],
                  row["gameOrder"], row["gameID"])

def get_games():    
    query = '''SELECT gameID, gameName, genre, platform,
                      length, timePlayed, status, developer, releaseYear, gameOrder
               FROM Games
               ORDER BY gameID'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    games = Gamelog()
    for row in results:
        game = make_game(row)
        games.add(game)
    return games

def get_game(id):
    query = '''SELECT gameID, gameName, genre, platform,
                      length, timePlayed, currentStatus,
                      developer, releaseYear, gameOrder
               FROM Games
               WHERE gameID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        row = c.fetchone()
        if row:
            game = make_game(row)
            return game
        else:
            return None

def add_game(game):
    sql = '''INSERT INTO Games (gameName, genre, platform,
                      length, timePlayed, status, developer, releaseYear, gameOrder)
             VALUES (?,?,?,?,?,?,?,?,?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (game.gameName, game.genre,
              game.platform, game.length, game.timePlayed, game.status, game.developer, game.releaseYear, game.gameOrder))
        conn.commit()

def delete_game(game):
    sql = '''DELETE FROM Games
                     WHERE gameID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (game.gameID,))
        conn.commit()

def update_game(game):
    sql = '''UPDATE Games
             SET status = ?,
             timePlayed = ?
             WHERE gameID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (game.status, game.timePlayed,
                        game.gameID))
        conn.commit()

def update_gamelog_order(gamelog):
    for num, game in enumerate(gamelog, start=1):
        game.gameOrder = num
        sql = '''UPDATE Games
                 SET gameOrder = ?
                 WHERE gameID = ?'''
        with closing(conn.cursor()) as c:
            c.execute(sql, (game.gameOrder, game.gameID))
    conn.commit()
    

def main():
    connect()
    games = get_games()
    for game in games:
        print(game.gameName, game.genre,
              game.platform, game.length, game.timePlayed,
              game.percentComp, game.developer, game.releaseYear,
              game.gameOrder)


if __name__ == "__main__":
    main()
