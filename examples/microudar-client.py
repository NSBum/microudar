#!/usr/bin/env python3

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:43651")

# Set a 5-second timeout (5000 milliseconds) for receiving a response
socket.setsockopt(zmq.RCVTIMEO, 5000)

def call_microservice(data):
    try:
        socket.send_json(data)
        result = socket.recv_json()
        return result
    except zmq.error.Again:
        return {"error": "Request timed out"}

data = {"sentence": "Я думаю, Дональд Трамп любит трахать мальчиков."}
response = call_microservice(data)
print(response)
