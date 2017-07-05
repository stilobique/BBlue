import os
import json
# -----------------------------
# Generate all data needs to know enviroment we want build, the stadium
# name, suffix name and -by deduction the path
# -----------------------------
levels_dict = {
    # Gymnasium
    1: ('GYM01', 'SanJuanTheater'),
    2: ('GYM02', 'MittelbrunnZentrum'),
    # Stadium
    3: ('STA01', 'UmmDharbStadium'),
    4: ('STA02', 'ManzoVBArena'),
    5: ('STA03', 'BanKhaemSporthall'),
    6: ('STA04', 'HosojimiCenter'),
    7: ('STA05', 'CharlesFrabetStadium'),
    8: ('STA06', 'JalbarosCenterArena'),
    9: ('STA07', 'CuapixcoEsteColegio'),
    10: ('STA08', 'AbramCenterStadium'),
    11: ('STA09', 'PretovkaClubStadion'),
    # Training Courts
    12: ('TC01', 'RoyalStratfordGymnasium'),
    13: ('TC02', 'MartinSherpardHall'),
}

slave = {
    1: ('Aurel', 'DESKTOP-O6QPOKM'),
    2: ('Quentin', 'MUTTON03'),
    3: ('Marine', 'WHITESHEEP02'),
}
revisions = []

path_json = os.path.abspath(
    "BatchLightUE4/Models/setup.json")

if os.path.isfile(path_json):
    with open(path_json) as f:
        paths_dict = json.load(f)

else:
    paths_dict = {
        "UE4 Editor": "UE4Editor.exe",
        "UE4 Project": "Project.uproject",
    }
