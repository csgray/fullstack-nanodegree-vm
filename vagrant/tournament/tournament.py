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


def deleteMatches():
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


def registerPlayer(name):
    """Adds a player to the tournament database with a unique ID assigned by the database.
  
    Args:
        name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    cur.execute("""
        INSERT INTO players (name)
        VALUES (%s);""",
        (name,)
                )
    conn.commit()
    conn.close()


def playerStandings():
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
            matches: the number of matches the player has played
            byes: whether or not the player has received a bye (0 or 1)
    """
    conn, cur = connect()
    cur.execute ("""SELECT * FROM standings;""")
    standings = cur.fetchall()
    conn.close()
    return standings


def reportMatch(player1, player2, winner):
    """Records the outcome of a single match between two players.

    Args:
        tournament: the id number of the tournament
        player1:  the id number of the first player
        player2:  the id number of the second player
        winner: the id number of the player who won or none for a draw

    Logic for entering results:
        win: ID in player1 OR player2 (both filled out) AND winner
        loss: ID in player1 OR player2 (both filled out) AND NOT winner
        draw: ID in player1 OR player2 but no winner (null)
        bye: ID in player1 AND player2 AND winner
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
    # Orders the players by wins then draws so that players of near-equal skill play together
    cur.execute("""
        SELECT id, name FROM standings
        ORDER BY wins, draws;"""
                )
    results = cur.fetchall()
    # Checks if there is an even number of players
    if len(results) % 2 == 0:
        # Pairs players who are adjacent in the standings
        pairings = []
        for p in range(0, len(results), 2):
            pair = results[p] + results[p + 1]
            pairings.append(pair)
        conn.close()
        return pairings
    # Checks if there is an odd number of players
    elif len(results) % 2 == 1:
        # Orders players by the number of byes received so far
        cur.execute("""
            SELECT id FROM standings
            ORDER BY byes;"""
                    )
        # Selects the player with the least number of byes
        bye = cur.fetchone()
        # Assigns that player a bye in matches#
        cur.execute("""
            INSERT INTO matches (player1, player2, winner)
            VALUES (%s, %s, %s);""",
            (bye, bye, bye)
                    )
        conn.commit()
        # Removes the player who received the bye from the pairings list
        bye = bye[0]
        for r in results:
            if r[0] == bye:
                results.remove(r)
        # Pairs players who are adjacent in the standings
        pairings = []
        for p in range(0, len(results), 2):
            pair = results[p] + results[p + 1]
            pairings.append(pair)
        conn.close()
        return pairings


