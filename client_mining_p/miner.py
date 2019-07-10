import hashlib
import requests
import time

import sys


# Implement functionality to search for a proof
if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    proof = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server and look for a new one
        lp_response = requests.get(f'{node}/last_proof')
        body = lp_response.json()
        last_proof = body['last_proof']

        # Search new proof
        print('Mining new block')
        start_time = time.time()
        valid_proof = False
        headers = {'Content-Type': 'application/json'}
        while not valid_proof:
            print(f"Checking for proof: {proof}, last_proof: {last_proof}")
            res = requests.post(f'{node}/mine',
                                data={'proof': proof, 'last_proof': last_proof}, headers=headers)
            code = res.status_code
            response = res.json()
            if code == 200:
                valid_proof = True
            else:
                proof += 1
        end_time = time.time()
        coins_mined += 1
        print(
            f'Block mined in {end_time-start_time} sec. Number of mined coins: {coins_mined}')
        print(f"Block number: {response['index']}\n")
