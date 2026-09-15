# Week 1 - Sept 14 - Sept 20

# Technical implementation Questions

## How do we set up a queue on server start for use later?

We establish the connection and declare queue on server start. We create a publisher object and assign it to be part of app state for use in request calls!

## For RabbitMQ, how do the concepts of environment, connection, and channel relate?

An environment houses configuration for a series of connections, a connection is like it sounds - a connection between RabbitMQ and a client.

For AMPQ 0-9-1 a channel is a lightweight connection inside a TCP connection.

- Multiple channels can share the TCP connection.
- Client performs sending/recieving/acknowledging.

AMPQ 1-0 has sessions - provides links to send and recieve messages. A session groups communication and manages flow control.

# How do we ensure that messages are finished by the worker?

We can use [message acknowledgements](https://www.rabbitmq.com/tutorials/tutorial-two-python#message-acknowledgment) to determine when an item is to be dequeued from list.
