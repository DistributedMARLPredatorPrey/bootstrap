#!/usr/bin/python3


pred_prey_services = [f"""
    predator-prey-service-{i}:
        image: predator-prey-service #ghcr.io/distributedmarlpredatorprey/predator-prey-service:release-0.2.0
        container_name: predator-prey-service-{i}
        hostname: predator-prey-service-{i}
        environment:
            PYTHONUNBUFFERED: 1
            GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
            REPLAY_BUFFER_HOST: replay-buffer
            REPLAY_BUFFER_PORT: 80
            BROKER_HOST: rabbitmq-broker
            REL_PATH: {i}
            RANDOM_SEED: {i}
            MODE: simulation 
        volumes:
            - ../predator-prey-service/venv/:/usr/app/venv/
            - ../predator-prey-service/:/usr/app/
            - ./config/:/usr/app/config/
            #- ./config/config.yaml:/usr/app/config/config.yaml
    """ for i in range(8)]

prefix = """
version: '3'

services:

"""

compose = prefix
for pred_prey_service in pred_prey_services:
    compose = compose + pred_prey_service + "\n"

print(compose)
