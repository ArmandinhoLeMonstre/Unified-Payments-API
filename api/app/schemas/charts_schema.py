from pydantic import BaseModel, ConfigDict, ValidationError, model_validator
from typing import Dict
from datetime import datetime

class ChartsResponse(BaseModel):
    chart: Dict[str, int]
