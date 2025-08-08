from pydantic import BaseModel
from typing import List

class BandNameRequest(BaseModel):
    description: str

class BandNameResponse(BaseModel):
    name_options: List[str]

class VenueRequest(BaseModel):
    band_style: str
    expected_audience: int = 50

class VenueRecommendation(BaseModel):
    name: str
    neighborhood: str
    capacity: str
    genres: str
    description: str
    why_recommended: str

class VenueResponse(BaseModel):
    venues: List[VenueRecommendation]
