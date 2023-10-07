import tkinter as tk
import itertools
import requests

# Default ELOS are given to each player in case this info is missing in the API
players = {
    "Lucipher": {"ELO": 1800, "steamID": 677003},
    "Bowman": {"ELO": 1800, "steamID": 288649},
    "zv": {"ELO": 1700, "steamID": 2680347},
    "sandriko": {"ELO": 1550, "steamID": 3153351},
    "guramata": {"ELO": 1530, "steamID": 5462150},
    "purple": {"ELO": 1500, "steamID": 238305},
    "dito": {"ELO": 1500, "steamID": 2654497},
    "WhiteFatal": {"ELO": 1250, "steamID": 3330863},
    "torkiel": {"ELO": 1200, "steamID": 2931088},
    "abgdevzt": {"ELO": 1000, "steamID": 8925314},
    "Nefro": {"ELO": 900, "steamID": 2673312},
    "the_kupre": {"ELO": 1250, "steamID": 10448993},
    "Urbifex": {"ELO": 1008, "steamID": 10448999}
}

# Define the API endpoint
def GetEloOf(player, player_name, id):
    api_url = "https://aoe2.net/api/leaderboard"
    # Set the query parameters
    params = {
        "game": "aoe2de",
        "language": "en",
        "leaderboard_id": 3,
        "start": 1,
        "count": 1,
        "profile_id": id
    }
    # Send a GET request to the API
    response = requests.get(api_url, params=params)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data["leaderboard"] == []:
            print(player_name, player["ELO"])
            return player["ELO"]
        # Return the ELO of the given player
        print(data['leaderboard'][0]['name'], '-', data['leaderboard'][0]['rating'])
        return data['leaderboard'][0]['rating']
    else:
        return player["ELO"]

# Fill ELLO-S of the players in real-time using AoE2.net API
for player in players:
    players[player]["ELO"] = GetEloOf(players[player], player, players[player]["steamID"])

# Create the main window
root = tk.Tk()
root.title("Select Players and Create Teams")

# Initialize tkinter variables for checkboxes
player_vars = {player: tk.BooleanVar(value=False) for player in players}

# Create checkboxes and labels for each player
checkboxes = {}
for player in players:
    checkboxes[player] = tk.Checkbutton(root, text=player, variable=player_vars[player])
    checkboxes[player].pack(anchor=tk.W)

# Function to create teams based on selected players
def create_teams():
    selected_names = [player for player, var in player_vars.items() if var.get()]
    if len(selected_names) == 6:
        # Generate all possible combinations of 3 names out of the selected names
        combinations = list(itertools.combinations(selected_names, 3))

        # Initialize variables to track the best teams and their absolute difference
        best_team1 = []
        best_team2 = []
        min_absolute_difference = float('inf')

        # Iterate through all combinations and find the best teams
        for i in range(len(combinations) // 2):
            team1 = list(combinations[i])
            team2 = list(combinations[-(i + 1)])

            # Calculate the absolute difference between the two teams
            absolute_difference = sum(players[name]["ELO"] for name in team1) - sum(players[name]["ELO"] for name in team2)

            # Update the best teams if the absolute difference is minimized
            if abs(absolute_difference) < min_absolute_difference:
                min_absolute_difference = abs(absolute_difference)
                best_team1 = team1
                best_team2 = team2

        # Print the best teams and their ELO ratings
        print("Best Team 1:")
        for name in best_team1:
            print(f"{name}: {players[name]['ELO']}")
        print(f"Total ELO: {sum(players[name]['ELO'] for name in best_team1)}")

        print("\nBest Team 2:")
        for name in best_team2:
            print(f"{name}: {players[name]['ELO']}")
        print(f"Total ELO: {sum(players[name]['ELO'] for name in best_team2)}")
        print(f"ELO Difference: {sum(players[name]['ELO'] for name in best_team1) - sum(players[name]['ELO'] for name in best_team2)}")
    else:
        print("Please select 6 players.")

# Button to create teams
create_teams_button = tk.Button(root, text="Create Teams", command=create_teams)
create_teams_button.pack()

root.mainloop()
