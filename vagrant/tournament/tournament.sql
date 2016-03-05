-- noinspection SqlNoDataSourceInspectionForFile
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Run the following in the command line to create and connect to the database:
-- psql -f tournament.sql
-- psql tournament

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- CREATE TABLE tournaments (
--   id SERIAL PRIMARY KEY NOT NULL,
--   name TEXT NOT NULL,
--   game TEXT NOT NULL
-- );

CREATE TABLE players (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL
);

-- CREATE TABLE registrations (
--   tournament INT REFERENCES tournaments(id) NOT NULL,
--   player INT REFERENCES players(id) NOT NULL,
--   PRIMARY KEY (tournament, player)
-- );

CREATE TABLE matches (
--   tournament INT REFERENCES tournaments(id) NOT NULL,
  date DATE DEFAULT current_date,
  player1 INT REFERENCES players(id) NOT NULL,
  player2 INT REFERENCES players(id) NOT NULL,
  winner INT REFERENCES players(id),
  PRIMARY KEY (player1, player2)
);

CREATE VIEW wins AS
  SELECT p.id, p.name, count(m.winner)
  FROM players p
  LEFT OUTER JOIN matches m ON p.id = m.winner
  GROUP BY p.id
  ORDER BY p.id;

CREATE VIEW losses AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON
    (p.id = m.player1 OR p.id = m.player2) AND (p.id != m.winner)
  GROUP BY p.id
  ORDER BY p.id;

CREATE VIEW draws AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON
    (p.id = m.player1 OR p.id = m.player2) AND (m.winner IS NULL)
  GROUP BY p.id
  ORDER BY p.id;

CREATE VIEW totals AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON (p.id = m.player1 OR p.id = m.player2)
  GROUP BY p.id
  ORDER by p.id;

CREATE VIEW byes AS
  SELECT p.id, p.name, count(m.winner)
  FROM players p
  LEFT OUTER JOIN matches m ON (p.id = m.winner) AND (m.player1 = m.player2)
  GROUP BY p.id
  ORDER BY p.id;

CREATE VIEW standings AS
  SELECT p.id, p.name,
    w.count AS wins, l.count AS losses, d.count AS draws, t.count AS matches, b.count AS byes
  FROM players p
  LEFT OUTER JOIN wins w ON (p.id = w.id)
  LEFT OUTER JOIN losses l ON (p.id = l.id)
  LEFT OUTER JOIN draws d ON (p.id = d.id)
  LEFT OUTER JOIN totals t ON (p.id = t.id)
  LEFT OUTER JOIN byes b ON (p.id = b.id)
  ORDER BY p.id;

-- SELECT p.id, p.name,
--   (  SELECT count(m.winner)
--      FROM players p
--      INNER JOIN matches m ON p.id = m.winner
--      GROUP BY m.tournament, p.id
--      ORDER BY m.tournament, p.id) as wins,
--   (  SELECT count(m.player1 + m.player2)
--      FROM players p
--      INNER JOIN matches m ON
--        (p.id = m.player1 OR p.id = m.player2) AND (p.id != m.winner)
--      GROUP BY m.tournament, p.id
--      ORDER BY m.tournament, p.id) as losses,
--   (  SELECT count(m.player1 + m.player2)
--      FROM players p
--      INNER JOIN matches m ON
--        (p.id = m.player1 OR p.id = m.player2) AND (m.winner IS NULL)
--      GROUP BY m.tournament, p.id
--      ORDER BY m.tournament, p.id) as draws
--   FROM players p
--   GROUP BY p.id
--   ORDER BY p.id;


-- CREATE VIEW standings AS
--   SELECT p.id, p.name, m.tournament,
--     count(m.winner) as wins,
--     count(m.player1 + m.player2) as losses,
--     count(m.player1 + m.player2) as draws,
--     count(m.winner) as byes
--   FROM players p
--   LEFT OUTER JOIN matches m ON p.id = m.winner
--   LEFT OUTER JOIN matches m ON
--     (p.id = m.player1 OR p.id = m.player2) AND (p.id != m.winner)
--   LEFT OUTER JOIN matches m ON
--     (p.id = m.player1 OR p.id = m.player2) AND (m.winner IS NULL)
--   LEFT OUTER JOIN matches m ON (p.id = m.winner) AND (m.player1 = m.player2)
--   GROUP BY m.tournament, p.id
--   ORDER BY m.tournament, p.id;

/* MOCK DATA FOR TESTING
Tournament 1:
  Arnold:  2 wins, 0 losses, 0 draws, 0 byes
  Bob:     1 win,  1 loss,   0 draws, 0 byes
  Charlie: 0 wins, 1 loss,   1 draw,  0 byes
  Dave:    1 win,  0 losses, 1 draw,  1 bye
  Eric:    1 win,  1 loss,   0 draws, 1 bye

Tournament 2:
  Arnold:  1 win, 0 losses, 1 draw,  0 byes
  Bob:     1 win, 1 loss,   0 draws, 0 byes
  Charlie: 1 win, 0 losses, 1 draw,  0 byes
  Frank:   1 win, 1 loss,   0 draws, 1 bye
  George:  1 win, 1 loss,   0 draws, 1 bye
 */

-- INSERT INTO tournaments (name, game) VALUES ('Check-A-Thon 2016', 'checkers');
-- INSERT INTO tournaments (name, game) VALUES ('Chess Masters', 'chess');
INSERT INTO players (name) VALUES ('Arnold');
INSERT INTO players (name) VALUES ('Bob');
INSERT INTO players (name) VALUES ('Charlie');
INSERT INTO players (name) VALUES ('Dave');
INSERT INTO players (name) VALUES ('Eric');
-- INSERT INTO players (name) VALUES ('Frank');
-- INSERT INTO players (name) VALUES ('George');
-- INSERT INTO registrations (tournament, player) VALUES ('1', '1');
-- INSERT INTO registrations (tournament, player) VALUES ('1', '2');
-- INSERT INTO registrations (tournament, player) VALUES ('1', '3');
-- INSERT INTO registrations (tournament, player) VALUES ('1', '4');
-- INSERT INTO registrations (tournament, player) VALUES ('1', '5');
-- INSERT INTO registrations (tournament, player) VALUES ('2', '1');
-- INSERT INTO registrations (tournament, player) VALUES ('2', '2');
-- INSERT INTO registrations (tournament, player) VALUES ('2', '3');
-- INSERT INTO registrations (tournament, player) VALUES ('2', '6');
-- INSERT INTO registrations (tournament, player) VALUES ('2', '7');
INSERT INTO matches (player1, player2, winner) VALUES ('1', '2', '1');
INSERT INTO matches (player1, player2, winner) VALUES ('3', '4', NULL);
INSERT INTO matches (player1, player2, winner) VALUES ('5', '5', '5');
INSERT INTO matches (player1, player2, winner) VALUES ('1', '5', '1');
INSERT INTO matches (player1, player2, winner) VALUES ('2', '3', '2');
INSERT INTO matches (player1, player2, winner) VALUES ('4', '4', '4');
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '1', '2', '1');
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '3', '6', '3');
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '7', '7', '7');
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '3', '1', NULL);
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '2', '7', '2');
-- INSERT INTO matches (tournament, player1, player2, winner) VALUES ('2', '6', '6', '6');