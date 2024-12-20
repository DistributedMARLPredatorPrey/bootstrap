# Bootstrap

The bootstrap of the project.

This repository contains all the use cases of the *Distributed MARL Predator-Prey* Project.
It allows you to:
1. Train the MARL System. Agents' experiences are collected from multiple parallel environments and integrated into a centralized dataset, ultimately used for the learning process.
2. Simulate multiple Predator-Prey MARL environments, if a previous training phase has been completed;
3. Plot the agents of an environment in a 2D scatterplot animation;
4. Plot the Critic network loss tendency over time.

## Prerequisites

- Make sure you have a running and active version of [Docker](https://docs.docker.com/engine/install/);
- Setup a Python3 Virtualenv and install the dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Use cases

### Train MARL System by parallelizing the environments
1. Create a Docker compose file by specifying the number Predator-Prey environments to parallelize:
 ```bash
 python3 compose_training.py --num_env 5 > docker-compose-training.yaml
 ```
2. Configure the environments by specifying the parameters inside the `config/config.yaml` file. The default configuration is:
 
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
     
### Run multiple Predator-Prey environments in simulation mode
   
1. Create a Docker compose file by specifying the number Predator-Prey environments to parallelize:
   ```bash
   python3 compose_simulation.py --num_env 5 > docker-compose-simulation.yaml
   ```
2. Run the simulations in parallel:
   ```bash
   docker compose -f docker-compose-simulation.yaml up
   ```
### Animate the agents of an environment
Run the following command after or during a training phase:
```bash
python3 scatter_agents.py --env_idx 0 --num_predators 5 --num_preys 5
```
You should specify the index of the environment and the number of predators and preys that has been chosen.

### Plot the Critic model loss tendency over time
```bash
python3 plot_losses.py
```

## License

Bootstrap is licensed under the GNU v3.0 License. See the [LICENSE](./LICENSE) file for details.

## Author

- Luca Fabri ([w-disaster](https://github.com/w-disaster))
