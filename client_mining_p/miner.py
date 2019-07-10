import hashlib
import requests

import sys


# Implement functionality to search for a proof
def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    response = 401
    while response == 200:
        res = requests.post("http://localhost:5000/mine",
                            body={'proof': proof, 'last_proof': last_proof})
        response = res.status_code
        proof += 1

    return proof


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

        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        break
