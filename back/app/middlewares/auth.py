import base64
import os
from typing import Annotated

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from app.core.config import settings
from app.core.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


def jwk_to_pem(jwk: dict) -> str:
    exponent_bytes = base64.urlsafe_b64decode(jwk["e"] + "=" * (4 - len(jwk["e"]) % 4))
    modulus_bytes = base64.urlsafe_b64decode(jwk["n"] + "=" * (4 - len(jwk["n"]) % 4))
    exponent_int = int.from_bytes(exponent_bytes, "big")
    modulus_int = int.from_bytes(modulus_bytes, "big")

    public_numbers = rsa.RSAPublicNumbers(n=modulus_int, e=exponent_int)
    public_key = public_numbers.public_key(backend=default_backend())

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem.decode("utf-8")


def verify_token(token: str):
    # Get the public key set
    #keys_response = requests.get(settings.KEY_SET_URL)
    #keys_response.raise_for_status()
    #keys = keys_response.json()
    return 
    # Get the header from the token to find the correct key
    #header = jwt.get_unverified_header(token)
    #jwk = next((key for key in keys["keys"] if key["kid"] == header["kid"]), None)
    #if not jwk:
    #    raise HTTPException(status_code=401, detail="Public key not found")
#
    ## Convert the JWK to a PEM-formatted key
    #pem_key = jwk_to_pem(jwk)
#
    ## Verify the token signature, audience, issuer, and expiration
    #try:
    #    payload = jwt.decode(
    #        token,
    #        pem_key,
    #        algorithms=["RS256"],
    #        audience=settings.APP_ID,
    #        issuer=settings.TOKEN_ISSUER,
    #        options={"verify_exp": True, "verify_aud": False, "verify_iat": True},
    #    )
    #    return payload
#
    #except ExpiredSignatureError:
    #    raise HTTPException(status_code=401, detail="Token has expired")
    #except DecodeError:
    #    raise HTTPException(status_code=401, detail="Invalid or malformed token")
    #except jwt.exceptions.InvalidTokenError:
    #    raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        payload = verify_token(token)
        return User(
            id=payload["sub"],
            username=payload["name"],
            email=payload["emails"][0],
            full_name=f'{payload["given_name"]} {payload["family_name"]}',
            disabled=False,
        )

    except HTTPException as e:
        raise e


UserDep = Annotated[User, Depends(get_current_user)]
