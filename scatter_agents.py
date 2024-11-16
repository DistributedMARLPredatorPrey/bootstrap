#!/usr/bin/python3

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from celluloid import Camera

experiment_data_path: str = os.path.join("data", "predator_prey_service")
blue_cmap = plt.cm.Blues
red_cmap = plt.cm.Reds


def scatter_agents(idx: int, num_predators: int, num_preys: int):
    """
    Scatters Agents
    :param idx: Environment Id
    :param num_predators: Number of predators inside the environment
    :param num_preys: Number of preys inside the environment
    :return:
    """

    coordinates_path = os.path.join(
        experiment_data_path, f"environment_{idx}", "positions.csv"
    )
    rewards_path = os.path.join(
        experiment_data_path, f"environment_{idx}", "rewards.csv"
    )

    df_coordinates: pd.DataFrame = pd.read_csv(coordinates_path)
    df_rewards: pd.DataFrame = pd.read_csv(rewards_path)

    x_coord = [col for col in df_coordinates.columns if col.startswith("x")]
    y_coord = [col for col in df_coordinates.columns if col.startswith("y")]
    reward_cols = [col for col in df_rewards.columns if col.startswith("r")]

    # Scatter
    camera = Camera(plt.figure())
    plt.title(f"Predator-Prey Environment {idx}")

    plt.scatter([], [], color=blue_cmap(100), label="Preys")
    plt.scatter([], [], color=red_cmap(100), label="Predators")
    plt.legend()

    for i in range(len(df_rewards)):
        x = df_coordinates[x_coord].loc[i]
        y = df_coordinates[y_coord].loc[i]
        r = df_rewards[reward_cols].loc[i]

        x_pred, y_pred, r_pred = (
            x[:num_predators],
            y[:num_predators],
            r[:num_predators],
        )
        x_prey, y_prey, r_prey = (
            x[num_predators:],
            y[num_predators:],
            r[num_predators:],
        )

        plt.scatter(
            x_pred,
            y_pred,
            c=[red_cmap(int((r + 1000) / 10)) for r in r_pred],
            s=200 * np.pi,
            marker="o",
        )
        for i in range(len(x_pred)):
            plt.text(
                x_pred.iloc[i] + 0.1, y_pred.iloc[i], round((r_pred.iloc[i] + 1000), 2), fontsize=12
            )  # Offset x[i] for better readability
        #
        plt.scatter(
            x_prey,
            y_prey,
            c=[blue_cmap(int((r + 1000) / 10)) for r in r_prey],
            s=200 * np.pi,
            marker="o",
        )
        for i in range(len(x_prey)):
            plt.text(
                x_prey.iloc[i] + 0.1, y_prey.iloc[i], round((r_prey.iloc[i] + 1000), 2), fontsize=12
            )  # Offset x[i] for better readability

        camera.snap()

    anim = camera.animate(blit=True)
    plt.show()
    # Decomment to save the video
    # anim.save("scatter.mp4")


def main():
    parser = argparse.ArgumentParser(
        description="Scatter agents of an environment whose ID is provided as parameter."
    )
    parser.add_argument(
        "--env_idx",
        type=int,
        required=True,
        help="Index of the environment to be scattered.",
    )
    parser.add_argument(
        "--num_predators",
        type=int,
        required=True,
        help="Number of predators inside the environment",
    )
    parser.add_argument(
        "--num_preys",
        type=int,
        required=True,
        help="Number of preys inside the environment",
    )

    args = parser.parse_args()
    scatter_agents(
        idx=args.env_idx, num_predators=args.num_predators, num_preys=args.num_preys
    )


if __name__ == "__main__":
    main()
