#!/usr/bin/env python3

import zmq
import json
import os
import requests
from stressrnn import StressRNN

# URL of the exceptions file
EXCEPTIONS_URL = "https://ojisanshare.s3.amazonaws.com/stressrnn/exceptions.txt"
EXCEPTIONS_PATH = "/tmp/exceptions.txt"  # Temporary path to store the downloaded file

def download_exceptions_file():
    try:
        # Download the file
        response = requests.get(EXCEPTIONS_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(EXCEPTIONS_PATH, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded exceptions file to {EXCEPTIONS_PATH}")
    except Exception as e:
        print(f"Error downloading exceptions file: {e}")

# Download the exceptions file before starting the service
download_exceptions_file()

# Initialize StressRNN with the downloaded exceptions file
stress_rnn = StressRNN(EXCEPTIONS_PATH)

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
