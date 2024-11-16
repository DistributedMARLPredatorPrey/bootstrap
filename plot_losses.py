#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

df_pred_losses = pd.read_csv("./data/learner_service/df_predator_losses.csv", index_col=0)
df_prey_losses = pd.read_csv("./data/learner_service/df_prey_losses.csv", index_col=0)

# Print the results
def plot_critic_loss():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

    for title, losses, ax in [("Predator Critic Loss", df_pred_losses["pred_loss"], ax1), 
                            ("Prey Critic Loss", df_prey_losses["prey_loss"], ax2)]:
        
        episodes = list(range(len(losses)))
        error = list(losses)
        slope, intercept, r_value, p_value, std_err = linregress(episodes, error)

        print(f"{title} Regression line stats")
        print(f"\tSlope: {slope}")
        print(f"\tIntercept: {intercept}")
        print(f"\tR-squared: {r_value**2}")
        print(f"\tP-value: {p_value} (Significant: {p_value < 0.05})")
        print("------------------------------------")

        # Plot the data and regression line
        episodes = np.array(episodes)
        ax.scatter(episodes, error, label="Error values")
        ax.plot(
            episodes,
            intercept + slope * episodes,
            color="red",
            label=f"Regression line (slope: {slope:.4f}, p-value: {p_value:.4f})",
        )
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Loss")
        ax.set_title(title)

        ax.legend()
    plt.show()


if __name__ == "__main__":
    plot_critic_loss()
