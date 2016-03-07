-- noinspection SqlNoDataSourceInspectionForFile
-- Table definitions for the tournament project.

-- Run the following in the command line to create and connect to the database:
-- psql -f tournament.sql
-- psql tournament

-- Initial setup
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Assigns and tracks the players' ID numbers
CREATE TABLE players (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL
);

-- Tracks the results of the tournament.
-- Win: ID in player1 OR player2 (both filled out) AND  winner
-- Loss: ID in player1 OR player2 (both filled out) AND NOT winner
-- Draw: ID in player1 OR player2 but no winner (null)
-- Bye: ID in player1 AND player2 AND winner
CREATE TABLE matches (
  date DATE DEFAULT current_date,
  player1 INT REFERENCES players(id) NOT NULL,
  player2 INT REFERENCES players(id) NOT NULL,
  winner INT REFERENCES players(id),
  PRIMARY KEY (player1, player2)
);

-- Calculates the wins from the matches table
CREATE VIEW wins AS
  SELECT p.id, p.name, count(m.winner)
  FROM players p
  LEFT OUTER JOIN matches m ON p.id = m.winner
  GROUP BY p.id
  ORDER BY p.id;

-- Calculates the losses from the matches table
CREATE VIEW losses AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON
    (p.id = m.player1 OR p.id = m.player2) AND (p.id != m.winner)
  GROUP BY p.id
  ORDER BY p.id;

-- Calculates the draws from the matches table
CREATE VIEW draws AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON
    (p.id = m.player1 OR p.id = m.player2) AND (m.winner IS NULL)
  GROUP BY p.id
  ORDER BY p.id;

-- Calculates the total matches from the matches table
CREATE VIEW totals AS
  SELECT p.id, p.name, count(m.player1 + m.player2)
  FROM players p
  LEFT OUTER JOIN matches m ON (p.id = m.player1 OR p.id = m.player2)
  GROUP BY p.id
  ORDER by p.id;

-- Calculates the byes from the matches table
CREATE VIEW byes AS
  SELECT p.id, p.name, count(m.winner)
  FROM players p
  LEFT OUTER JOIN matches m ON (p.id = m.winner) AND (m.player1 = m.player2)
  GROUP BY p.id
  ORDER BY p.id;

-- Combines the other views into one cohesive view
CREATE VIEW standings AS
  SELECT p.id, p.name,
    w.count AS wins, d.count AS draws, l.count AS losses, t.count AS matches, b.count AS byes
  FROM players p
  LEFT OUTER JOIN wins w ON (p.id = w.id)
  LEFT OUTER JOIN draws d ON (p.id = d.id)
  LEFT OUTER JOIN losses l ON (p.id = l.id)
  LEFT OUTER JOIN totals t ON (p.id = t.id)
  LEFT OUTER JOIN byes b ON (p.id = b.id)
  ORDER BY p.id;
