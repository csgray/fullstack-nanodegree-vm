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

-- Players' wins, losses, draws, byes, and matches are derived from the matches table
-- Win: entries in player1 and player2, ID in winner
--    Example: 1, 2, 1
-- Loss: entries in player1 and player2, ID not in winner
--    Example: 1, 2, 2
-- Draw: entries in player1 and player2, no winner at all
--    Example: 1, 2, 0
-- Bye: entry in player1, no entry in player2, ID in winner
--    Example: 1, 0, 1

CREATE TABLE matches (
  id SERIAL PRIMARY KEY NOT NULL,
  tournament INT REFERENCES tournaments(id) NOT NULL,
  date DATE DEFAULT current_date,
  winner INT REFERENCES players(id) NOT NULL,
  loser INT REFERENCES players(id) NOT NULL,
  draw BOOLEAN DEFAULT FALSE
);

-- MOCK DATA FOR TESTING:
INSERT INTO tournaments (name, game) VALUES ('Check-A-Thon 2016', 'checkers');
INSERT INTO players (id, name) VALUES ('1', 'Arnold');
INSERT INTO players (id, name) VALUES ('2', 'Bob');
INSERT INTO players (id, name) VALUES ('3', 'Charlie');
INSERT INTO players (id, name) VALUES ('4', 'Dave');
INSERT INTO players (id, name) VALUES ('5', 'Eric');
INSERT INTO registrations (tournament, player) VALUES ('1', '1');
INSERT INTO registrations (tournament, player) VALUES ('1', '2');
INSERT INTO registrations (tournament, player) VALUES ('1', '3');
INSERT INTO registrations (tournament, player) VALUES ('1', '4');
INSERT INTO registrations (tournament, player) VALUES ('1', '5');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '1', '2', 'False');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '3', '4', 'True');
INSERT INTO matches (tournament, winner, loser, draw) VALUES ('1', '5', '5', 'False');

-- CREATE VIEW wins AS
--   SELECT p.id, p.name, m.player1, m.player2, m.winner
--   FROM players p, matches m
--     WHERE m.player1 = p.id AND m.player2 = p.id
--   GROUP BY m.tournament, p.id, m.player1, m.player2, m.winner
-- ;