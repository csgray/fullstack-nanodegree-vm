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

CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  game TEXT NOT NULL
);

CREATE TABLE players (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL
);

CREATE TABLE registrations (
  tournament INT REFERENCES tournaments(id) NOT NULL,
  player INT REFERENCES players(id) NOT NULL
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY NOT NULL,
  tournament INT REFERENCES tournaments(id) NOT NULL,
  date DATE DEFAULT current_date,
  winner INT REFERENCES players(id) NOT NULL,
  loser INT REFERENCES players(id) NOT NULL,
  draw BOOLEAN DEFAULT FALSE
);

CREATE VIEW wins AS
  SELECT m.tournament, p.id, p.name, count(m.winner)
  FROM players p INNER JOIN matches m ON p.id = m.winner
  WHERE m.draw = false
  GROUP BY m.tournament, p.id;

CREATE VIEW losses AS
  SELECT m.tournament, p.id, p.name, count(m.loser)
  FROM players p INNER JOIN matches m ON p.id = m.loser
  WHERE m.winner != m.loser
  GROUP BY m.tournament, p.id;

CREATE VIEW draws AS
  SELECT m.tournament, p.id, p.name, count(p.id)
  FROM players p INNER JOIN matches m ON (p.id = m.winner OR p.id = m.loser)
  WHERE m.draw = true
  GROUP BY m.tournament, p.id;

CREATE VIEW byes AS
  SELECT m.tournament, p.id, p.name, count(m.winner)
  FROM players p INNER JOIN matches m ON (p.id = m.winner AND p.id = m.loser)
  GROUP BY m.tournament, p.id;

-- MOCK DATA FOR TESTING:
INSERT INTO tournaments (name, game) VALUES ('Check-A-Thon 2016', 'checkers');
INSERT INTO tournaments (name, game) VALUES ('Chess Masters', 'chess');
INSERT INTO players (name) VALUES ('Arnold');
INSERT INTO players (name) VALUES ('Bob');
INSERT INTO players (name) VALUES ('Charlie');
INSERT INTO players (name) VALUES ('Dave');
INSERT INTO players (name) VALUES ('Eric');
INSERT INTO players (name) VALUES ('Frank');
INSERT INTO players (name) VALUES ('George');
INSERT INTO registrations (tournament, player) VALUES ('1', '1');
INSERT INTO registrations (tournament, player) VALUES ('1', '2');
INSERT INTO registrations (tournament, player) VALUES ('1', '3');
INSERT INTO registrations (tournament, player) VALUES ('1', '4');
INSERT INTO registrations (tournament, player) VALUES ('1', '5');
INSERT INTO registrations (tournament, player) VALUES ('2', '1');
INSERT INTO registrations (tournament, player) VALUES ('2', '2');
INSERT INTO registrations (tournament, player) VALUES ('2', '3');
INSERT INTO registrations (tournament, player) VALUES ('2', '6');
INSERT INTO registrations (tournament, player) VALUES ('2', '7');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '1', '2', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '3', '4', 'True');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '5', '5', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '1', '5', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '2', '3', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '4', '4', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '1', '2', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '3', '6', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '7', '7', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '3', '1', 'True');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '2', '7', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('2', '6', '6', 'False');