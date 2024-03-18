import pickle
import jsonlines

data = pickle.load(open("aligned_routes2.pickle", "rb"))
system_prompt = open("./prompts/system.txt", "r").read()


obstacles = data["obstacles"]
trajectories = data["trajectories"]
n_sample = len(obstacles)

n_split = round(n_sample * 0.8)
train_obstacles = obstacles[:n_split]
train_trajectories = trajectories[:n_split]
test_obstacles = obstacles[n_split:]
test_trajectories = trajectories[n_split:]


def create_dataset(train_or_test: str):
    if train_or_test not in ["train", "test"]:
        raise ValueError('train_or_test should be "train" or "test"')
    if train_or_test == "train":
        obst = train_obstacles
        traj = train_trajectories
    else:
        obst = test_obstacles
        traj = test_trajectories
    with jsonlines.open(f"{train_or_test}_data.jsonl", "w") as writer:
        for i in range(len(obst)):
            messages = []
            messages.append({"role": "system", "content": system_prompt})
            messages.append(
                {
                    "role": "user",
                    "content": f"Perception:\n{obst[i]}\nStarting point:\n{traj[i][0]}",
                }
            )
            messages.append({"role": "assistant", "content": f"{traj[i]}"})
            writer.write({"messages": messages})


create_dataset("train")
create_dataset("test")
