#!/usr/bin/python3


pred_prey_services = [f"""
    predator-prey-service-{i}:
        image: predator-prey-service
        container_name: predator-prey-service-{i}
        hostname: predator-prey-service-{i}
        depends_on:
            rabbitmq:
                condition: service_healthy
        environment:
            PYTHONUNBUFFERED: 1
            GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
            REPLAY_BUFFER_HOST: replay-buffer
            REPLAY_BUFFER_PORT: 80
            BROKER_HOST: rabbitmq-broker
            REL_PATH: {i}
        healthcheck:
            test: python3 -m src.main.controllers.policy.predator_prey.actor_receiver_healthcheck
            interval: 2s
            timeout: 5s
            retries: 10
        volumes:
            - ../ds-project-fabri-ay2223/:/usr/app/
            - ./config/:/usr/app/config/
            #- ./config/config.yaml:/usr/app/config/config.yaml
    """ for i in range(5)]

prefix = """
version: '3'

services:

    rabbitmq:
        image: "rabbitmq:3-management"
        container_name: "rabbitmq-broker"
        hostname: "rabbitmq-broker"
        ports:
            - "5672:5672"  # RabbitMQ main port
            - "15672:15672"  # RabbitMQ management plugin port
        volumes:
            - rabbitmq_data:/var/lib/rabbitmq
        healthcheck:
            test: rabbitmq-diagnostics -q ping
            interval: 5s
            timeout: 10s
            retries: 1

    replay-buffer-service:
        image: replay-buffer #ghcr.io/distributedmarlpredatorprey/replay-buffer-service:release-0.2.0
        container_name: replay-buffer-service
        hostname: replay-buffer
        environment:
            PYTHONUNBUFFERED: 1
            GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
            PREDATOR_DATASET_PATH: /usr/app/dataset/predator_data1.csv
            PREY_DATASET_PATH: /usr/app/dataset/prey_data1.csv
        volumes:
            - ./config/config.yaml:/usr/app/config/config.yaml
            - ./config/replay-buffer/:/usr/app/dataset/
            - ../replay-buffer-service/:/usr/app/

"""

learner_dependencies = ""
for i in range(len(pred_prey_services)):
    dep = f"""
            predator-prey-service-{i}:
                condition: service_healthy
    """
    learner_dependencies = learner_dependencies + dep

suffix = f"""
    pred-learner-service:
        image: learner-service
        container_name: pred-learner-service
        hostname: pred-learner
        depends_on:
            rabbitmq:
                condition: service_healthy
            {learner_dependencies}
        environment:
            PYTHONUNBUFFERED: 1
            GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
            AGENT_TYPE: predator
            BATCH_SIZE: 64
            REPLAY_BUFFER_HOST: replay-buffer
            REPLAY_BUFFER_PORT: 80
            BROKER_HOST: rabbitmq-broker
        volumes:
            - ./config/config.yaml:/usr/app/config/config.yaml
            - ../learner-service/:/usr/app/

    prey-learner-service:
        image: learner-service
        container_name: prey-learner-service
        hostname: prey-learner
        depends_on:
            rabbitmq:
                condition: service_healthy
            {learner_dependencies}
        environment:
            PYTHONUNBUFFERED: 1
            GLOBAL_CONFIG_PATH: /usr/app/config/config.yaml
            AGENT_TYPE: prey
            BATCH_SIZE: 64
            REPLAY_BUFFER_HOST: replay-buffer
            REPLAY_BUFFER_PORT: 80
            BROKER_HOST: rabbitmq-broker
        volumes:
            - ./config/config.yaml:/usr/app/config/config.yaml
            - ../learner-service/:/usr/app/

volumes:
    rabbitmq_data:
"""

compose = prefix
for pred_prey_service in pred_prey_services:
    compose = compose + pred_prey_service + "\n"

compose = compose + suffix
print(compose)

