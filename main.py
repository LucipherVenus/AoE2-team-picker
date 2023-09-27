import tkinter as tk
import itertools
import requests

# Names and profile ID-s of the players for AoE2.net API
names_and_ids = {
    "Lucipher": 677003,
    "Bowman": 288649,
    "zv": 2680347,
    "sandriko": 3153351,
    "guramata": 5462150,
    "purple": 238305,
    "dito": 2654497,
    "WhiteFatal": 3330863,
    "torkiel": 2931088,
    "abgdevzt": 8925314,
    "Nefro": 2673312,
    # "Urbifex": 1231321123121313129,
    # "the_kupre": 1231313213238
}

# Create the ELOS dictionary
# These are the default ELOS, they will be updated in real-time from AoE2.net
# These default ELOS are necessary in case of missing data from the website
ELOS = {
    "Lucipher": 1800,
    "Bowman": 1800,
    "Valchoka": 1700,
    "zv": 1700,
    "sandriko": 1550,
    "guramata": 1530,
    "purple": 1500,
    "dito": 1500,
    "Giorgilandia": 1300,
    "WhiteFatal": 1250,
    "torkiel": 1200,
    "Urbifex": 1100,
    "abgdevzt": 1000,
    "the_kupre": 1300,
    "Nefro": 900
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


print("get elo of", ELOS)

def Fill_Ellos():
    for i in names_and_ids:
        ELOS[i] = GetEloOf(names_and_ids[i])

print("fillElos", ELOS)

# Function to add a name to the selected list
def add_name(name):
    if name not in selected_names and len(selected_names) < 6:
        selected_names.append(name)
        selected_names_label.config(text=", ".join(selected_names))
        if len(selected_names) == 6:
            listbox.config(state=tk.DISABLED)
            add_button.config(state=tk.DISABLED)
print("add_name", ELOS)
# Function to calculate the absolute difference in ELO ratings between two teams
def calculate_absolute_difference(team1, team2):
    elo_team1 = sum(ELOS[name] for name in team1)
    elo_team2 = sum(ELOS[name] for name in team2)
    return abs(elo_team1 - elo_team2)


#______________________________________________________________________________________________________________________#

# Fill ELLO-S of the player in real-time using AoE2.net API
Fill_Ellos()

# Create the main window
root = tk.Tk()
root.title("Pick Names")

# Create a label to display available names
available_names_label = tk.Label(root, text="Available names:")
available_names_label.pack()

# Create a listbox to display the names
listbox = tk.Listbox(root)
for name in ELOS.keys():
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
        print(f"{name}: {ELOS[name]}")
    print(f"Total ELO: {sum(ELOS[name] for name in best_team1)}")

    print("\nBest Team 2:")
    for name in best_team2:
        print(f"{name}: {ELOS[name]}")
    print(f"Total ELO: {sum(ELOS[name] for name in best_team2)}")
    print(f"ELO Difference: {sum(ELOS[name] for name in best_team1) - sum(ELOS[name] for name in best_team2)}")

create_teams_button = tk.Button(root, text="Create Teams", command=create_teams)
create_teams_button.pack()

root.mainloop()
