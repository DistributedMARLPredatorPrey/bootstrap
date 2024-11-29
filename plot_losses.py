#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_pred_losses = pd.read_csv("./data/learner_service/df_predator_losses.csv", index_col=0)
df_prey_losses = pd.read_csv("./data/learner_service/df_prey_losses.csv", index_col=0)

# Print the results
def plot_critic_loss():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for title, losses, ax in [("Predator Critic Loss", df_pred_losses["pred_loss"], ax1), 
                            ("Prey Critic Loss", df_prey_losses["prey_loss"], ax2)]:
        
        episodes = list(range(len(losses)))
        error = list(losses)

        # Plot the data and regression line
        episodes = np.array(episodes)
        ax.scatter(episodes, error, label="Error values")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Loss")
        ax.set_title(title)

        ax.legend()
    plt.show()


if __name__ == "__main__":
    plot_critic_loss()
