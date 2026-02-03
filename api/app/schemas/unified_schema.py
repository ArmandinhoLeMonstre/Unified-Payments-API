from pydantic import BaseModel, model_validator
from typing_extensions import Self

class SyncRequest(BaseModel):
    providers: list[str]

    @model_validator(mode="after")
    def check_amount(self) -> Self:
        providers_available = [
            "stripe",
            "mollie"
        ]
        
        if not self.providers:
            raise ValueError("empty request")

        for provider in self.providers:
            if provider not in providers_available:
                raise ValueError(f'{provider} is not a valid provider')
        
        return self
