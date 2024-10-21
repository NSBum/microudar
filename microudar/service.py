#!/usr/bin/env python3

import zmq
import json
from stressrnn import StressRNN

stress_rnn = StressRNN()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:43651")

def log_request(message):
    text = message.get('sentence', '')
    # Get the length of the JSON payload in bytes
    payload_length = len(json.dumps(message).encode('utf-8'))
    
    # Extract the first three words from the sentence
    first_three_words = ' '.join(text.split()[:3]) + "..." if len(text.split()) > 3 else text
    
    # Log the information (since we're not handling IP here, skip that for now)
    print(f"Rcd req len: {payload_length} | '{first_three_words}'")

def start_service():
    print("microudar running on tcp://127.0.0.1:43651")
    while True:
        try:
            message = socket.recv_json()
            # Log the request
            log_request(message)
        except ValueError:
            print("Invalid JSON received")
            continue
        except Exception as e:
            print(f"Error occurred: {e}")
            continue
        
        text = message.get('sentence', '')
        
        # Process the sentence with StressRNN
        stressed_text = stress_rnn.put_stress(text, stress_symbol='+', 
            accuracy_threshold=0.75, 
            replace_similar_symbols=True
        )
        
        # Send the processed response
        socket.send_json({"result": stressed_text})

if __name__ == "__main__":
    start_service()
