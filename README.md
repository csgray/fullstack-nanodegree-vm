Swiss Pairs Generator
==========
The back-end development path final project for Udacity's Intro to Programming Nanodegree.<br>
Doubles as the Full-Stack Nanodegree's second project.<br>
Coded in Python and PostgreSQL.

To Run the Code:
----------
1. Open the command-line interface and navigate to ./vagrant/ within this repository
2. Start the VM: `vagrant up`
3. Connect to the VM: `vagrant ssh`
4. Navigate to the tournament directory within the VM: `cd /vagrant/tournament`
5. Create the database by importing the SQL file: `psaql -f tournament.sql`
6. Run the tests module: `python tournament_test.py`

The results of the tests will be evident within the terminal.

Connect to the database itself after creating it: `psql tournament`<br>
Then check out the standings after the tests module runs: `SELECT * FROM standings;`

The Database
----------
The database schema consists of two tables: "players" and "matches".

Players has a serialized integer "id" column as its primary key. Its only other column is "name".

Matches has four columns: date, player1, player2, and winner. Date automatically fills itself in with the current date,
and the other three columns are all foreign keyed to players(id). Matches's primary key is the combination of player1
and player2 to ensure there are no duplicate matches.

There are also six views: "wins", "losses", "draws", "totals", "byes", and "standings".The first five views calculate
their namesakes ("totals" is for total matches) and standings combines them into one view.

Win: Player's ID in player1 or player2, ID also in winner<br>
Loss: Player's ID in player1 or player2, different player's ID in winner<br>
Draw: Player's ID in player1 or player2, nothing (null) in winner<br>
Bye: Player's ID in player1 and player2 and winner