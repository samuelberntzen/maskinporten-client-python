import json
import logging
import time
from urllib.parse import urlencode

import requests
from jwcrypto import jwk, jwt

from maskinporten.core.Generator import MaskinportenJWTGenerator


class MaskinportenClient:
    
    def __init__(
        self,
        token_url: str,
        scopes: list,
        audience: str,
        issuer: str,
        consumer_organization: str,
        private_key_json: dict = None,
        x509_private_key: str = None,
        exp_time_seconds: int = 10,
    ):
        """Client for retrieving access token from Maskinporten using either private key pair or x509 certificate.

        Args:
            token_url (str): The endpoint from which the access token is retrieved (e.g. "https://ver2.maskinporten.no/token").
            scopes (list): The scope of which the token encompasses.
            audience (str): The audience (e.g. "https://ver2.maskinporten.no/" for testing).
            issuer (str): The issuer of the token (e.g. your integration identificator in Maskinporten).
            consumer_organization (str): The consumer of the token, e.g. your organization number.
            private_key_json (dict): A dictionary representing your private key-pair. Public pair must be uploaded to Maskinporten.
            x509_private_key (str): The x509 private key of your organization. Defaults to None.
            exp_time_seconds (int, optional): The expiration time (seconds) of the token. Defined in Maskinporten. Value here determines if the client must generate a new token before the old expires Defaults to 10.
        """
        
        # Configuration
        self.token_url = token_url
        self.audience = audience
        self.issuer = issuer
        self.scopes = scopes
        self.consumer_organization = consumer_organization
        self.exp_time_seconds = exp_time_seconds

        # Set auth method
        self.jwt_method, self.auth = self._determine_jwt_method(private_key_json, x509_private_key)

        # Placeholder values for last token generation and jwt
        self.last_token_generate = False

        # Load the generator into the client object
        self.generator = MaskinportenJWTGenerator(
                config = {
                    'audience': self.audience,
                    'issuer': self.issuer,
                    'scopes':  self.scopes,
                    'consumer_organization': self.consumer_organization,
                    'exp_time_seconds': exp_time_seconds,
                },
                jwt_method = self.jwt_method,
                auth = self.auth
        )

        # Instantiate with non valid JWT because no JWT has been generated
        self.jwt_valid = False

    def __str__(self):
        return (
            f"MaskinportenClient(token_url={self.token_url}, "
            f"MaskinportenClient(audience={self.audience}, "
            f"MaskinportenClient(issuer={self.issuer}, "
            f"MaskinportenClient(scopes={self.scopes}, "
            f"MaskinportenClient(consumer_organization={self.consumer_organization}, "
            f"MaskinportenClient(exp_time_seconds={self.exp_time_seconds}, "
            f"MaskinportenClient(last_token_generate={self.last_token_generate}, "
        )

    def __repr__(self):
        return self.__str__()

    def _determine_jwt_method(self, private_key_json, x509_private_key) -> tuple:
        """
        Determine the authentication method based on the values of private_key_json and x509_private_key.

        Args:
        private_key_json (dict): The private key JSON data (or None if not provided).
        x509_private_key (str): The x509 certificate data (or None if not provided).

       Returns:
            tuple: A tuple containing determined auth method and credentials.

        Raises:
        ValueError: If both or neither of private_key_json and x509_certificate have values.
        """
        if private_key_json and not x509_private_key:
            return "private_key", private_key_json
        elif not private_key_json and x509_private_key:
            return "x509", x509_private_key
        elif private_key_json and x509_private_key:
            raise ValueError("Only one of private_key_json and x509_private_key should have a value.")
        else:
            raise ValueError("The instance is missing one of private_key_json and x509_private_key.")

    def get_jwt(self) -> jwt.JWT:
        """Generates a JWT to use for Maskinporten authentication

        Returns:
            jwt.JWT: JWT token from jwcrypto
        """
          
        
        if not self.jwt_valid:
            logging.info("Generating new token")
            jwt = self.generator.generate_jwt()
            self.last_token_generate = time.time()
            self.jwt = jwt

            self.jwt_valid = True
            return jwt
        
        # Otherwise previously generated token is still valid
        else:
              logging.info("JWT still valid. New generation not necessary.")
              print("JWT still valid. New generation not necessary.")
              return self.jwt
    

    def assert_jwt_valid(self) -> bool:
        """Checks if the current JWT is either expired or consumed

        Returns:
            bool: True if valid, false if expired
        """
        current_time = time.time()

        # If a generated token close to expiration or has already been used
        if (current_time >= self.last_token_generate + self.exp_time_seconds - 5) or not self.jwt_valid:
            return False
        
        # Otherwise JWT is still valid, unless it has been used
        return True

    def get_access_token(self) -> str:
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            str: _description_
        """

          # Use jwt_token to make request to maskinporten
        body = {
            "grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self.get_jwt()
        }

        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Accept": "*/*"
        }

        response = requests.post(
        url = self.token_url,
        data=urlencode(body),
        headers = headers
        )

        logging.info(f"Maskinporten response status code: {response.status_code}")

        # JWT is invalid after it has been used
        if response.status_code == 200:
            self.jwt_valid = False

        # Get data
        data = response.json()

        # Extract access_token
        access_token = data['access_token']

        return access_token