#!/usr/bin/python3

import argparse
import sys


def compose_train(num_env: int):
    pred_prey_services = [
        f"""
    predator-prey-service-{i}:
        image: ghcr.io/distributedmarlpredatorprey/predator-prey-service:main
        container_name: predator-prey-service-training-{i}
        hostname: predator-prey-{i}
        restart: always
        depends_on:
            rabbitmq:
                condition: service_healthy
        environment:
            <<: *common-variables
            RANDOM_SEED: {i}
        healthcheck:
            test: python3 -m src.main.controllers.agents.policy.predator_prey.actor_receiver_healthcheck
            interval: 2s
            timeout: 5s
            retries: 10
        volumes:
            - ./config/:/usr/app/config/
            - ./data/predator_prey_service/environment_{i}/:/usr/app/src/main/resources/
        """
        for i in range(num_env)
    ]

    prefix = """x-common-variables: &common-variables
    GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
    PYTHONUNBUFFERED: 1
    REPLAY_BUFFER_HOST: replay-buffer
    REPLAY_BUFFER_PORT: 80
    BROKER_HOST: rabbitmq-broker
    PROJECT_ROOT_PATH: /usr/app/
    MODE: train

services:
    rabbitmq:
        image: rabbitmq:3-management
        container_name: rabbitmq-broker
        hostname: rabbitmq-broker
        restart: always
        environment:
            RABBITMQ_HEARTBEAT: 60
        volumes:
            - rabbitmq_data:/var/lib/rabbitmq
        healthcheck:
            test: rabbitmq-diagnostics -q ping
            interval: 5s
            timeout: 10s
            retries: 1

    replay-buffer-service:
        image: ghcr.io/distributedmarlpredatorprey/replay-buffer-service:main
        container_name: replay-buffer-service
        hostname: replay-buffer
        restart: always
        environment:
            <<: *common-variables            
        volumes:
            - ./config/config.yaml:/usr/app/config/config.yaml
            - ./data/replay-buffer-service/:/usr/app/src/main/resources/
    """

    learner_dependencies = ""
    for i in range(len(pred_prey_services)):
        dep = f"""predator-prey-service-{i}:
                condition: service_healthy
            """
        learner_dependencies = learner_dependencies + dep

    suffix = f"""
    learner-service:
        image: ghcr.io/distributedmarlpredatorprey/learner-service:main
        container_name: learner-service
        hostname: learner
        restart: always
        depends_on:
            rabbitmq:
                condition: service_healthy
            {learner_dependencies}
        environment:
            <<: *common-variables
            BATCH_SIZE: 64
        volumes:
            - ./data/learner_service/:/usr/app/src/main/resources/loss/
            - ./config/config.yaml:/usr/app/config/config.yaml
volumes:
    rabbitmq_data:
    """

    compose = prefix
    for pred_prey_service in pred_prey_services:
        compose = compose + pred_prey_service

    compose = compose + suffix
    print(compose)


def main():
    parser = argparse.ArgumentParser(
        description="Creates a Docker Compose file content to train multiple MARL Predator-Prey environments."
    )
    parser.add_argument(
        "--num_env",
        type=str,
        required=True,
        help="Number of environments to run in parallel.",
    )
    args = parser.parse_args()
    compose_train(int(args.num_env))
    print(
        "-----------------------------------------------------------------------------------",
        file=sys.stderr,
    )
    print(
        f"A Docker compose file content is generated for training {args.num_env} environments in parallel.",
        file=sys.stderr,
    )
    print(
        "-----------------------------------------------------------------------------------",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
