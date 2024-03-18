import pickle
import json
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import List, Dict, Tuple


def prompt2obstacles(prompt: List[Dict[str, str]]) -> List[Tuple[float, float]]:
    prompt = prompt[1]["content"]
    str_list = prompt.split("\n")
    str_list = str_list[1:4]
    positions = []
    for s in str_list:
        i = 0
        while s[i] != "(":
            i += 1
        j = i
        while s[j] != ")":
            j += 1
        positions.append(eval(s[i : j + 1]))
    return positions


def json2trajectories(
    messages: Dict[str, List[Dict[str, str]]]
) -> List[Tuple[float, float]]:
    return eval(messages["messages"][2]["content"])


def plot(
    obstacles: List[Tuple], traj_real: List[Tuple], traj_pred: List[Tuple], name: str
):
    obstacle_width = 1.8
    obstacle_length = 4.9

    # define Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(15, 3))
    # background
    ax.axhline(26.6 - 3.5 / 2, c="white")
    ax.axhline((26.6 + 30) / 2, linestyle=(0, (20, 40)), c="white")
    ax.axhline((30 + 33.6) / 2, linestyle=(0, (20, 40)), c="white")
    ax.axhline((33.6 + 37.1) / 2, linestyle=(0, (20, 40)), c="white"),
    ax.axhline(37.1 + 3.5 / 2, c="white")
    # ax.axvline(-250, c="red", lw=3)
    ax.set_facecolor((211 / 255, 211 / 255, 211 / 255))
    p = Rectangle(
        (-250, 26.6 - 3.5 / 2),
        3,
        37.1 + 3.5 - 26.6,
        linewidth=0,
        fill=None,
        hatch="///",
    )
    ax.add_patch(p)
    # trajectories
    x, y = tuple(zip(*traj_real))
    ax.plot(x, y, c="blue", label="Ground Truth", lw=3)
    x, y = tuple(zip(*traj_pred))
    ax.plot(x, y, c="orange", label="Fine-tuned GPT-3.5", lw=3)
    ax.legend()
    # obstacles
    for obs in obstacles:
        ax.add_patch(
            Rectangle(
                (obs[0] - obstacle_length / 2, obs[1] - obstacle_width / 2),
                obstacle_length,
                obstacle_width,
                edgecolor="red",
                facecolor="silver",
                fill=False,
                lw=2,
            )
        )
    # remove axes
    # for spine in ax.spines.values():
    #     spine.set_visible(False)
    ax.tick_params(bottom=False, labelbottom=True, left=False, labelleft=False)
    ax.set_xticks([-325.3, -250], labels=["Start", "Finish"])
    plt.tight_layout()
    plt.savefig(f"{name}.png")
    plt.close()


def l1_loss(
    trajectory1: List[tuple[float, float]], trajectory2: List[tuple[float, float]]
) -> float:
    s = 0
    for p1, p2 in zip(trajectory1, trajectory2):
        s += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return s


def l2_loss(
    trajectory1: List[tuple[float, float]], trajectory2: List[tuple[float, float]]
) -> float:
    s = 0
    for p1, p2 in zip(trajectory1, trajectory2):
        s += np.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return s


def collision_rate(obstacles: List[Tuple], trajectory: List[Tuple]) -> float:
    total_count = -250 - (-325)
    collision_count = 0

    if trajectory[-1][0] < -250:
        trajectory[-1] = (-250, trajectory[-1][1])
    else:
        i = len(trajectory) - 1
        while trajectory[i][0] > -250:
            i -= 1
        i += 1
        trajectory = trajectory[: i + 1]
        trajectory[-1] = (-250, trajectory[-1][1])

    for i in range(1, len(trajectory)):
        tx0, ty0 = trajectory[i - 1][0], trajectory[i - 1][1]
        tx1, ty1 = trajectory[i][0], trajectory[i][1]
        if tx1 - tx0 == 0:
            continue
        slope = (ty1 - ty0) / (tx1 - tx0)
        for x in range(math.ceil(tx0), math.ceil(tx1)):
            y = (x - tx0) * slope + ty0
            for op in obstacles:
                if np.sqrt(np.square(x - op[0]) + np.square(y - op[1])) < 2.5:
                    collision_count += 1

    return collision_count / total_count, collision_count


if __name__ == "__main__":
    test_chat_pickle = "./test_chat_2_3.pickle"
    test_data_jsonl = "./jsonl/test_data_3.jsonl"
    plots_output_dir = "./plots_2_3"
    metrics_csv = "driving_metrics_2_3.csv"

    chats = pickle.load(open(test_chat_pickle, "rb"))
    prompts = chats["prompts"]
    answers = chats["answers"]
    trajectories_pred = []
    for i, ans in enumerate(answers):
        try:
            t = eval(ans)
        except:
            raise ValueError(f"the {i}-th answer failed")
        trajectories_pred.append(t)
    obstacles = []
    for prompt in prompts:
        obstacles.append(prompt2obstacles(prompt))

    with open(test_data_jsonl, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]

    trajectories_real = []
    for messages in dataset:
        trajectories_real.append(json2trajectories(messages))

    ############## DATA VAR NAME #############
    ##         obstacles: List[List[Tuple]] ##
    ## trajectories_pred: List[List[Tuple]] ##
    ## trajectories_real: List[List[Tuple]] ##
    ##########################################

    n_sample = len(obstacles)

    # Plots
    for i in range(n_sample):
        plot(
            obstacles[i],
            trajectories_real[i],
            trajectories_pred[i],
            f"{plots_output_dir}/{i}",
        )

    # L1 loss
    metrics_df = pd.DataFrame(
        columns=["l1_loss", "l2_loss", "collision_rate", "collision_count"],
        index=np.arange(n_sample),
    )
    for i in range(n_sample):
        metrics_df.loc[i, "l1_loss"] = l1_loss(
            trajectories_real[i], trajectories_pred[i]
        )
        metrics_df.loc[i, "l2_loss"] = l2_loss(
            trajectories_real[i], trajectories_pred[i]
        )
        rate, count = collision_rate(obstacles[i], trajectories_pred[i])
        metrics_df.loc[i, "collision_rate"] = rate
        metrics_df.loc[i, "collision_count"] = count
    metrics_df.to_csv(metrics_csv)

    print()
