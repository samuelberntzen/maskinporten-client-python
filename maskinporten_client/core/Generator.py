import base64
import logging
import time
import uuid

from jwcrypto import jwk, jwt


class MaskinportenJWTGenerator:
    def __init__(self, config: dict, jwt_method: str, auth: dict):
        """_summary_

        Args:
            config (dict): _description_
            jwt_method (str): _description_
            auth (dict): _description_
        """

        self.config = config
        self.jwt_method = jwt_method
        self.auth = auth
        
    def __str__(self):
        return f"MaskinportenJWTGenerator(public_attribute={self.config})"

    def __repr__(self):
        return self.__str__()

    def generate_claims(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        issue_time = int(time.time())
        expiration_time = issue_time + self.config["exp_time_seconds"]

        claims = {
            'aud': self.config['audience'],
            'iss': self.config['issuer'],
            'scope': ' '.join(self.config['scopes']),
            'consumer_org': self.config['consumer_organization'],
            'jti': str(uuid.uuid4()),
            'iat': issue_time,
            'exp': expiration_time
        }

        return claims 

    def jwt_private_key(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """

        # Create JWK and get key id 
        key = jwk.JWK(**self.auth)
        kid = self.auth['kid']

        claims = self.generate_claims()

        header = {
            'alg': 'RS256',
            'kid': kid
        }

        token = jwt.JWT(header=header, claims=claims)
        token.make_signed_token(key)
        return token.serialize()
    
    def jwt_x509(self) -> str:
        # Not supported
        pass
    
    def generate_jwt(self) -> str:
        """_summary_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """

        logging.info(f"JWT method is {self.jwt_method}")

        if self.jwt_method == "private_key":
            token = self.jwt_private_key() 
        elif self.jwt_method == "x509":
            token = self.jwt_x509() 

        else:
            raise ValueError(f"Invalid authentication method. Must be one of 'private_key' or 'x509'. Received {self.jwt_method}")

        return token 