#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    return conn


def deleteMatches(tournament):
    """Remove all the match records from the database for a particular tournament."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM matches WHERE tournament = (%s);""",
        (tournament)
    )
    cur.execute("""
        UPDATE players
        SET wins = 0, draws = 0, losses = 0, byes = 0, matches = 0
        WHERE tournament = (tournament);""",
        (tournament)
    )
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE FROM players;""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) from players;""")
    result = cur.fetchone()
    number = result[0]
    conn.close()
    return number


def createTournament(name, game):
    """Adds a tournament to the tournaments table.

    The database assigns a unique serial id number for the tournament.

    Args:
      name: name of the tournament (such as 'Check-A-Thon 2016').
      game: name of the game being played (such as 'checkers').
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tournaments (name, game)
        VALUES ('%s', '%s');""",
        (name, game)
    )
    conn.commit()
    conn.close()


def registerPlayer(tournament, name):
    """Adds a player to the tournament database.

    NOTE: There MUST be a pre-existing tournament to add the player to.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      tournament: serial id from tournaments table (mandatory foreign key).
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO players (tournament, name)
        VALUES (%s, %s);""",
        (tournament, name)
    )
    conn.commit()
    conn.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, tournament, name, wins, draws, losses, byes, matches):
        id: the player's unique id (assigned by the database)
        tournament: the id of the tournament hte player is in
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player has tied in
        losses: the number of matches the player has lost
        byes: whether or not the player has received a bye (0 or 1)
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM players
        WHERE tournament = (%s)
        ORDER BY wins;""",
        (tournament)
    )
    result = cur.fetchall()
    conn.close()
    return result


def reportMatch(player1, player2, tournament, winner):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id number of the tournament
      player1:  the id number of the first player
      player2:  the id number of the second player
      winner: the id number of the player who won or none for a draw
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO matches (player1, player2, tournament, winner)
        VALUES (%s, %s, %s, %s);""",
        (player1, player2, tournament, winner)
    )
    if winner == player1:
        cur.execute("""
            UPDATE players
            SET wins = wins + 1, matches = matches + 1
            WHERE id = (%s);""",
            ([player1])
        )
        cur.execute("""
            UPDATE players
            SET losses = losses + 1, matches = matches + 1
            WHERE id = (%s);""",
            ([player2])
        )
    if winner == player2:
        cur.execute("""
            UPDATE players
            SET wins = wins + 1, matches = matches +1
            WHERE id = (%s);""",
            ([player2])
        )
        cur.execute("""
            UPDATE players
            SET losses = losses +1, matches = matches + 1
            WHERE id = (%s);""",
            ([player1])
        )
    elif winner == None:
        cur.execute("""
            UPDATE players
            SET draws = draws + 1, matches = matches + 1
            WHERE id IN (%s, %s);"""
            ([player1], [player2])
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
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name FROM players
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
#    elif len(results) % 2 == 1:
#        pairings = []


