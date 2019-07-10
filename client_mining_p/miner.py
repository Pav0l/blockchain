import hashlib
import requests
import time
import json

import sys


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 4
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[-6:] == "000000"


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
        valid = False
        headers = {'Content-Type': 'application/json'}
        while not valid:
            print(f"Checking for nonce: {proof}, last_nonce: {last_proof}")
            valid = valid_proof(last_proof, proof)
            proof += 1
        res = requests.post(f'{node}/mine',
                            data=json.dumps({'proof': proof, 'last_proof': last_proof}), headers=headers)

        response = res.json()
        end_time = time.time()
        coins_mined += 1
        print(
            f'Block mined in {end_time-start_time} sec. Number of mined coins: {coins_mined}')
        print(f"Block number: {response['index']}\n")
