import os
import pickle
from dotenv import load_dotenv

load_dotenv()

data_dir = os.getenv("DATA_DIR")
obstacles = []
trajectories = []
for datafile_idx in range(5, 9):
    file = open(os.path.join(data_dir, f"NLP dataset {datafile_idx}.txt"), "r")
    text = file.read()
    blocks = text.split("\n\n")
    for i in range(len(blocks)):
        if len(blocks[i]) == 0:
            continue
        lines = blocks[i].split("\n")
        if i % 2 == 0:
            if datafile_idx == 1:
                lines = lines[1:]
            else:
                lines = lines[2:]
            obstacles.append("\n".join(lines))
        else:
            line = lines[1]
            trajectory = []
            x, y = "", ""
            i = 0
            while i < len(line):
                if line[i] == "(":
                    j = i + 1
                    while line[j] != ",":
                        x += line[j]
                        j += 1
                    j += 2
                    while line[j] != ")":
                        y += line[j]
                        j += 1
                    trajectory.append((float(x), float(y)))
                    x, y = "", ""
                    i = j
                i += 1
            trajectories.append(trajectory)

obstacles2 = []
trajectories2 = []
for i in range(len(obstacles)):
    if trajectories[i][-1][0] < -270:
        continue
    obstacles2.append(obstacles[i])
    trajectories2.append(trajectories[i])

success_routes = {"obstacles": obstacles2, "trajectories": trajectories2}
pickle.dump(success_routes, open("success_routes2.pickle", "wb"))
