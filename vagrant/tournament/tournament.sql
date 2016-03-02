-- noinspection SqlNoDataSourceInspectionForFile
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  game text NOT NULL
);

CREATE TABLE players (
  id SERIAL PRIMARY KEY NOT NULL,
  tournament INT REFERENCES tournaments(id),
  name TEXT NOT NULL,
  wins INT DEFAULT 0,
  draws INT DEFAULT 0,
  losses INT DEFAULT 0,
  byes INT DEFAULT 0,
  matches INT DEFAULT 0
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY NOT NULL,
  player1 INT REFERENCES players(id),
  player2 INT REFERENCES players(id),
  tournament INT REFERENCES tournaments(id),
  date DATE DEFAULT GETDATE(),
  winner INT REFERENCES players(id)
);