from mollie.api.client import Client
from mollie.api.error import RequestSetupError, BadRequestError, UnauthorizedError
from fastapi import HTTPException
import stripe
from stripe import AuthenticationError

def mollie_credentials_test(api_key):
    client = Client()

    try:
        client.set_api_key(api_key)
    except RequestSetupError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Mollie Api key"
        )
    try:
        client.methods.list(resource="orders")
    except BadRequestError as e:
        raise HTTPException(
            status_code=401, 
            detail=str(e)
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=401, 
            detail=str(e)
        )

    return(0)

def stripe_credentials_test(api_key):
    stripe.api_key = api_key

    try:
        stripe.Account.retrieve()
    except AuthenticationError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

    return(0)