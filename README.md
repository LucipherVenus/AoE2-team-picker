# AoE2-team-picker-Geo
Lets the user choose the players and creates 2 fairest teams of AoE 2 DE (for Georgian players only).

The final version of the project will do the following:
1. Asks the user the type of the team game (3v3 or 4v4).
2. Displays the names of the players on the screen so that the user can pick the ones who are playing.
3. Creates 2 "fairest" teams out of the selected players and displays them on the screen.
4. Also displays:
    *  Average synergy ELO for each team;
    *  Higher ranked team number based on summed individual 1v1 ELO;
    *  The difference of total synergy ELO-s as the absolute value of the difference of summed individual 1v1 ELOS for each team.



Uses the AoE2.net API to get the live ELOS of the players.
