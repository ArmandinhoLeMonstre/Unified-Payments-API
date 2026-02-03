from pydantic import BaseModel, ConfigDict, ValidationError, model_validator
from typing_extensions import Self

class ApiKeyRequest(BaseModel):
    provider: str
    api_key: str

    @model_validator(mode="after")
    def check_amount(self) -> Self:
        providers_available = [
            "stripe",
            "mollie"
        ]
        
        if not self.provider:
            raise ValueError("empty request")
        
        if not self.api_key:
            raise ValueError("empty request")

        if self.provider not in providers_available:
            raise ValueError(f'{self.provider} is not a valid provider')
        
        return self

class ProviderStatusRequest(BaseModel):
    provider: str

    @model_validator(mode="after")
    def check_provider(self) -> Self:
        providers_available = [
            "stripe",
            "mollie"
        ]

        if not self.provider:
            raise ValueError("empty request")

        if self.provider not in providers_available:
            raise ValueError(f'{self.provider} is not a valid provider')

        return self