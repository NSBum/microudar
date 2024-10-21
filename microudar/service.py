#!/usr/bin/env python3

import zmq
from stressrnn import StressRNN

stress_rnn = StressRNN()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:43651")

def start_service():
	while True:
		message = socket.recv_json()
		text = message['sentence']
		
		stressed_text = stress_rnn.put_stress(text, stress_symbol='+', 
			accuracy_threshold=0.75, 
			replace_similar_symbols=True
		)
		socket.send_json({"result": stressed_text})
