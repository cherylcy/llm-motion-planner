import os
import pickle
from collections import defaultdict

data = pickle.load(open("success_routes2.pickle", "rb"))
obstacles = data["obstacles"]
trajectories = data["trajectories"]
n_sample = len(obstacles)

# length_count = defaultdict(int)
# for t in trajectories:
#     length_count[len(t)] += 1

# for i in range(n_sample):
#     traj = trajectories[i]
#     n_point = len(traj)
#     if n_point == 14:
#         distance = []
#         for i in range(1, n_point):
#             x_dist = round(traj[i][0] - traj[i - 1][0])
#             y_dist = abs(round(traj[i][1] - traj[i - 1][1]))
#             distance.append((x_dist, y_dist))
#         print(distance)
#         # print(traj)

# 1. cut trajectories with longer than 10
trajectories2 = []
for i in range(n_sample):
    traj = trajectories[i]
    n_point = len(traj)
    if n_point >= 10:
        traj2 = [traj[0]]
        for i in range(1, n_point):
            x_dist = round(traj[i][0] - traj[i - 1][0])
            y_dist = abs(round(traj[i][1] - traj[i - 1][1]))
            if not (x_dist < 2 and y_dist == 0):
                traj2.append(traj[i])
        traj = traj2
    trajectories2.append(traj)

# length_count = defaultdict(int)
# for t in trajectories2:
#     length_count[len(t)] += 1

# for i in range(n_sample):
#     traj = trajectories2[i]
#     n_point = len(traj)
#     if n_point == 9:
#         # distance = []
#         # for i in range(1, n_point):
#         #     x_dist = round(traj[i][0] - traj[i - 1][0])
#         #     y_dist = abs(round(traj[i][1] - traj[i - 1][1]))
#         #     distance.append((x_dist, y_dist))
#         # print(distance)
#         print(traj)

# 2. add points to trajectores shorter than 10
for i in range(n_sample):
    traj = trajectories2[i]
    n_point = len(traj)
    if n_point == 7:
        traj.insert(1, (traj[0][0] + 1, traj[0][1]))
    n_point = len(traj)
    if n_point == 8:
        traj.insert(8, (traj[-1][0] + 7, traj[-1][1]))
    n_point = len(traj)
    if n_point == 9:
        traj.insert(9, (traj[-1][0] + 3, traj[-1][1]))
    trajectories2[i] = traj

# 3. make all the trajectories pass through -250
for i in range(n_sample):
    traj = trajectories2[i]
    if traj[-1][0] < -250:
        trajectories2[i][-1] = (-(249 + abs(traj[-1][0]) % 1), traj[-1][1])

# length_count = defaultdict(int)
# for t in trajectories2:
#     length_count[len(t)] += 1

# for i in range(n_sample):
#     traj = trajectories2[i]
#     # n_point = len(traj)
#     # distance = []
#     # for i in range(1, n_point):
#     #     x_dist = round(traj[i][0] - traj[i - 1][0])
#     #     y_dist = abs(round(traj[i][1] - traj[i - 1][1]))
#     #     distance.append((x_dist, y_dist))
#     # print(distance)
#     print(traj)

# round all points to 1 decimal point
for i in range(n_sample):
    for j in range(10):
        p = trajectories2[i][j]
        trajectories2[i][j] = (round(p[0], 1), round(p[1], 1))

data = {"obstacles": obstacles, "trajectories": trajectories2}
pickle.dump(data, open("aligned_routes2.pickle", "wb"))
