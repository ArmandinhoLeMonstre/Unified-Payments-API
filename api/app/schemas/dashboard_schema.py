from pydantic import BaseModel, Field, ConfigDict, ValidationError, model_validator
from typing_extensions import Self
from typing import Dict
from datetime import datetime

class TableRequest(BaseModel):
    limit: int = Field(5, gt=0, le=100)
    offset: int = Field(0, ge=0)
    start: int | None = Field(None, gt=0)
    end: int | None = Field(None, gt=0)

    @model_validator(mode="after")
    def check_start_and_end(self) -> Self:
        if self.start and self.end:
            if self.end >= self.start:
                raise ValueError(f'End : {self.end} >= Start: {self.start}, this is an invalid duration')
        
        return self

class TableResponse(BaseModel):
    created_at: datetime
    provider: str
    provider_id: str
    amount: int
    currency: str
    status: str

    model_config = ConfigDict(from_attributes=True) #This is to convert SQLAlchemy attributes

class RevenueRequest(BaseModel):
    currencies: list[str]
    providers: list[str]
    hours: int

    @model_validator(mode="after")
    def check_currency_and_hours(self) -> Self:
        currencies_available = ["eur", "usd"]

        for currency in self.currencies:
            if (currency not in currencies_available):
                raise ValueError(f'{currency} is not a valid currency')
        
        if (self.hours < 24 or self.hours > 720):
            raise ValueError(f'{self.hours} is an invalid duration, has to be between 1 hour and 30 days') # Change this to minutes after
        
        return self

class OverviewRequest(BaseModel):
    hours: int

class OverviewResponse(BaseModel):
    revenues: Dict[str, int]
    transactions: int
    last_sync: datetime | None

class RevenueByCurrencyResponse(BaseModel):
    currency: str
    revenue: int

class RevenueByCurrency(BaseModel):
    currency: str
    total: int

class TransactionsRequest(BaseModel):
    providers: list[str]
    statuses: list[str]
    hours: int

    @model_validator(mode="after")
    def check_status_and_hours(self) -> Self:
        statuses_available = ["succeeded", "failed", "pending", "requires_action"]
        providers_available = [
            "stripe",
            "mollie"
        ]
        for status in self.statuses:
            if (status not in statuses_available):
                raise ValueError(f'{status} is not a valid status')

        if (self.hours < 24 or self.hours > 720):
            raise ValueError(f'{self.hours} is an invalid duration, has to be between 1 hour and 30 days') # Change this to minutes after
        
        for provider in self.providers:
            if provider not in providers_available:
                raise ValueError(f'{provider} is not a valid provider')
        
        return self

class TransactionsResponse(BaseModel):
    transactions: Dict[str, Dict[str, int]]

