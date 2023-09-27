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
}


# Define the API endpoint
def GetEloOf(id):

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

        # Return the ELO of the given player
        print(data['leaderboard'][0]['name'], '-', data['leaderboard'][0]['rating'])
        return data['leaderboard'][0]['rating']

    else:
        return -99999999


def Fill_Ellos():
    for i in players:
        players[i]["ELO"] = GetEloOf(players[i]["steamID"])


# Function to add a name to the selected list
def add_name(name):
    if name not in selected_names and len(selected_names) < 6:
        selected_names.append(name)
        selected_names_label.config(text=", ".join(selected_names))


def calculate_absolute_difference(team1, team2):
    elo_team1 = sum(players[name]["ELO"] for name in team1)
    elo_team2 = sum(players[name]["ELO"] for name in team2)
    return abs(elo_team1 - elo_team2)


#______________________________________________________________________________________________________________________#

# Fill ELLO-S of the players in real-time using AoE2.net API
Fill_Ellos()

# Create the main window
root = tk.Tk()
root.title("Pick Names")

# Create a label to display available names
available_names_label = tk.Label(root, text="Available names:")
available_names_label.pack()

# Create a listbox to display the names
listbox = tk.Listbox(root)
for name in players.keys():
    listbox.insert(tk.END, name)
listbox.pack()

# Create a button to add the selected name
add_button = tk.Button(root, text="Add Name", command=lambda: add_name(listbox.get(tk.ACTIVE)))
add_button.pack()

# Create a label to display selected names
selected_names_label = tk.Label(root, text="Selected names:")
selected_names_label.pack()

# Initialize the list of selected names
selected_names = []

# Create a button to create two teams based on the rules
def create_teams():
    if len(selected_names) != 6:
        return  # Ensure exactly 6 names are selected before creating teams

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
        absolute_difference = calculate_absolute_difference(team1, team2)

        # Update the best teams if the absolute difference is minimized
        if absolute_difference < min_absolute_difference:
            min_absolute_difference = absolute_difference
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

create_teams_button = tk.Button(root, text="Create Teams", command=create_teams)
create_teams_button.pack()

root.mainloop()
