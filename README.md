# Bootstrap

The bootstrap of the project.

This repository contains all the use cases of the *Distributed MARL Predator-Prey* Project.
It allows you to:
1. Train two separate MARL models for Predator and Preys. Using a data augmentation approach, agents' experiences are collected from multiple parallel environments.
2. Simulate multiple Predator-Prey MARL environments, if a previous training phase is completed;
3. Plot the agents of an environment in a 2D scatterplot;
4. Plot the Critic network loss tendency over time.

## Prerequisites

- Make sure you have a running and active version of [Docker](https://docs.docker.com/engine/install/).

## Usage:

1. Clone the repository and change directory:
    ```bash
    git clone git@github.com:DistributedMARLPredatorPrey/bootstrap.git && cd bootstrap
    ```
2. To train two MARL models using data augmentation:
  1. Create a Docker compose file by specifying the number Predator-Prey environments to parallelize:
     ```bash
     python3 compose_training.py --num_env 5 > docker-compose-training.yaml
     ```
  2. Configure the environments by specifying its parameters inside the `config/config.yaml` file. The default configuration is:
     
     ```yaml
     environment:
       x_dim: 250 # X dimension
       y_dim: 250 # Y dimension
       num_predators: 5 # Number of predators
       num_preys: 5 # Number of preys
       num_states: 30 # Observation space of the agent
       r: 10 # Radius of the agent
       vd: 250 # Visual Depth of the agent
       life: 200 # Predator's life in episodes
       save_experiment_data: true # Save experiment data
     ```
  3. Run the training phase:
     ```bash
     docker compose -f docker-compose-training.yaml up
     ```
3. To run multiple Predator-Prey environments in simulation mode:
   1. Create a Docker compose file by specifying the number Predator-Prey environments to parallelize:
       ```bash
       python3 compose_simulation.py --num_env 5 > docker-compose-simulation.yaml
       ```
   2. Run the simulations in parallel:
       ```bash
       docker compose -f docker-compose-simulation.yaml up
       ```
4. To scatter the agents of an environment, specify the index of the environment, as well as the number of predators and preys that has been chosen: 
    ```bash
    python3 scatter_agents.py --env_idx 0 --num_predators 5 --num_preys 5
    ```
5. To analyze the Critic model loss tendency over time (of both Predator and Prey's network), run the following command after or during a training phase:
   ```bash
   python3 plot_losses.py
   ```

## License

Bootstrap is licensed under the GNU v3.0 License. See the [LICENSE](./LICENSE) file for details.

## Author

- Luca Fabri ([w-disaster](https://github.com/w-disaster))
