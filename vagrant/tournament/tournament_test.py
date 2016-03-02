#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def testSetup():
    """
    Test for initial database creation and creating a tournament.
    """
    apocalypse()
    print "0-A. apocalypse() drops all of the tables."
    setup()
    print "0-B. setup() creates tables."
    createTournament("Check-A-Thon 2016", "checkers")
    print "0-C. createTournament() creates a tournament."

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches("1")
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    registerPlayer("1", "Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer("1", "Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches("1")
    deletePlayers()
    registerPlayer("1", "Melpomene Murray")
    registerPlayer("1", "Randy Schwartz")
    standings = playerStandings("1")
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 8:
        raise ValueError("Each playerStandings row should have eight columns.")
    [(id1, tournament1, name1, wins1, draws1, losses1, byes1, matches1),
     (id2, tournament2, name2, wins2, draws2, losses2, byes2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches("1")
    deletePlayers()
    registerPlayer("1", "Bruno Walton")
    registerPlayer("1", "Boots O'Neal")
    registerPlayer("1", "Cathy Burton")
    registerPlayer("1", "Diane Grant")
    standings = playerStandings("1")
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "1", id1)
    reportMatch(id3, id4, "1", id3)
    standings = playerStandings("1")
    for (i, t, n, w, d, l, b, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches("1")
    standings = playerStandings("1")
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, t, n, w, d, l, b, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteMatches("1")
    deletePlayers()
    registerPlayer("1", "Twilight Sparkle")
    registerPlayer("1", "Fluttershy")
    registerPlayer("1", "Applejack")
    registerPlayer("1", "Pinkie Pie")
    registerPlayer("1", "Rarity")
    registerPlayer("1", "Rainbow Dash")
    registerPlayer("1", "Princess Celestia")
    registerPlayer("1", "Princess Luna")
    standings = playerStandings("1")
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, "1", id1)
    reportMatch(id3, id4, "1", id3)
    reportMatch(id5, id6, "1", id5)
    reportMatch(id7, id8, "1", id7)
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


def testByes():
    """
    Test that pairs with odd numbers assign byes and generate pairs properly.
    """
    deleteMatches("1")
    deletePlayers()
    registerPlayer("1", "Twilight Sparkle")
    registerPlayer("1", "Fluttershy")
    registerPlayer("1", "Applejack")
    registerPlayer("1", "Pinkie Pie")
    registerPlayer("1", "Rarity")
    registerPlayer("1", "Rainbow Dash")
    registerPlayer("1", "Princess Celestia")
    registerPlayer("1", "Princess Luna")
    registerPlayer("1", "Spike")
    standings = playerStandings("1")
    [id1, id2, id3, id4, id5, id6, id7, id8, id9] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For nine players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id2, id3, "1", id2)
    reportMatch(id4, id5, "1", id4)
    reportMatch(id6, id7, "1", id6)
    reportMatch(id8, id9, "1", id8)
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For nine players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    expected_pairs = set([frozenset([id3, id5]), frozenset([id7, id8]),
                          frozenset([id6, id2]), frozenset([id1, id4]),
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in expected_pairs:
            raise ValueError(
                "Something broke and you got an unexpected pair! Fix it!")
    reportMatch(pid1, pid2, "1", pid1)
    reportMatch(pid3, pid4, "1", pid3)
    reportMatch(pid5, pid6, "1", pid5)
    reportMatch(pid7, pid8, "1", None)


if __name__ == '__main__':
    testSetup()
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success! All primary tests pass!"
    testByes()
    print "Bonus! Tournaments with odd numbers of players assign byes and you can have draws!"