#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.

    Returns: a database connection and the cursor.
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    return conn, cur


def deleteMatches(tournament):
    """Remove all the match records from the database."""
    conn, cur = connect()
    cur.execute("""DELETE FROM matches;""")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("""DELETE FROM players;""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    cur.execute("""SELECT COUNT(*) from players;""")
    result = cur.fetchone()
    number = result[0]
    conn.close()
    return number


# def createTournament(name, game):
#     """Adds a tournament to the tournaments table.
#
#     The database assigns a unique serial id number for the tournament.
#
#     Args:
#       name: name of the tournament (such as 'Check-A-Thon 2016').
#       game: name of the game being played (such as 'checkers').
#     """
#     conn, cur = connect()
#     cur.execute("""
#         INSERT INTO tournaments (name, game)
#         VALUES (%s, %s);""",
#         (name, game)
#                 )
#     conn.commit()
#     conn.close()


def registerPlayer(tournament, name):
    """Adds a player to the tournament database.

    NOTE: There MUST be a pre-existing tournament to add the player to.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      tournament: serial id from tournaments table (mandatory foreign key).
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
   # Checks to see if the player is already in the players table and grabs the id
    cur.execute ("""SELECT id FROM players WHERE name = (%s);""",
                 (name,))
    id = cur.fetchone()
    # Adds the player to players if they aren't in the database and grabs the id
    if id == None:
        cur.execute("""
            INSERT INTO players (name)
            VALUES (%s);""",
            (name,)
                    )
        cur.execute ("""SELECT id FROM players WHERE name = (%s);""",
                     (name,))
        id = cur.fetchone()
    # # Adds the player to registrations
    # cur.execute("""
    #     INSERT INTO registrations (tournament, player)
    #     VALUES (%s, %s);""",
    #             (tournament, id)
    #             )
    conn.commit()
    conn.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, tournament, name, wins, draws, losses, byes, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player has tied in
        losses: the number of matches the player has lost
        byes: whether or not the player has received a bye (0 or 1)
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    cur.execute ("""SELECT * FROM standings;""")
    standings = cur.fetchall()
    conn.close()
    return standings


def reportMatch(player1, player2, tournament, winner):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id number of the tournament
      player1:  the id number of the first player
      player2:  the id number of the second player
      winner: the id number of the player who won or none for a draw
    """
    conn, cur = connect()
    cur.execute("""
        INSERT INTO matches (player1, player2, winner)
        VALUES (%s, %s, %s);""",
        (player1, player2, winner)
                )
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn, cur = connect()
    cur.execute("""
        SELECT id, name FROM standings
        ORDER BY wins, draws;"""
                )
    results = cur.fetchall()
    if len(results) % 2 == 0:
        pairings = []
        for p in range(0, len(results), 2):
            pair = results[p] + results[p + 1]
            pairings.append(pair)
        conn.close()
        return pairings
    elif len(results) % 2 == 1:
        cur.execute("""
            SELECT id FROM standings
            ORDER BY byes;"""
                    )
        bye = cur.fetchone()
        cur.execute("""
            INSERT INTO matches (player1, player2, winner)
            VALUES (%s, %s, %s);""",
            (bye, bye, bye)
                    )
        conn.commit()
        bye = bye[0]
        for r in results:
            if r[0] == bye:
                results.remove(r)
        pairings = []
        for p in range(0, len(results), 2):
            pair = results[p] + results[p + 1]
            pairings.append(pair)
        conn.close()
        return pairings


