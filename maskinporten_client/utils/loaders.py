import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def load_private_key_from_json(path: str) -> dict:
    """Helper function for loading private key from a json file

    Args:
        path (str): The path of the JSON private key file

    Returns:
        dict: A dictionary containing your private key
    """

    # Load private key json
    with open(path, 'r') as f:
        private_key_json = json.load(f)

    return private_key_json

def load_private_key_from_pem(path: str) -> str:
    """
    Load a private key from a PEM file.

    Args:
        path_to_pem (str): Path to the PEM file containing the private key.

    Returns:
        Private key object suitable for signing operations.
    """
    with open(path, "rb") as pem_file:
        private_key = serialization.load_pem_private_key(
            pem_file.read(),
            password=None,  # Provide a password here if the PEM file is encrypted
            backend=default_backend()
        )
    return private_key
