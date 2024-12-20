#!/usr/bin/python3

import argparse
import sys


def compose_simulation(num_env: int):
    pred_prey_services = [
        f"""
    predator-prey-service-{i}:
        image: ghcr.io/distributedmarlpredatorprey/predator-prey-service:main
        container_name: predator-prey-service-simulation-{i}
        hostname: predator-prey-{i}
        restart: always
        environment:
            <<: *common-variables
            RANDOM_SEED: {i}
        volumes:
            - ./config/:/usr/app/config/
            - ./data/predator_prey_service/environment_{i}/:/usr/app/src/main/resources/"""
        for i in range(num_env)
    ]

    prefix = """x-common-variables: &common-variables
    GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
    PYTHONUNBUFFERED: 1
    PROJECT_ROOT_PATH: /usr/app/
    MODE: simulation 

services:"""

    compose = prefix
    for pred_prey_service in pred_prey_services:
        compose = compose + pred_prey_service + "\n"

    print(compose)


def main():
    parser = argparse.ArgumentParser(
        description="Creates a Docker Compose file content to simulate multiple MARL Predator-Prey environments."
    )
    parser.add_argument(
        "--num_env",
        type=str,
        required=True,
        help="Number of environments to run in parallel.",
    )
    args = parser.parse_args()
    compose_simulation(int(args.num_env))
    print(
        "-----------------------------------------------------------------------------------",
        file=sys.stderr,
    )
    print(
        f"A Docker compose file content is generated for simulating {args.num_env} environments in parallel.",
        file=sys.stderr,
    )
    print(
        "-----------------------------------------------------------------------------------",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
